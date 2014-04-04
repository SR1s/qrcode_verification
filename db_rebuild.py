from qv.app import app
from qv.app import db

with app.test_request_context():
    db.drop_all()
    db.create_all()