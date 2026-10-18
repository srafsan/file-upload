from django.urls import path

from quickstart import views

urlpatterns = [
    path(f"v1/application/", views.ApplicationView.as_view(), name='application'),
]