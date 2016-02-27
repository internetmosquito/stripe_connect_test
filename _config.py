import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# avoid cross site attacks
SECRET_KEY = 'super_secret_password'
DEBUG = False

# The API Key, can be obtained in Stripe dashboad
API_KEY = ''

# The client ID
CLIENT_ID = ''

# Public key of our Account, need it for the checkout form
PUBLIC_KEY = ''

# Stripe URI
SITE = 'https://connect.stripe.com'

# The authorize URI section
AUTHORIZE_URI = '/oauth/authorize'

# The token URI section
TOKEN_URI = '/oauth/token'
