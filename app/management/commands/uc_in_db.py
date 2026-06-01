import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from app.models import Combo, Brand, Category


class Command(BaseCommand):
    help = "Import Combo data from CSV (robust version)"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to CSV file"
        )

    def normalize_headers(self, fieldnames):
        """
        Fix BOM, spaces, and hidden characters in headers
        """
        return [
            f.strip().replace("\ufeff", "") if f else f
            for f in fieldnames
        ]

    @transaction.atomic
    def handle(self, *args, **kwargs):

        file_path = kwargs["csv_file"]

        created_count = 0
        updated_count = 0
        skipped_count = 0

        # ---------------- FILE CHECK ----------------
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        try:
            with open(file_path, newline="", encoding="utf-8-sig") as file:

                reader = csv.DictReader(file)

                # Normalize headers (IMPORTANT FIX)
                reader.fieldnames = self.normalize_headers(reader.fieldnames)

                # ---------------- REQUIRED COLUMNS ----------------
                required_columns = [
                    "main_model",
                    "compatible_model",
                    "brand",
                    "category",
                ]

                missing = [
                    col for col in required_columns
                    if col not in reader.fieldnames
                ]

                if missing:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Missing required columns: {', '.join(missing)}"
                        )
                    )
                    return

                # ---------------- PROCESS ROWS ----------------
                for row_number, row in enumerate(reader, start=2):

                    try:
                        main_model = (row.get("main_model") or "").strip()
                        compatible_model = (row.get("compatible_model") or "").strip()
                        brand_name = (row.get("brand") or "").strip()
                        category_name = (row.get("category") or "").strip()

                        # OPTIONAL COLUMN (safe fallback)
                        is_active_raw = (row.get("is_active") or "true").strip().lower()
                        is_active_value = is_active_raw in ["true", "1", "yes"]

                        # Skip empty main model
                        if not main_model:
                            skipped_count += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Row {row_number}: skipped (empty main_model)"
                                )
                            )
                            continue

                        # ---------------- BRAND ----------------
                        brand = None
                        if brand_name:
                            brand, _ = Brand.objects.get_or_create(name=brand_name)

                        # ---------------- CATEGORY ----------------
                        category = None
                        if category_name:
                            category, _ = Category.objects.get_or_create(name=category_name)

                        # ---------------- COMBO UPSERT ----------------
                        combo, created = Combo.objects.update_or_create(
                            main_model=main_model,
                            defaults={
                                "compatible_model": compatible_model,
                                "brand": brand,
                                "category": category,
                                "is_active": is_active_value,
                            }
                        )

                        if created:
                            created_count += 1
                        else:
                            updated_count += 1

                    except Exception as e:
                        skipped_count += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f"Row {row_number} skipped: {str(e)}"
                            )
                        )

            # ---------------- SUMMARY ----------------
            self.stdout.write(
                self.style.SUCCESS(
                    "\nImport Completed Successfully!\n"
                    f"Created : {created_count}\n"
                    f"Updated : {updated_count}\n"
                    f"Skipped : {skipped_count}\n"
                )
            )

        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Fatal Error: {str(error)}"))