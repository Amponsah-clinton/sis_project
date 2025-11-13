from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('browse/', views.browse, name='browse'),
    path('submit/', views.submit, name='submit'),
    path('about/', views.about, name='about'),
    path('auth/', views.auth, name='auth'),
    path('indexed_articles/', views.indexed_articles, name='indexed_articles'),
    path('indexed_journals/', views.indexed_journals, name='indexed_journals'),
    path('project_archive/', views.project_archive, name='project_archive'),
    path('upload_article/', views.upload_article, name='upload_article'),
    path('register_journal/', views.register_journal, name='register_journal'),
    path('directory_researchers/', views.directory_researchers, name='directory_researchers'),
    path('upload_project/', views.upload_project, name='upload_project'),
    path('council_members/', views.council_members, name='council_members'),
    path('team_members/', views.team_members, name='team_members'),
    path('sponsors/', views.sponsors, name='sponsors'),
    path('request_membership/', views.request_membership, name='request_membership'),
    path('apply_directory/', views.apply_directory, name='apply_directory'),
    path('hall_of_fame/', views.hall_of_fame, name='hall_of_fame'),
    path('hall_of_fame/apply/', views.hall_of_fame_apply, name='hall_of_fame_apply'),
    path('check_turnitin/', views.check_turnitin, name='check_turnitin'),
    path('work_plagiarism/', views.work_plagiarism, name='work_plagiarism'),
    path('thesis_to_article/', views.thesis_to_article, name='thesis_to_article'),
    path('thesis_to_book/', views.thesis_to_book, name='thesis_to_book'),
    path('thesis_to_book_chapter/', views.thesis_to_book_chapter, name='thesis_to_book_chapter'),
    path('powerpoint_preparation/', views.powerpoint_preparation, name='powerpoint_preparation'),
]

