import urllib
import os

from flask import Flask, render_template, request, redirect, session
import requests
import stripe


app = Flask(__name__)
app.config.from_pyfile('_config.py')


@app.route('/')
def index():
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
    # For this demo, just save it in session
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
        # Need to set up the API key
        stripe.api_key = app.config['API_KEY']
        # Amount is always in cents
        amount = 1000
        try:
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
