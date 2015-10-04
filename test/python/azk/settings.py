import os
BASE_DIR = os.path.dirname(__file__)
BEANSTALK_SERVERS = {'default': {'host': '127.0.0.1', 'port': 11300}}
SECRET_KEY = "unused"
DEBUG = True
INSTALLED_APPS = ( 'azk.azu', )
MIDDLEWARE_CLASSES = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.environ.get('SHARNESS_TRASH_DIRECTORY', BASE_DIR), 'db.sqlite3'),
    }
}
