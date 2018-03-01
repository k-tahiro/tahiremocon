#!/usr/bin/env python3

"""
BTO IR Server Api with Flask-RESTful
"""

import begin

from flask import Flask

from app import api, db

DB_FILE = '/var/opt/tahiremocon/command.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
db.init_app(app)
api.init_app(app)


@begin.start
def main(host='0.0.0.0', debug=False):
    """
    main method
    """
    app.run(host=host, debug=debug)
