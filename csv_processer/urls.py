from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path("csv/upload", views.upload_csv),
    path("csv/getData", views.get_csv_data),
]
