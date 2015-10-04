import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'azk.settings'
from azk.azu.models import Azu

class DjangoTest(unittest.TestCase):
    def test_django(self):
        obj = Azu.objects.create(name="django")
        self.assertEqual(type(obj.greet()), int)
