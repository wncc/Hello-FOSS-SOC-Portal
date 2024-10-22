# Write your functions for uploading the projects from csv file.. 

# Use projects.csv 
import csv
from django.core.management.base import BaseCommand
from projects.models import Project  # Assuming you have a Project model
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Upload projects from a CSV file'

    def add_arguments(self, parser):
        # Argument for the CSV file path
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        # Open the CSV file
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    # Replace 'name', 'description' with your actual field names
                    project, created = Project.objects.update_or_create(
                        name=row['name'],
                        defaults={
                            'description': row['description'],
                            'start_date': row['start_date'],  # Adjust field names as per your model
                            'end_date': row['end_date'],
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Project '{project.name}' created successfully."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Project '{project.name}' updated successfully."))

                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"Missing field in CSV: {e}"))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(f"Database error: {e}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

