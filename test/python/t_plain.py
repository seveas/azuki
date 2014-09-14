from azuki import beanstalk
import os
import sys
import unittest

@beanstalk(os.environ['test_tube'])
def hello(arg):
    print("Hello, %s" % arg)
    sys.exit(0)

class AzukiTest(unittest.TestCase):
    def test_azuki(self):
        self.assertEqual(type(hello("world")), int)

    def test_serializer(self):
        self.assertRaises(TypeError, lambda: hello(self))
