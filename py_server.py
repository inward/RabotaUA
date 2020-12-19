from http.server import BaseHTTPRequestHandler, HTTPServer
import rabotaUa as rab
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        self.send_response(200)
        if path.endswith('css'):
            self.send_header('Content-type','text/css')
            print('css')
        else:
            self.send_header('Content-type','text/html')
        self.end_headers()
        if path == "/":
            path = "pages/index.html"
        if path.startswith('/'):
            path = path[1:]

        try:
            rab.go()
            file  = open(path, 'r', encoding='utf-8')
            print(path)
        except FileNotFoundError:
            file  = open("pages/404.html", 'r')

        message = file.read()
        file.close()
        self.wfile.write(bytes(message, "utf8"))
        return



server = HTTPServer(('127.0.0.1', 8081), myHandler)
server.serve_forever()