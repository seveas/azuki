from django.db import models
from azuki import beanstalk
import sys,os

class Azu(models.Model):
    name = models.CharField("Name", max_length=24)

    @beanstalk(os.environ['test_tube'])
    def greet(self):
        print("Hello, %s" % self.name)
        sys.exit(0)
