from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.custom_auth import CookieJWTAuthentication
from accounts.models import UserProfile
from .models import Mentee, Project, MenteePreference, MenteeWishlist
from .serializers import (
    ProjectSerializer,
    BasicProjectSerializer,
    MenteePreferenceSerializer,
    MenteePreferenceSaveSerializer,
)
from projects.management.commands.upload_projects import upload_projects
import logging

logger = logging.getLogger(__name__)

class ProjectDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectSerializer

    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            serializer = self.serializer_class(project)
            return Response(serializer.data)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)


class ProjectWishlist(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            preferences = MenteeWishlist.objects.filter(mentee=mentee)
            project_objects = [preference.project for preference in preferences]
            serializer = BasicProjectSerializer(project_objects, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching wishlist: {e}")
            return Response({"error": "Failed to fetch wishlist"}, status=500)

    def post(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            project_id = request.data["project_id"]
            project = Project.objects.get(pk=project_id)
            preference = MenteeWishlist(mentee=mentee, project=project)
            preference.save()
            return Response({"message": "Project added to wishlist."})
        except Exception as e:
            logger.error(f"Error adding to wishlist: {e}")
            return Response({"error": "Failed to add project to wishlist"}, status=500)

    def delete(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            project_id = request.GET.get("project_id")
            project = Project.objects.get(pk=project_id)
            preference = MenteeWishlist.objects.get(mentee=mentee, project=project)
            preference.delete()
            return Response({"message": "Project removed from wishlist."})
        except Exception as e:
            logger.error(f"Error removing from wishlist: {e}")
            return Response({"error": "Failed to remove project from wishlist"}, status=500)


class ProjectPreference(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            preferences = MenteePreference.objects.filter(mentee=mentee)
            serializer = MenteePreferenceSerializer(preferences, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching preferences: {e}")
            return Response({"error": "Failed to fetch preferences"}, status=500)

    def post(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            project_id = request.data["project"]
            preference = request.data["preference"]
            sop = request.data["sop"]
            project = Project.objects.get(pk=project_id)
            serializer = MenteePreferenceSaveSerializer(
                data={
                    "mentee": mentee.id,
                    "project": project.id,
                    "preference": preference,
                    "sop": sop,
                }
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Error adding preference: {e}")
            return Response({"error": "Failed to add preference"}, status=500)

    def delete(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            mentee = Mentee.objects.get(user=user_profile)
            project_id = request.data["project_id"]
            project = Project.objects.get(pk=project_id)
            preference = MenteePreference.objects.get(mentee=mentee, project=project)
            preference.delete()
            return Response({"message": "Project removed from preferences."})
        except Exception as e:
            logger.error(f"Error removing preference: {e}")
            return Response({"error": "Failed to remove preference"}, status=500)


class BasicProjectListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = BasicProjectSerializer


class UploadProjectsView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            csv_path = request.data.get("csv_path", "./projects.csv")
            upload_projects(csv_path)
            return Response({"message": "Projects uploaded successfully."})
        except Exception as e:
            logger.error(f"Error uploading projects: {e}")
            return Response({"error": str(e)}, status=500)
