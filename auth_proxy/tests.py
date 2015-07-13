from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import requests_unixsocket
import threading
import unittest
import os

from vesna.alh_auth_proxy import ALHAuthProxy

class TestAuthProxy(unittest.TestCase):

	def setUp(self):
		self.path = "/tmp/alh.sock"
		self.a = None

	def tearDown(self):
		if self.a is not None:
			self.a.stop()
			self.t.join()

	def _start(self, **kwargs):
		self.a = ALHAuthProxy(self.path, **kwargs)
		self.t = threading.Thread(target=self.a.start)
		self.t.start()

	def _get(self, path):
		session = requests_unixsocket.Session()
		return session.get('http+unix://%s/%s' % (self.path.replace('/', '%2F'), path))

	def test_invalid(self):
		self._start()

		r = self._get('foo')
		self.assertEqual(r.status_code, 404)

	def test_get(self):
		self._start()

		r = self._get('communicator')
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'Hello, world!')

	def test_auth(self):

		l = []

		class MockAuthenticator:
			def is_allowed(self, pid, uid, gid):
				l.append((pid, uid, gid))
				return False

		self._start(auth=MockAuthenticator())
		r = self._get('communicator')
		self.assertEqual(r.status_code, 403)
		self.assertEqual(l[0], (os.getpid(), os.getuid(), os.getgid()))

if __name__ == '__main__':
	unittest.main()
