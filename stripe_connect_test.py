import urllib
import os

import requests
import stripe
from flask import Flask, render_template, request, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

import models

@app.route('/')
def index():
    # Need to set up the API key
    stripe.api_key = app.config['API_KEY']
    # Check if the Stripe Account has already authorized our app
    if session.get('connected_user_id'):
        try:
            # Get the account associated with the token (our connected account)
            user_acct = stripe.Account.retrieve(session['connected_user_id'])
            public_key = app.config['PUBLIC_KEY']
            return render_template('index.html', auth=True, user_id=user_acct.email, pk=public_key)
        except Exception as e:
            print(repr(e))
            return render_template('error.html', error=repr(e))
    else:
        # Just show the regular index to connect with Stripe
        return render_template('index.html')

@app.route('/authorize')
def authorize():
    # Build the URI for letting a Stripe user authorize our app to make charges on their behalf
    site = app.config['SITE'] + app.config['AUTHORIZE_URI']
    # We need to ask for read_write permissions and provide our client ID
    params = {
        'response_type': 'code',
        'scope': 'read_write',
        'client_id': app.config['CLIENT_ID']
    }

    # Redirect to Stripe /oauth/authorize endpoint
    url = site + '?' + urllib.urlencode(params)
    # Stripe will get this and send the response to the callback URI specified for our platform
    return redirect(url)

@app.route('/oauth/callback')
def callback():
    # Get the response from Stripe
    code = request.args.get('code')
    # Build the dict needed to get a token
    data = {
        'client_secret': app.config['API_KEY'],
        'grant_type': 'authorization_code',
        'client_id': app.config['CLIENT_ID'],
        'code': code
    }

    # Make /oauth/token endpoint POST request
    url = app.config['SITE'] + app.config['TOKEN_URI']
    resp = requests.post(url, params=data)

    # Grab access_token (use this as your user's API key)
    token = resp.json().get('access_token')

    # We should store access_token, refresh_token, stripe_user_id,
    # For this demo, just save it in session for this demo
    session['access_token'] = token
    session['refresh_token'] = resp.json().get('refresh_token')
    session['connected_user_id'] = resp.json().get('stripe_user_id')

    public_key = app.config['PUBLIC_KEY']

    # Show a view to actually make a fake charge on behalf of the connected account
    return render_template('callback.html', token=token, pk=public_key)


@app.route('/charge', methods=['POST'])
def charge():
    if request.form:
        stripe_token = request.form.get('stripeToken')
        stripe_email = request.form.get('stripeEmail')
        connected_user_id = session['connected_user_id']

        try:
            # Check if there is a Customer already created for this email
            platform_account_customers = stripe.Customer.list()
            platform_customer = [cus for cus in platform_account_customers if cus.email == stripe_email]
            # If there was no customer, need to create a new platform customer
            if not platform_customer:
                stripe_customer = stripe.Customer.create(
                    email=stripe_email,
                    source=stripe_token,
                )
                # Check if we had the customer in he db
                if not db.session.query(models.Customer).filter('email' == stripe_email).count():
                    #Create the db user
                    new_customer = models.Customer(
                        stripe_id=stripe_customer.stripe_id,
                        email=stripe_customer.email,
                        account_balance=stripe_customer.account_balance,
                        creation_time=stripe_customer.created,
                        currency=stripe_customer.currency,
                        delinquent=stripe_customer.delinquent,
                        description=stripe_customer.description,
                    )
                    db.session.add(new_customer)
                    db.session.commit()

                # Need to recreate the token to be able to crete the customer on the connected account too
                cus_token = stripe.Token.create(
                    customer=stripe_customer.id,
                    stripe_account=connected_user_id
                )
                # Create the customer in the connected account
                connected_account_customer = stripe.Customer.create(
                    email=stripe_customer.email,
                    source=cus_token.id,
                    stripe_account=connected_user_id,
                )
                # Make the charge to the customer on the connected account
                amount = 10000
                stripe.Charge.create(
                    amount=amount,
                    currency='eur',
                    customer=connected_account_customer.id,
                    stripe_account=connected_user_id,
                    application_fee=123,
                )
            # Just make the charge
            else:
                # Amount is always in cents
                amount = 10000
                stripe.Charge.create(
                    amount=amount,
                    currency='eur',
                    source=stripe_token,
                    stripe_account=connected_user_id,
                    application_fee=123,
                )

        except Exception as e:
            print(repr(e))
            return render_template('error.html', error=repr(e))
        return render_template('success.html', payment_amount=str(amount / 100), connected_account_id=connected_user_id,
                               connected_account_email=stripe_email)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run()
