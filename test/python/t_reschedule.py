from azuki import beanstalk, Reschedule
import os
import sys
import unittest

rescheduled = False

@beanstalk(os.environ['test_tube'])
def hello(arg):
    global rescheduled
    if arg == 2 and not rescheduled:
        rescheduled = True
        raise Reschedule(0)
    print(str(arg))
    if arg == 2:
        sys.exit(0)


class RescheduleTest(unittest.TestCase):
    def test_azuki(self):
        hello(1)
        hello(2)
        hello(3)
