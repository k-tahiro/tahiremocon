import os
import subprocess


class BtoIrCmd:
    def __init__(self, cmd: str = '/usr/local/bin/bto_ir_cmd'):
        args = [cmd, '-e'] if os.getuid() == 0 else ['sudo', cmd, '-e']
        self._receive_args = args + ['-r']
        self._transmit_args = args + ['-t']

    def receive(self) -> str:
        result = subprocess.run(self._receive_args, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        return result.stdout.decode().split()[-1]

    def transmit(self, code: str):
        args = self._transmit_args + [code]
        result = subprocess.run(args, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr)


class CameraCmd:
    def __init__(self, cmd: str = os.path.join(os.path.dirname(__file__), '../bin/camera.sh')):
        self._args = [cmd] if os.getuid() == 0 else ['sudo', cmd]

    def run(self) -> str:
        result = subprocess.run(self._args, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        return result.stdout.decode()


if __name__ == '__main__':
    bto_ir_cmd = BtoIrCmd()
    result = bto_ir_cmd.receive()
    print(result)
