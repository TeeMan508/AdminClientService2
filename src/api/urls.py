from django.urls import path

from .views import *

app_name = 'admin_client_service_api'

urlpatterns = [
    path("django_api", MainView.as_view()),

]
