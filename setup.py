#!/usr/bin/python

from distutils.core import setup

setup(name = "azuki",
      version = "1.2",
      author = "Dennis Kaarsemaker",
      author_email = "dennis@kaarsemaker.net",
      url = "http://github.com/seveas/azuki",
      description = "Beanstalkd utilities for CLI and python",
      package_dir = {'': 'lib'},
      packages = ["azuki","azuki.management","azuki.management.commands"],
      scripts = ["bin/azuki"],
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      install_requires=["whelk>=2.4", "docopt>=0.5.0", "PyYAML>=3.10", "beanstalkc>=0.3.0"],
)
