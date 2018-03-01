import subprocess

from flask_restful import Api, Resource, reqparse

from database import db, Command

CMD_FILE = '/usr/local/bin/bto_ir_cmd'


# 管理API
class BtoIrCmdAdmin(Resource):
    """
    赤外線リモコン操作API管理クラス
    """

    def get(self):
        return [command.name for command in Command.query.all()]


class BtoIrCmdBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('data', required=True)

    @staticmethod
    def _get_cmd_name():
        args = BtoIrCmdBase.parser.parse_args()
        return "暖房_24"


# 送信API
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


# 受信API
class BtoIrCmdReceiver(BtoIrCmdBase):
    """
    赤外線リモコン信号受信クラス
    """

    def post(self):
        cmd_name = self._get_cmd_name()
        print(f'Recieve command: {cmd_name}')

        try:
            sp = subprocess.run(['sudo', CMD_FILE, '-e', '-r'],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except subprocess.SubprocessError:
            return {'success': False}

        cmd = sp.stdout.decode().split()[7]
        BtoIrCmdReceiver._append_cmd(cmd_name, cmd)
        return {'success': True}

    @staticmethod
    def _append_cmd(cmd_name: str, cmd: str):
        db.session.add(Command(cmd_name, cmd))
        db.session.commit()


api = Api()
api.add_resource(BtoIrCmdAdmin, '/bto_ir_cmd')
api.add_resource(BtoIrCmdTransmitter, '/bto_ir_cmd/transmit')
api.add_resource(BtoIrCmdReceiver, '/bto_ir_cmd/receive')
