from django.core.management import BaseCommand
import azuki.daemon
import logging
import sys

class Command(BaseCommand):
    help = "Run the azuki daemon"

    def handle(self, *args, **options):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        d = azuki.daemon.Daemon('default')
        d.run()
