# Write your functions for uploading the projects from csv file.. 

# Use projects.csv 
import os
import uuid
from django.core.files import File
import pandas as pd
from projects.models import Project

IMG_PROJECTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    'img'
)

def upload_projects(csv_file_path):
    data = pd.read_csv(csv_file_path)
    no_of_projects = Project.objects.all().__len__
    if no_of_projects != data.__len__:
        Project.objects.all().delete()
        # Iterate through each row and save it to the Project model
        for index ,row in data.iterrows():
            project = Project(
                title=row['title'],
                general_category=row.get('general_category', 'Others'),
                specific_category=row.get('specific_category', 'NA'),
                mentee_max=row['mentee_max'],
                mentor=row.get('mentor', 'NA'),
                co_mentor_info=row.get('co_mentor_info', 'NA'),
                description=row.get('description', 'NA'),
                timeline=row.get('timeline', 'NA'),
                checkpoints=row.get('checkpoints', 'NA'),
                prereuisites=row.get('prereuisites', 'NA'),
                banner_image=row.get('banner_image', None),  
                banner_image_link=row.get('banner_image_link', None),
            )
            image_filename = row.get('banner_image')
            if pd.notna(image_filename):  
                image_path = os.path.join(IMG_PROJECTS_PATH, image_filename)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        project.banner_image.save(image_filename, File(image_file), save=False)

            if not project.code:
                project.code = str(uuid.uuid4())[:8]

            no_of_projects = data.__len__
            project.save()
