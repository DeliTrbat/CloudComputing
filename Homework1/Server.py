from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import Controller
import BadRequestException
import json


class Server(BaseHTTPRequestHandler):
    paths = ['/', '/movies']

    def end_headers(self) -> None:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        BaseHTTPRequestHandler.end_headers(self)

    def validate_url(self):
        url = urlparse(self.path)
        print(url)
        if url.path in self.paths or url.path.startswith('/movies/'):
            return url
        return False

    def do_GET(self):
        url = self.validate_url()
        if not url:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404 Not Found", 'utf-8'))
            return

        filters = None
        if url.query:
            filters = url.query

        page = ''
        if url.path.startswith('/movies/'):
            try:
                id = url.path.split('/')[2]
                if not id.isdigit():
                    raise BadRequestException.BadRequestException(
                        "ID must be a number")
                page = Controller.Controller.generate_list(f"id={id}")
                self.send_response(200)
            except Exception as e:
                if e.code == 400:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(bytes(e.message, 'utf-8'))
                    return
                self.send_response(404)
                return

        if url.path == '/movies':
            try:
                page = Controller.Controller.generate_list(filters)
                self.send_response(200)
            except Exception as e:
                self.send_response(404)
        elif url.path == '/':
            self.send_response(200)
            page = "Hello World"

        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(page, 'utf-8'))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        try:
            data_json = json.loads(data.decode('utf-8'))
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Invalid JSON", 'utf-8'))
            return
        try:
            Controller.Controller.add_movie(data_json)
        except Exception as e:
            if e.code == 400:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes(e.message, 'utf-8'))
                return
            if e.code == 409:
                self.send_response(409)
                self.end_headers()
                self.wfile.write(bytes(e.message, 'utf-8'))
                return
            self.send_response(404)
            return
        self.send_response(201)
        self.end_headers()
        self.wfile.write(bytes("Post request received", 'utf-8'))

    def do_PUT(self):
        try:
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            data_json = json.loads(data.decode('utf-8'))
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Invalid JSON", 'utf-8'))
            return
        try:
            Controller.Controller.update_movie(data_json)
        except Exception as e:
            if e.code == 400:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes(e.message, 'utf-8'))
                return
            self.send_response(404)
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("Put request received", 'utf-8'))

    def do_DELETE(self):

        try:
            length = int(self.headers['Content-Length'])
            data = self.rfile.read(length)
            data_json = json.loads(data.decode('utf-8'))
        except:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Invalid JSON", 'utf-8'))
            return
        try:
            Controller.Controller.delete_movie(data_json)
        except Exception as e:
            self.send_response(404)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes("Delete request received", 'utf-8'))


server = HTTPServer(('localhost', 8000), Server)
server.serve_forever()
