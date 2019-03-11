import subprocess

from psutil import process_iter
from signal import SIGTERM

from flask import Flask
app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

def start_server_debug():
    app.run(port=1867, host='0.0.0.0')

def start_server():
    subprocess.call('ql --start-server debug > /dev/null 2>&1 &', shell=True)

def kill_server():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 1867:
                proc.send_signal(SIGTERM)
