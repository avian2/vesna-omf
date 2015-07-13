import requests_unixsocket
import threading
import unittest
import os

from vesna.alh_auth_proxy import ALHAuthProxy

class TestAuthProxy(unittest.TestCase):

	def _start(self, **kwargs):
		self.a = ALHAuthProxy(self.path, **kwargs)
		self.t = threading.Thread(target=self.a.start)
		self.t.start()

	def setUp(self):
		self.path = "/tmp/alh.sock"

	def tearDown(self):
		self.a.stop()
		self.t.join()

	def test_init(self):
		self._start()
		session = requests_unixsocket.Session()

		# Access /path/to/page from /tmp/profilesvc.sock
		r = session.get('http+unix://%s/foo' % (self.path.replace('/', '%2F'),))
		self.assertEqual(r.status_code, 200)
		self.assertEqual(r.text, 'Hello, world!')

if __name__ == '__main__':
	unittest.main()
