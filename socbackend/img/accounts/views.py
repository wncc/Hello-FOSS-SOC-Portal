import re
from django.http import JsonResponse
from django.db.models import Value as V
from django.db.models.functions import Concat
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import APIException

from socbackend.settings import SIMPLE_JWT
from django.core.mail import send_mail

from .helpers import fetch_from_sso
from .models import UserProfile
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer, UserAutoCompleteSerializer, UserProfileSerializer

from projects.models import Mentee

from .options import DepartmentChoices, YearChoices
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import AnonymousUser






from django.utils.crypto import get_random_string
import os


# views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import DepartmentChoices

class DepartmentListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        departments = DepartmentChoices.choices
        return Response(departments)
    

class YearListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        years = YearChoices.choices
        return Response(years)

@api_view(['GET'])
@permission_classes([AllowAny])
def isloggedin(request):
    if isinstance(request.user, AnonymousUser):
        return JsonResponse({"status": "NO"}, status=200)
    else:
        return JsonResponse({"status": "YES"}, status=200)

def generate_verification_token():
    return get_random_string(length=32)


# def verify_email(request, token):
#     try:
#         user_profile = UserProfile.objects.get(verification_token=token)
#         user_profile.verified = True
#         user = user_profile.user
#         user.is_active = True
#         user.save()
#         user_profile.save()
#         mentee = Mentee.objects.create(user=user_profile)
#         mentee.save()


#         return JsonResponse({"success": "verified"}, status=200)
#     except UserProfile.DoesNotExist:
#         return JsonResponse({"error": "User does not exist"}, status=400)

# def send_verification_email(user_profile):
#     subject = 'SOC Menteee Registration Verification Link'
#     message = f"""
#     Hi {user_profile.name},
    
#     Please click on the link below to verify your email address and complete your registration.
    
#     {os.getenv('DOMAIN_NAME')}/verify-email/{user_profile.verification_token}
    
#     Regards,
#     Team WnCC"""
#     from_email = 'wncc@iitb.ac.in'  # Sender's email address
#     recipient_list = [user_profile.roll_number+'@iitb.ac.in']  # Recipient's email address
    
#     send_mail(subject, message, from_email, recipient_list)  
    

def logout(request):
    response = JsonResponse({"success": "logged out"}, status=200)
    response.delete_cookie(SIMPLE_JWT["AUTH_COOKIE"])
    return response


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        roll_number = request.data.get("roll_number").lower()
        password = request.data.get("password")

        if User.objects.filter(username=roll_number).exists():
            user = User.objects.get(username=roll_number)
            if UserProfile.objects.filter(user=user).exists():
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.verified:
                    return Response({"error": "User already exists"}, status=400)
                else:
                    user.delete()
            else:
                user.delete()
            
        user = User.objects.create_user(username=roll_number, password=password)
        user.is_active = False
        user.save()
        mutable_copy = request.POST.copy()
        mutable_copy["user"] = user.id
        
        serializer = RegisterUserSerializer(data=mutable_copy)

        if serializer.is_valid():
            serializer.save()
            verification_token = generate_verification_token()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.verification_token = verification_token
            user_profile.verified = True
            user = user_profile.user
            user.is_active = True
            user.save()
            user_profile.save()
            print(f"User profile: {user_profile}")
            if user_profile:
                mentee = Mentee.objects.create(user=user_profile)
                mentee.save()
            else:
                raise print("User profile does not exist.")
            
            # send_verification_email(user_profile)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)




class UserAutoCompleteView(ListAPIView):
    """
    ListAPIView to access user data, for user searching
    """

    serializer_class = UserAutoCompleteSerializer

    def get_queryset(self):
        queryset = UserProfile.objects.all()
        query = self.request.query_params.get("search")

        if query is not None and query != "":
            if re.search(r"\d", query):
                queryset = queryset.filter(user__roll_number__iexact=query)
            else:
                queryset = queryset.annotate(
                    full_name=Concat("user__first_name", V(" "), "user__last_name")
                )
                for term in query.split():
                    queryset = queryset.filter(full_name__icontains=term)

        return queryset[:10]


class CreateUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = fetch_from_sso(
                request.data["code"], "http://localhost:3000/register", request
            )
        except APIException as e:
            return Response(e.detail, status=e.status_code)

        return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        mutable_copy = request.POST.copy()
        mutable_copy["username"] = mutable_copy["username"].lower()
        response = super().post(request, *args, **kwargs)
        if "access" in response.data:
            access_token = response.data["access"]
            response.set_cookie(
                key=SIMPLE_JWT["AUTH_COOKIE"], value=access_token, httponly=True
            )
        return response
