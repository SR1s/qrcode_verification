from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.String(255), unique=True)
    number = db.Column(db.String(255))
    description = db.Column(db.Text)
    producer = db.Column(db.String(255))
    note = db.Column(db.Text, default='')
    status = db.Column(db.Integer, default=0)
    
    def __init__(self, feature=None, number=None, \
                 description=None, producer=None, \
                 note=None):
        if feature and number and description:
            self.feature = feature
            self.number = number
            self.description = description
            self.producer = producer
            if note:
                self.note = note
        else:
            raise ValueError