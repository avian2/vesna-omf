from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import os
import struct
from SocketServer import TCPServer
from socket import AF_UNIX, SOL_SOCKET
import sys

SO_PEERCRED = 17

class UnixSocketHTTPServer(TCPServer):
	allow_reuse_address = 1
	address_family = AF_UNIX

	def server_close(self):
		TCPServer.server_close(self)
		os.unlink(self.server_address)

class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.end_headers()

		creds = self.request.getsockopt(SOL_SOCKET, SO_PEERCRED, struct.calcsize('3i'))
		pid, uid, gid = struct.unpack('3i',creds)

		print 'pid: %d, uid: %d, gid %d' % (pid, uid, gid)

		self.wfile.write("Hello, world!")

	def log_message(self, format, *args):
		sys.stderr.write("- - - [%s] %s\n" %
                         (self.log_date_time_string(),
                          format%args))

class ALHAuthProxy(object):
	def __init__(self, path):
		self.path = path

	def start(self):
		self.httpd = UnixSocketHTTPServer(self.path, HTTPRequestHandler)
		self.httpd.serve_forever()

	def stop(self):
		self.httpd.shutdown()
		self.httpd.server_close()
