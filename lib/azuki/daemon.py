try:
    import beanstalkc
except (ImportError, SyntaxError):
    # Hey, we're on python 3, let's load our fixed version!
    import azuki.beanstalkc as beanstalkc
import azuki
import imp
import logging
import sys
import json
import traceback

try:
    from django.core.exceptions import ImproperlyConfigured
    from django.conf import settings
    from django.db.models import get_model
    from django.db import connections
    django = True
except ImportError:
    django = False
except ImproperlyConfigured:
    django = False

class Daemon(object):
    def __init__(self, beanstalk):
        self.beanstalk = beanstalk
        self.logger = logging.getLogger("azuki")
        self.main_modules = {}

    def run(self):
        azuki.running_azuki_daemon = True
        self.connect()
        while True:
            job = self.fetch()
            try:
                self.handle(job)
                job.delete()
            except Exception:
                self.job_error(job, tb=traceback.format_exc())

    def watch(self, tube):
        azuki.all_tubes[self.beanstalk].add(tube)
    
    def job_error(self, job, message='', tb=None):
        self.logger.error("Error processing job %d from tube %s: %s" % (job.jid, job.stats()['tube'], message))
        if tb:
            for line in tb.split('\n'):
                self.logger.error(line)
        job.bury()

    def handle(self, job):
        try:
            job = json.loads(job.body)
        except ValueError:
            return self.job_error(job, "Could not decode job")
        handler = job.get('handler', None)
        if not hasattr(self, 'handle_' + handler):
            return self.job_error(job, "Unknown handler '%s'" % handler)
        getattr(self, 'handle_' + handler)(job)

    # TODO: handle ImportError, AttributeError
    def handle_function(self, job):
        if job['module'] == '__main__':
            if job['file'] not in self.main_modules:
                with open(job['file']) as fd:
                    dwb = sys.dont_write_bytecode
                    sys.dont_write_bytecode = True
                    self.main_modules[job['file']] = imp.load_module('azuki.fake_main', fd, job['file'], ('', 'r', imp.PY_SOURCE))
                    sys.dont_write_bytecode = dwb
                module = self.main_modules[job['file']]
        else:
            if job['module'] not in sys.modules:
                __import__(job['module'])
            module = sys.modules[job['module']]
        getattr(module, job['function'])(*job['args'], **job['kwargs'])

    # TODO: hanlde model not found, instance not found, AttributeError
    def handle_django(self, job):
        if not django:
            return self.job_error(job, "Unable to handle django jobs")
        model = get_model(job['app'], job['model'])
        instance = model.objects.get(pk=job['pk'])
        self.logger.info("Calling %s.%s.%s, pk %d" % (job['app'], job['model'], job['method'], job['pk']))
        getattr(instance, job['method'])(*job['args'], **job['kwargs'])

        # Close all DB connections so we don't hang/crash later
        for connection in connections:
            connections[connection].close()

    def connect(self):
        self.bs = beanstalkc.Connection(**azuki.beanstalks[self.beanstalk])
        for tube in azuki.all_tubes[self.beanstalk]:
            self.bs.watch(tube)
    
    def fetch(self):
        self.logger.info("Waiting for job")
        try:
            return self.bs.reserve()
        except Exception:
            self.logger.error("Connection to beanstalk failed: %s, reconnecting" % str(sys.exc_info()[1]))
            self.connect()
            return self.bs.reserve()
