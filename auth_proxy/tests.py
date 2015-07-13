from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import requests_unixsocket
import threading
import unittest
import os

from vesna.alh_auth_proxy import ALHAuthProxy
from vesna.alh import ALHWeb

class MockALH:
	def __init__(self):
		self.requests = []

	def get(self, resource, *args):
		self.requests.append(('get', resource, args))
		return 'get'

	def post(self, resource, data, *args):
		self.requests.append(('post', resource, data, args))
		return 'post'

class TestAuthProxyMockedALH(unittest.TestCase):

	def setUp(self):
		self.path = "/tmp/alh.sock"
		self.a = None

	def tearDown(self):
		if self.a is not None:
			self.a.stop()
			self.t.join()

	def _start(self, **kwargs):
		self.alh = MockALH()

		clusters = {'test': self.alh}

		self.a = ALHAuthProxy(self.path, clusters=clusters, **kwargs)
		self.t = threading.Thread(target=self.a.start)
		self.t.start()

	def _get(self, path, params=None):
		session = requests_unixsocket.Session()
		return session.get('http+unix://%s/%s' % (self.path.replace('/', '%2F'), path), params=params)

	def test_invalid_url(self):
		self._start()

		r = self._get('foo')
		self.assertEqual(r.status_code, 404)

	def test_missing_uid(self):
		self._start()

		r = self._get('communicator')
		self.assertEqual(r.status_code, 400)

	def test_wrong_uid(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'foo'})
		self.assertEqual(r.status_code, 404)

	def test_no_method(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test'})
		self.assertEqual(r.status_code, 400)

	def test_wrong_method(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'foo'})
		self.assertEqual(r.status_code, 400)

	def test_get_no_resource(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get'})
		self.assertEqual(r.status_code, 400)

	def test_get(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'get')
		self.assertEqual(self.alh.requests, [('get', '/test', ('',))])

	def test_post_no_resource(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post'})
		self.assertEqual(r.status_code, 400)

	def test_post_no_data(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post', 'resource':'/test'})
		self.assertEqual(r.status_code, 400)

	def test_post(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'post', 'resource':'/test', 'content': 'data'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'post')
		self.assertEqual(self.alh.requests, [('post', '/test', 'data', ('',))])

	def test_auth(self):

		l = []

		class MockAuthenticator:
			def is_allowed(self, pid, uid, gid):
				l.append((pid, uid, gid))
				return False

		self._start(auth=MockAuthenticator())

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 403)
		self.assertEqual(self.alh.requests, [])
		self.assertEqual(l[0], (os.getpid(), os.getuid(), os.getgid()))

class TestAuthProxyALHWeb(unittest.TestCase):

	def setUp(self):
		self.path = "/tmp/alh.sock"
		self.a = None

		self.l = l = [0]

		class MockHTTPRequestHandler(BaseHTTPRequestHandler):
			def do_GET(self):
				self.send_response(200)
				self.end_headers()

				self.wfile.write('bar')

				l[0] += 1

		server_address = ('localhost', 12345)
		self.httpd = HTTPServer(server_address, MockHTTPRequestHandler)
		self.t = threading.Thread(target=self.httpd.serve_forever)
		self.t.start()

	def tearDown(self):
		self.httpd.shutdown()
		self.t.join()

		if self.a is not None:
			self.a.stop()
			self.t2.join()

	def _start(self, **kwargs):
		self.alh = ALHWeb("http://localhost:12345", "1")
		clusters = {'test': self.alh}

		self.a = ALHAuthProxy(self.path, clusters=clusters, **kwargs)
		self.t2 = threading.Thread(target=self.a.start)
		self.t2.start()

	def _get(self, path, params=None):
		session = requests_unixsocket.Session()
		return session.get('http+unix://%s/%s' % (self.path.replace('/', '%2F'), path), params=params)


	def test_proxy(self):
		self._start()

		r = self._get('communicator', {'cluster_uid': 'test', 'method': 'get', 'resource':'/test'})
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'bar')
		self.assertEqual(self.l[0], 1)

if __name__ == '__main__':
	unittest.main()
