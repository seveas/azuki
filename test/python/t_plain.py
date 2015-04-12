from azuki import beanstalk
import os
import sys
import unittest

@beanstalk(os.environ['test_tube'])
def hello(arg):
    print("Hello, %s" % arg)
    sys.exit(0)

@beanstalk(os.environ['test_tube'], priority=1)
def fast_hello(arg):
    print("Hello, important %s" % arg)

class AzukiTest(unittest.TestCase):
    def test_azuki(self):
        self.assertEqual(type(hello("world")), int)
        self.assertEqual(type(fast_hello("world")), int)

    def test_serializer(self):
        self.assertRaises(TypeError, lambda: hello(self))
