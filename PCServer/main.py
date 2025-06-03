from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import re
import socket

UPLOAD_DIR = "uploads"
PORT = 8000

class SimpleUploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        html = '''
            <html><body>
            <h2>Upload a File</h2>
            <form enctype="multipart/form-data" method="post">
                <input name="file" type="file"/>
                <input type="submit" value="Upload"/>
            </form>
            </body></html>
        '''
        self.wfile.write(html.encode())

    def do_POST(self):
        content_type = self.headers.get('Content-Type')
        if not content_type or 'multipart/form-data' not in content_type:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Expected multipart/form-data')
            return

        boundary_match = re.search('boundary=(.+)', content_type)
        if not boundary_match:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'No boundary in content type')
            return

        boundary = boundary_match.group(1).encode()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        parts = body.split(b'--' + boundary)
        for part in parts:
            if b'Content-Disposition' in part and b'name="file"' in part:
                header_part, file_data = part.split(b'\r\n\r\n', 1)
                file_data = file_data.rstrip(b'\r\n--')

                # Extract filename using regex
                filename_match = re.search(b'filename="(.+?)"', header_part)
                if not filename_match:
                    continue
                filename = filename_match.group(1).decode('utf-8')

                os.makedirs(UPLOAD_DIR, exist_ok=True)
                path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
                with open(path, 'wb') as f:
                    f.write(file_data)

                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Uploaded: {filename}".encode())
                return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'No valid file uploaded')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()

def run():
    ip = get_local_ip()
    print(f"Server is running:")
    print(f"  -> Local:    http://localhost:{PORT}/")
    print(f"  -> Network:  http://{ip}:{PORT}/")
    print("\nUse the network address on your laptop to connect.")

    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, SimpleUploadHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()

'''
to make this accessible outside your wifi network, theoretically:
1. 🔁 Set Up Port Forwarding on Your Router
Log into your router (usually at 192.168.1.1).

Go to Port Forwarding settings.

Forward external port 8000 to:

Internal IP: your PC's local IP (e.g., 192.168.1.123)

Internal port: 8000

This lets traffic from the internet reach your local server.

2. 🌐 Get Your Public IP Address
Go to https://whatismyipaddress.com from your PC.
You’ll see something like 123.45.67.89.

Then from any remote device, go to:

http://123.45.67.89:8000/
'''