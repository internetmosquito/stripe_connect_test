from stripe_connect_test import db


class Customer(db.Model):

    __tablename__ = "customers"

    customer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stripe_id = db.Column(db.String, nullable=False)
    stripe_email = db.Column(db.Integer, nullable=False)
    stripe_account_balance = db.Column(db.Integer, nullable=True)
    stripe_creation_time = db.Column(db.Integer, nullable=True)
    stripe_currency = db.Column(db.String, nullable=True)
    stripe_delinquent = db.Column(db.Boolean, nullable=True)
    stripe_description = db.Column(db.String, nullable=True)

    def __init__(self, stripe_id, email, account_balance=None, creation_time=None, currency=None,
                 delinquent=None, description=None):
        self.stripe_id = stripe_id
        self.stripe_email = email
        self.stripe_account_balance = account_balance
        self.stripe_creation_time = creation_time
        self.stripe_currency = currency
        self.stripe_delinquent = delinquent
        self.stripe_description = description

    def __repr__(self):
        return '<Stripe ID {0}>'.format(self.stripe_id)
