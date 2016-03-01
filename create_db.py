from stripe_connect_test import db

# create the database and the db table
db.create_all()

# commit the changes
db.session.commit()
