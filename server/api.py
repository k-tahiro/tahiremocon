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
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
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


class BtoIrCmdBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mode', required=True)
    parser.add_argument('degree', type=int, required=True)

    @staticmethod
    def _get_cmd_name():
        args = BtoIrCmdBase.parser.parse_args()
        return f'{args.mode}_{args.degree}'


class BtoIrCmdTransmitter(BtoIrCmdBase):
    """
    赤外線リモコン信号送信クラス
    """

    def post(self):
        cmd_name = self._get_cmd_name()
        print(f'Transmit command: {cmd_name}')
        result = BtoIrCmdTransmitter._exec_cmd(cmd_name)
        return {'success': result}

    @staticmethod
    def _exec_cmd(cmd_name: str) -> int:
        cmd = Command.query.filter_by(name=cmd_name).first()
        if cmd:
            try:
                subprocess.run(['sudo', CMD_FILE, '-e', '-t', cmd.signal])
                return True
            except:
                return False
        else:
            return False


class BtoIrCmdReceiver(BtoIrCmdBase):
    """
    赤外線リモコン信号受信クラス
    """
    def post(self):
        cmd_name = self._get_cmd_name()
        print(f'Recieve command: {cmd_name}')

        try:
            sp = subprocess.run(['sudo', CMD_FILE, '-e', '-r'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.SubprocessError:
            return {'success': False}

        cmd = sp.stdout.decode().split()[7]
        BtoIrCmdReceiver._append_cmd(cmd_name, cmd)
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
