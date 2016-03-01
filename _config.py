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

# Database name to store customers of connected accounts
DATABASE = 'customers.db'

# Database user name
USERNAME = 'admin'

# Database password
PASSWORD = '6f53f8f4e2c8dae37fc7352a83b1068c85a4a7706945d649'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

