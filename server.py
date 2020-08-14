import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import yaml
import base64

PAGE="""\
<html>
<head>
<title>Alko</title>
</head>
<body>
<h1>Alko Home</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Alko\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('no auth header received', 'utf-8'))
        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            if self.path == '/':
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                content = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    while True:
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                self.send_error(404)
                self.end_headers()
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('not authenticated', 'utf-8'))

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    with open("config.yml", 'r') as stream:
        config_loaded = yaml.load(stream)
    camera.vflip = config_loaded['vflip']
    camera.hflip = config_loaded['hflip']
    camera.brightness = config_loaded['brightness']
    camera.contrast = config_loaded['contrast']
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 80)
        server = StreamingServer(address, StreamingHandler)
        server.set_auth(config_loaded['auth_user'], config_loaded['auth_pass'])
        server.serve_forever()
    finally:
        camera.stop_recording()
