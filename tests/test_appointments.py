__author__ = 'mosquito'
import os
import unittest

from stripe_connect_test import app, db
from _config import basedir
from models import Customer

TEST_DB = 'test.db'

class CustomersTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.assertEquals(app.debug, False)

    # executed after to each test
    def tearDown(self):
        db.drop_all()

    ########################
    #### helper methods ####
    ########################

    def create_customer(self, stripe_id=None, email=None, account_balance=None,
                        creation_time=None, currency=None, delinquent=None, description=None):
        new_customer = Customer(
            stripe_id=stripe_id,
            email=email,
            account_balance=account_balance,
            creation_time=creation_time,
            currency=currency,
            delinquent=delinquent,
            description=description,
        )
        db.session.add(new_customer)
        db.session.commit()

    ###############
    #### views ####
    ###############
    def test_can_create_customer_and_query_for_it(self):
        self.create_customer('cus_xxxxxxxxxxxx', 'judaspriest@isthebest.com', 0, 123456789, 'eur',
                             False, 'best client ever')
        customers = db.session.query(Customer).all()
        self.assertEquals(len(customers), 1)

    ################
    #### models ####
    ################
    def test_string_reprsentation_of_the_customer_object(self):
        self.create_customer('cus_xxxxxxxxxxxx', 'judaspriest@isthebest.com', 0, 123456789, 'eur',
                             False, 'best client ever')
        customers = db.session.query(Customer).all()
        #print appointments
        for customer in customers:
            self.assertEquals(customer.stripe_id, 'cus_xxxxxxxxxxxx')

if __name__ == "__main__":
    unittest.main()
