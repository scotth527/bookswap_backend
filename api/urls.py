from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('contacts/<int:contact_id>', views.ContactsView.as_view(), name='id-contacts'),
    path('contacts/', views.ContactsView.as_view(), name='all-contacts'),
    path('login/', obtain_jwt_token)
]
