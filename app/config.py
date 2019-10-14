import os

DB_FILE = os.getenv('DB_FILE')
MODEL_FILE = os.getenv('MODEL_FILE')
INPUT_SIZE = int(os.getenv('INPUT_SIZE', '224'))
