#!/usr/bin/env python3

"""
BTO IR Server Api with Flask-RESTful
"""

import csv
import os

from flask import Flask
from flask_restful import Resource, Api
import begin

CMD_FILE = '/usr/local/bin/bto_ir_cmd'
CMD_DEF_FILE = '/etc/bto_ir_cmd.csv'
with open(CMD_DEF_FILE) as f:
    reader = csv.reader(f)
    CMD_DEF = {
        row[0]: row[1]
        for row in reader
    }


class BtoIrCmd(Resource):
    """
    赤外線リモコン操作APIクラス
    """

    def get(self, cmd_name: str):
        return_code = BtoIrCmd._exec_cmd(cmd_name)
        if return_code == 0:
            is_success = True
        else:
            is_success = False

        return {'success': is_success}

    @staticmethod
    def _exec_cmd(cmd_name: str) -> int:
        cmd = CMD_DEF.get(cmd_name)
        if cmd:
            return os.system('{CMD_FILE} -e -t {cmd}'.format(CMD_FILE, cmd))
        else:
            return 99


app = Flask(__name__)
api = Api(app)
api.add_resource(BtoIrCmd, '/bto_ir_cmd/<string:cmd_name>')


@begin.start
def main(debug=False):
    """
    main method
    """
    app.run(debug=debug)
