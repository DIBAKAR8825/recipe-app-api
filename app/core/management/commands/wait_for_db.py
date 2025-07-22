"""
Django management command to wait for the database to be ready.
This command is useful in scenarios where the application needs to ensure that
the database is available before proceeding with migrations or starting the server.
It attempts to connect to the database at regular intervals until it succeeds or a timeout is reached.
"""

import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database."""
    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write('Waiting for database...')
        db_up = False
        # Loop until the database is available
        # or a timeout occurs.
        # Adjust the number of retries and sleep duration as needed.
        #  max_retries = 5 # Maximum number of retries
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
