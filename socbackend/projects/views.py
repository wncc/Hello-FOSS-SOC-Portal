from rest_framework import generics

from .models import Project
from .serializers import ProjectSerializer, BasicProjectSerializer, MenteePreferenceSerializer, MenteePreferenceSaveSerializer

# from projects.models import Season
from accounts.custom_auth import CookieJWTAuthentication
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Mentee, Project, MenteePreference, MenteeWishlist
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from rest_framework.permissions import AllowAny
import logging
import os
import csv

logger = logging.getLogger(__name__)
# from .serializers import (
#     ProjectAdditionSerializer,
# )

class ProjectDetailView(APIView):
    permission_classes = []
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        project = Project.objects.get(pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)
    

class ProjectWishlist(APIView):
    authentication_classes  = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]  # Allow any user to access the post request

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        
        # logger.error('\n \n Error 1 \n \n ')
        mentee = Mentee.objects.get(user=user_profile)
        # logger.error('\n \n Error 2 \n \n ')
        preferences = MenteeWishlist.objects.filter(mentee=mentee)
        # logger.error('\n \n Error 3 \n \n ')
        project_objects = [preference.project for preference in preferences]
        # logger.error('\n \n Error 4 \n \n ')
        serializer = BasicProjectSerializer(project_objects, many=True)
        # logger.error('\n \n Error 5 \n \n ')
        return Response(serializer.data)
    
    def post(self, request):
        # logger.error('\n \n Error 6 \n \n ')
        # print("HI")
        user_profile = UserProfile.objects.get(user=request.user)
        # logger.error('\n \n Error 7 \n \n ')
        mentee = Mentee.objects.get(user=user_profile)
        # logger.error('\n \n Error 8 \n \n ')
        project_id = request.data["project_id"]
        # logger.error('\n \n Error 9 \n \n ')
        project = Project.objects.get(pk=project_id)
        # logger.error('\n \n Error 10 \n \n ')
        preference = MenteeWishlist(mentee=mentee, project=project)
        # logger.error('\n \n Error 11 \n \n ')
        preference.save()
        # logger.error('\n \n Error 12 \n \n ')
        return Response({"message": "Project added to wishlist."})
    
    def delete(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        mentee = Mentee.objects.get(user=user_profile)
        project_id = request.GET['project_id']
        project = Project.objects.get(pk=project_id)
        preference = MenteeWishlist.objects.get(mentee=mentee, project=project)
        preference.delete()
        return Response({"message": "Project removed from wishlist."})
    
class ProjectPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        mentee = Mentee.objects.get(user=user_profile)
        preferences = MenteePreference.objects.filter(mentee=mentee)
        serializer = MenteePreferenceSerializer(preferences, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        mentee = Mentee.objects.get(user=user_profile)
        project_id = request.data["project"]
        preference = request.data["preference"]
        sop = request.data["sop"]
        project = Project.objects.get(pk=project_id)
        serializer = MenteePreferenceSaveSerializer(data={"mentee": mentee.id, "project": project.id, "preference": preference, "sop": sop})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        mentee = Mentee.objects.get(user=user_profile)
        project_id = request.data["project_id"]
        project = Project.objects.get(pk=project_id)
        preference = MenteePreference.objects.get(mentee=mentee, project=project)
        preference.delete()
        return Response({"message": "Project removed from preferences."})
    
class FileUploadView(APIView):
    authentication_classes  = [CookieJWTAuthentication]

    EXPECTED_HEADERS = ['id','mentor','title','co_mentor_info','specific_category','description','mentee_max','prereuisites','banner_image','banner_image_link','timeline','checkpoints','general_category']
    
    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get('file')
            # print("Uploaded file:", uploaded_file)

            if not uploaded_file:
                return Response({
                    'message': 'No file uploaded.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            file_extension = os.path.splitext(uploaded_file.name)[1]
            if file_extension.lower() != '.csv':
                return Response({
                    'message': 'Unsupported file. Upload only csv file'
                }, status=status.HTTP_400_BAD_REQUEST)
            

            # read csv file directly from memory
            csv_reader = csv.DictReader(uploaded_file.read().decode('utf-8').splitlines())
            headers = []

            is_header_checked = False

            for idx, row in enumerate(csv_reader):
                if not is_header_checked:
                    headers = list(row.keys())
                    is_header_checked = True
                    if headers != self.EXPECTED_HEADERS:
                            raise Exception('Headers mistach: csv file headers corrupted')

                try:
                    project, created = Project.objects.get_or_create(
                        title=row['title'].strip(),
                        mentor=row['mentor'].strip(),
                        defaults={
                            'co_mentor_info': row['co_mentor_info'],
                            'specific_category': row['specific_category'],
                            'description': row['description'],
                            'mentee_max': int(row['mentee_max']),
                            'prereuisites': row['prereuisites'],
                            'banner_image_link': row['banner_image_link'],
                            'timeline': row['timeline'],
                            'checkpoints': row['checkpoints'],
                            'general_category': row['general_category'],
                            'banner_image': row['banner_image']
                        }
                    )

                    if created:
                        project.save()
                        print(f'new entry created for {project.title}')
                    else:
                        logger.error(f'project {project.code} already exists')

                except Exception as e:
                    logger.error(f'database error for {row['title']}: {e}')

            return Response({
                'message': 'File upload successful'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f'error: {e}')
            # print('error: ', e)
            return Response({
                'message': 'Corrupted file'
            }, status=status.HTTP_400_BAD_REQUEST)

class BasicProjectListView(generics.ListAPIView):
    permission_classes = []
    queryset = Project.objects.all()
    serializer_class = BasicProjectSerializer


# class ProjectAddView(generics.CreateAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectAdditionSerializer

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context
