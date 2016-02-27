# Description

A simple Flask project to demonstrate how to use Stripe Connect to make charges on behalf of other Stripe accounts. This is ideal if you plan
to have a marketplace where you charge on behalf of others.

# Requirements

* Flask
* Stripe
* Python :D
* 2 Stripe Accounts (One to act as the marketplace, the other to act as the one that is going to accept payments on Stripe on behalf of the marketplace)

It is highly recommended that you download and use ngrok (https://ngrok.com/download), I use it to be able to test oauth callback when authorizing (oauth dance),
otherwise it is hard to trick Stripe to redirect their request to your localhost machine. Ngrok creates a tunnel that can be used for that, you will need to 
specify the ngrok tunnel in your Stripe Platform (more on this later).

# Usage instructions

* Install requirements from requirements.txt file (pip install -r requirements.txt)
* Start ngrok and redirect all calls from the default Flask port (5000):
    `ngrok http 5000`
* You will need a Stripe Connect platform (thus a Stripe account). Check how to do this here: https://stripe.com/docs/connect#getting-started. Make sure youn don't select Managed account. 
  You will need to specify the address returned by ngrok (i.e. http://97b6f926.ngrok.io) and put it in the RedirectURIs field when registering your platform (i.e. http://97b6f926.ngrok.io/callback)
* You need to specify the API_KEY, CLIENT_ID and PUBLIC_KEY in the _config.py file. I recommended to use the test ones for now (those with _test_ in the key) 
  API_KEY -> Refers to the secret_key of your app. You can find it here https://dashboard.stripe.com/account/applications/settings, in the API Keys tab (Test Secret Key)
  PUBLIC_KEY -> Refers to the public_key of your app. You can find it here https://dashboard.stripe.com/account/applications/settings, in the API Keys tab (Test Publishable Key)
  CLIENT_ID -> Referes to the Connect client ID. You can find it here https://dashboard.stripe.com/account/applications/settings, in the Connect tab (client_id in Development)
* Fire up the server `python stripe_connect_test.py`
* Go to http://127.0.0.1:5000. First step is to authorize the application we just created in Stripe so we can charge on behalf of others. To do so, click in the blue button. 
* This will start the oauth dance, it will redirect to a Stripe page, you will need to create another Stripe Account (to act as the one that is going to receive payments on behalf of our app)
  if you don't have one. Once authorized we get the access_token and refresh_token and you are redirected to the /callback view.
* In the callback view, we can make a test charge, click on the Stripe button. You will be presented with a Stripe Checkout Form. This is just a test, so enter:
    * Any valid test email address (darthvader@rulestheworld.com)
    * Any valid Stripe fake account card number (4242 4242 4242 4242)
    * Any expiry date in the future
    * Any 3 digit for the CCV
    * Do not select to store data for now 
    * Click OK
* Upon successful charge, we've charged the specified amount on behalf of the Stripe user that previously has authorized our app to do so. If you login with the Stripe account that you used
  to authorize the application, you should see a charge being made there in the Successful charges graph.
* Have a look at the code for more insights, its pretty self-explanatory
   
 
