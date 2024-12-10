from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import redirect

# Optional: Define a root view with a welcome message
def root_view(request):
    return HttpResponse(
        "<h1>Welcome to the Backend</h1>"
        "<p>Available endpoints:</p>"
        "<ul>"
        "<li><a href='/api/accounts/'>Accounts API</a></li>"
        "<li><a href='/api/projects/'>Projects API</a></li>"
        "</ul>"
    )

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/projects/", include("projects.urls")),
    path("", root_view, name="root"),  # Add this line for the root URL
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
