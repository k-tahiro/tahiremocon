from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    signal = db.Column(db.String(70), unique=True)

    def __init__(self, name, signal):
        self.name = name
        self.signal = signal

    def __repr__(self):
        return '<Command %r>' % self.name
