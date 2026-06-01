
import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import Icon


class Command(BaseCommand):
    help = "Import icons from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file'
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Check file exists
        if not os.path.exists(csv_file):
            self.stdout.write(
                self.style.ERROR(f'File not found: {csv_file}')
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                required_columns = ['name', 'class_name', 'is_active']

                # Validate CSV columns
                for column in required_columns:
                    if column not in reader.fieldnames:
                        self.stdout.write(
                            self.style.ERROR(
                                f'Missing required column: {column}'
                            )
                        )
                        return

                for row_number, row in enumerate(reader, start=2):
                    try:
                        name = row.get('name', '').strip()
                        class_name = row.get('class_name', '').strip()
                        is_active = row.get('is_active', 'True').strip().lower()

                        # Skip empty name
                        if not name:
                            skipped_count += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'Row {row_number}: Empty name skipped.'
                                )
                            )
                            continue

                        # Convert boolean safely
                        is_active_value = is_active in ['true', '1', 'yes']

                        # Create or update
                        icon, created = Icon.objects.update_or_create(
                            name=name,
                            defaults={
                                'class_name': class_name,
                                'is_active': is_active_value,
                            }
                        )

                        if created:
                            created_count += 1
                        else:
                            updated_count += 1

                    except Exception as row_error:
                        skipped_count += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'Row {row_number} skipped: {str(row_error)}'
                            )
                        )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Import completed successfully!\n'
                    f'Created: {created_count}\n'
                    f'Updated: {updated_count}\n'
                    f'Skipped: {skipped_count}'
                )
            )

        except Exception as error:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(error)}')
            )
