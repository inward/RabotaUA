from http.server import BaseHTTPRequestHandler, HTTPServer
import rabotaUa as rab
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        path = self.path
        if path == "/":
            path = "/index"

        try:
            rab.go()
            file  = open("pages"+path + ".html", 'r', encoding='utf-8')
        except FileNotFoundError:
            file  = open("pages/404.html", 'r')

        message = file.read()
        file.close()
        self.wfile.write(bytes(message, "utf8"))
        return



server = HTTPServer(('127.0.0.1', 8081), myHandler)
server.serve_forever()