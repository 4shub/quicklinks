import subprocess
import request

from psutil import process_iter
from signal import SIGTERM
from flask import Flask
from api.actions import *



app = Flask(__name__)

@app.route('/status')
def status():
    return Flask.jsonify(status= 'online')

def post_website():
    key = request.form.get('key')
    value = request.form.get('value')

    if not key:
        return Flask.jsonify(error= 'key not provided'), 400

    if not value:
        return Flask.jsonify(error= 'value not provided'), 400

    api.append_or_update_quicklink(key, value)

    return Flask.jsonify(status= 'done'), 201

def delete_website():
    key = request.form.get('key')

    if not key:
        return Flask.jsonify(error= 'key not provided'), 400

    api.remove_quicklink(key)

    return Flask.jsonify(status= 'done')

@app.route('/website', methods=['POST', 'DELETE'])
def website():
    try:
        if request.method == 'POST':
            return post_website()

        if request.method == 'DELETE':
            return delete_website()

        return Flask.jsonify(status= 'None'), 404
    except:
        return Flask.jsonify(error= 'server side error'), 500


def start_server_debug():
    app.run(port=1867, host='0.0.0.0')

def start_server():
    subprocess.call('ql --start-server debug > /dev/null 2>&1 &', shell=True)

def kill_server():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 1867:
                proc.send_signal(SIGTERM)
