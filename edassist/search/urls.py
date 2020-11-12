from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:q>', views.course_searcher),
    path('nptel/<str:subjectid>', views.subjectid_nptel_information),
    path('nptel/<str:subjectid>/<str:youtube_video_id>', views.caption_nptel),
    path('nptel/<str:subjectid>/<str:youtube_video_id>/imp_words', views.important_words_nptel)
]
