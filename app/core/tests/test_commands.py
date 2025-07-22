"""
Test custom Django management commands.
This module contains tests for the custom management commands defined in the application.
It ensures that the commands behave as expected, particularly in scenarios like waiting for the database to be ready.
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


class CommandTests(SimpleTestCase):
    """Test custom Django management commands."""
    @patch('django.core.management.base.BaseCommand.check')
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database when database is ready."""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    @patch('django.core.management.base.BaseCommand.check')
    def test_wait_for_db_delay(self, patched_check, patched_sleep):
        """Test waiting for database when database is not ready."""
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
