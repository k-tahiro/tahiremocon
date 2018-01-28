#!/usr/bin/env python3

"""
BTO IR Server Api with Flask-RESTful
"""

import csv
import os
import subprocess

from flask import Flask
from flask_restful import Resource, Api
import begin

CMD_FILE = '/usr/local/bin/bto_ir_cmd'
CMD_DEF_FILE = '/etc/bto_ir_cmd.csv'


class BtoIrCmdAdmin(Resource):
    """
    赤外線リモコン操作API管理クラス
    """

    def get(self):
        return list(BtoIrCmdAdmin.get_commands.keys())

    @staticmethod
    def get_commands():
        with open(CMD_DEF_FILE) as f:
            reader = csv.reader(f)
            return {
                row[0]: row[1]
                for row in reader
            }


class BtoIrCmd(Resource):
    """
    赤外線リモコン操作APIクラス
    """

    def __init__(**kwargs):
        # smart_engine is a black box dependency
        self.commands = BtoIrCmdAdmin.get_commands()

    def get(self, cmd_name: str):
        return_code = BtoIrCmd._exec_cmd(cmd_name)
        if return_code == 0:
            is_success = True
        else:
            is_success = False

        return {'success': is_success}

    def _exec_cmd(self, cmd_name: str) -> int:
        cmd = self.commands.get(cmd_name)
        if cmd:
            return os.system('{} -e -t {}'.format(CMD_FILE, cmd))
        else:
            return 99

    def post(self, cmd_name: str):
        try:
            cp = subprocess.run([CMD_FILE, '-e', '-r'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.SubprocessError:
            return {'success': False}

        _, _, result = cp.stdout.split()
        cmd = result.strip().split()
        BtoIrCmd._append_cmd(cmd_name, cmd)
        return {'success': True}

    @staticmethod
    def _append_cmd(cmd_name: str, cmd: str):
        with open(CMD_DEF_FILE, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([cmd_name, cmd])


app = Flask(__name__)
api = Api(app)
api.add_resource(BtoIrCmdAdmin, '/bto_ir_cmd')
api.add_resource(BtoIrCmd, '/bto_ir_cmd/<string:cmd_name>')


@begin.start
def main(host='0.0.0.0', debug=False):
    """
    main method
    """
    app.run(host=host, debug=debug)
