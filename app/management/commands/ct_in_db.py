# =========================================================
# MANAGEMENT COMMAND
# Import Category Data from CSV
# File:
# app_name/management/commands/import_categories.py
# =========================================================

import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from app_name.models import Category


class Command(BaseCommand):
    help = "Import categories from CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="CSV file path"
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):

        csv_file = kwargs["csv_file"]

        # =====================================================
        # CHECK FILE EXISTS
        # =====================================================
        if not os.path.exists(csv_file):

            self.stdout.write(
                self.style.ERROR(
                    f"File not found: {csv_file}"
                )
            )
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        try:
            with open(
                csv_file,
                mode="r",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                # =================================================
                # REQUIRED CSV COLUMNS
                # =================================================
                required_columns = [
                    "name",
                    "slug",
                    "order",
                    "is_active"
                ]

                # =================================================
                # VALIDATE CSV COLUMNS
                # =================================================
                for column in required_columns:

                    if column not in reader.fieldnames:

                        self.stdout.write(
                            self.style.ERROR(
                                f"Missing required column: {column}"
                            )
                        )
                        return

                # =================================================
                # PROCESS CSV ROWS
                # =================================================
                for row_number, row in enumerate(
                    reader,
                    start=2
                ):
                    try:
                        name = row.get(
                            "name",
                            ""
                        ).strip()

                        slug = row.get(
                            "slug",
                            ""
                        ).strip()

                        order = row.get(
                            "order",
                            "0"
                        ).strip()

                        is_active = row.get(
                            "is_active",
                            "True"
                        ).strip().lower()

                        # =========================================
                        # EMPTY NAME CHECK
                        # =========================================
                        if not name:

                            skipped_count += 1

                            self.stdout.write(
                                self.style.WARNING(
                                    f"Row {row_number}: Empty name skipped."
                                )
                            )
                            continue

                        # =========================================
                        # BOOLEAN CONVERSION
                        # =========================================
                        is_active_value = is_active in [
                            "true",
                            "1",
                            "yes"
                        ]

                        # =========================================
                        # INTEGER CONVERSION
                        # =========================================
                        try:
                            order_value = int(order)

                        except ValueError:
                            order_value = 0

                        # =========================================
                        # AUTO GENERATE SLUG
                        # =========================================
                        if not slug:
                            slug = slugify(name)

                        # =========================================
                        # CREATE OR UPDATE
                        # =========================================
                        category, created = Category.objects.update_or_create(
                            name=name,
                            defaults={
                                "slug": slug,
                                "order": order_value,
                                "is_active": is_active_value,
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
                                f"Row {row_number} skipped: {str(row_error)}"
                            )
                        )

            # =====================================================
            # SUCCESS MESSAGE
            # =====================================================
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nImport Completed Successfully!\n"
                    f"Created : {created_count}\n"
                    f"Updated : {updated_count}\n"
                    f"Skipped : {skipped_count}\n"
                )
            )

        except Exception as error:

            self.stdout.write(
                self.style.ERROR(
                    f"Error: {str(error)}"
                )
            )