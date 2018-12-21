import unittest
from csw_event.RedisConnector import RedisConnector


class RedisTester(unittest.TestCase):
    def test(self):
        r = RedisConnector()
        r.set_foo()
        r.subscribe_foo()
#        time.sleep(10)
#        r.unsubscribe()
#        r.close()
        self.assertEqual(1, 1)

