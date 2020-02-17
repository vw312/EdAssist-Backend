from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:q>', views.courseSearcher),
    path('nptel/<str:subjectid>', views.subjectidNptelInformation),
]
