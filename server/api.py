#!/usr/bin/env python3

"""
BTO IR Server Api with Flask-RESTful
"""

import csv
import os
import subprocess

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import begin

CMD_FILE = '/usr/local/bin/bto_ir_cmd'
DB_FILE = '/var/opt/tahiremocon/command.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_FILE)
db = SQLAlchemy(app)


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True)
    signal = db.Column(db.String(70), unique=True)

    def __init__(self, name, signal):
        self.name = name
        self.signal = signal

    def __repr__(self):
        return '<Command %r>' % self.name


db.create_all()


class BtoIrCmdAdmin(Resource):
    """
    赤外線リモコン操作API管理クラス
    """

    def get(self):
        return [command.name for command in Command.query.all()]


class BtoIrCmdTransmitter(Resource):
    """
    赤外線リモコン信号送信クラス
    """
    r_parser = reqparse.RequestParser()
    r_parser.add_argument('mode', required=True)
    r_parser.add_argument('degree', type=int, required=True)

    def post(self):
        args = BtoIrCmdTransmitter.r_parser.parse_args()
        return_code = BtoIrCmdTransmitter._exec_cmd('{}_{}'.format(args.mode, args.degree))
        return {'success': True if return_code == 0 else False}

    @staticmethod
    def _exec_cmd(cmd_name: str) -> int:
        cmd = Command.query.filter_by(name=cmd_name).first()
        if cmd:
            return os.system('{} -e -t {}'.format(CMD_FILE, cmd))
        else:
            return 99


class BtoIrCmdReceiver(Resource):
    """
    赤外線リモコン信号受信クラス
    """
    r_parser = reqparse.RequestParser()
    r_parser.add_argument('mode', required=True)
    r_parser.add_argument('degree', type=int, required=True)

    def post(self):
        args = BtoIrCmdReceiver.r_parser.parse_args()

        try:
            cp = subprocess.check_call([CMD_FILE, '-e', '-r'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.SubprocessError:
            return {'success': False}

        _, _, result = cp.stdout.split()
        cmd = result.strip().split()
        BtoIrCmdReceiver._append_cmd('{}_{}'.format(args.mode, args.degree), cmd)
        return {'success': True}

    @staticmethod
    def _append_cmd(cmd_name: str, cmd: str):
        db.session.add(Command(cmd_name, cmd))
        db.session.commit()


api = Api(app)
api.add_resource(BtoIrCmdAdmin, '/bto_ir_cmd')
api.add_resource(BtoIrCmdTransmitter, '/bto_ir_cmd/transmit')
api.add_resource(BtoIrCmdReceiver, '/bto_ir_cmd/receive')


@begin.start
def main(host='0.0.0.0', debug=False):
    """
    main method
    """
    app.run(host=host, debug=debug)
