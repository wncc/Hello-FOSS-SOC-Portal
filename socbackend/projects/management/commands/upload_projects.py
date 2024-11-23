import csv
import os
from django.core.management.base import BaseCommand, CommandError
from projects.models import Project  
from django.conf import settings

class Command(BaseCommand):
    help = 'Upload project data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be processed')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"File '{csv_file_path}' does not exist.")

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    project, created = Project.objects.update_or_create(
                        project_id=row['project_id'],
                        defaults={
                            'primary_mentor': row['primary_mentor'],
                            'project_title': row['project_title'],
                            'co_mentor_details': row['co_mentor_details'],
                            'project_category_specific': row['project_category_specific'],
                            'project_description': row['project_description'],
                            'maximum_mentees': row['maximum_mentees'],
                            'prereuisites': row['prereuisites'],
                            'banner_image_path': row['banner_image_path'],
                            'banner_image_url': row['banner_image_url'],
                            'project_timeline': row['project_timeline'],
                            'project_checkpoints': row['project_checkpoints'],
                            'project_category_general': row['project_category_general'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Successfully created project {project.project_title}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Updated project {project.project_title}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))

