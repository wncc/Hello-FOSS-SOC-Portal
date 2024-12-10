from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.BasicProjectListView.as_view(), name="project_list"),
    path("<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("wishlist/", views.ProjectWishlist.as_view(), name="wishlist"),
    path("preference/", views.ProjectPreference.as_view(), name="preference"),
    path("upload-projects/", views.UploadProjectsView.as_view(), name="upload_projects"),  # New endpoint
    # path("add/", views.ProjectAddView.as_view(), name="project_add"),
]
