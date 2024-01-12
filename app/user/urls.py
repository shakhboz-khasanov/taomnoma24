"""
Url patterns for user app API
"""

from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='create'),
]
