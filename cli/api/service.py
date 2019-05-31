import subprocess
import json
import logging

from psutil import process_iter
from signal import SIGTERM


from http.server import BaseHTTPRequestHandler, HTTPServer


from api.actions import *

PORT = 1867


class Server(BaseHTTPRequestHandler):
    def send_json(self, value = { 'status': 'done' }, status_code=200):
        self._set_response(status_code)
        self.wfile.write(json.dumps(value).encode('utf-8'))

    def send_error(self, error_text, status_code=400):
        self._set_response(status_code)
        self.send_json({
            'error': error_text,
        })

    def get_status(self):
        response = {
            'status': 'online'
        }

        self.send_json(response)

    def post_website(self, body):
        data = json.loads(body)

        key = data.get('key')
        url = data.get('url')

        if not key:
            return self.send_error('key not provided')

        if not url:
            return self.send_error('url not provided')

        append_or_update_quicklink(key, url)

        return self.send_json(None, 201)

    def delete_website(self, body):
        data = json.loads(body)
        key = data.get('key')

        if not key:
            return self.send_error('key not provided')

        remove_quicklink(key)

        return self.send_json()

    def _set_response(self, status_code = 200):
        self.send_response(status_code)

        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Methods', 'GET,HEAD,OPTIONS,POST,PUT')
        self.send_header('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers')

        self.end_headers()

    def do_OPTIONS(self):
        self._set_response()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))

        if self.path == '/status':
            self.get_status()
            return

        self._set_response(404)
        self.wfile.write('404 - Not Found'.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), body.decode('utf-8'))

        if self.path == '/website':
            self.post_website(body)
            return

    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), body.decode('utf-8'))

        if self.path == '/website':
            self.delete_website(body)
            return


def start_server_debug():
    logging.basicConfig(level=logging.INFO)
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, Server)
    logging.info('Starting httpd...\n')
    httpd.serve_forever()


def start_server():
    subprocess.call('ql --start-server debug > /dev/null 2>&1 &', shell=True)


def kill_server():
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == PORT:
                proc.send_signal(SIGTERM)
