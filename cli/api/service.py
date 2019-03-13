import subprocess

from psutil import process_iter
from signal import SIGTERM
from flask import Flask, Response, request, jsonify
from api.actions import *



app = Flask(__name__)

def generate_response(data = '', status = 200):
    return data, status

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,HEAD,OPTIONS,POST,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'

    return response

@app.route('/status')
def status():
    return jsonify(status= 'online')

def post_website():
    data = request.get_json()

    key = data.get('key')
    url = data.get('url')

    if not key:
        return generate_response(jsonify(error= 'key not provided'), 400)

    if not url:
        return generate_response(jsonify(error= 'url not provided'), 400)

    append_or_update_quicklink(key, url)

    return generate_response(jsonify(status='done'), 201)

def delete_website():
    data = request.get_json()
    key = data.get('key')

    if not key:
        return generate_response(jsonify(error='key not provided'), 400)

    remove_quicklink(key)

    return generate_response(jsonify(status='done'))

@app.route('/website', methods=['POST', 'DELETE'])
def website():
    try:
        if request.method == 'POST':
            return post_website()

        if request.method == 'DELETE':
            return delete_website()

        return generate_response(jsonify(status='None'), 404)
    except:
        return generate_response(jsonify(error='server side error'), 500)


def start_server_debug():
    app.run(port=1867, host='0.0.0.0')

def start_server():
    subprocess.call('ql --start-server debug > /dev/null 2>&1 &', shell=True)

def kill_server():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == 1867:
                proc.send_signal(SIGTERM)
