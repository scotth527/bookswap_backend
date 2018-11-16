from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework_jwt.views import obtain_jwt_token

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   
   public=True,
   
)

urlpatterns = [
    path('users/<int:users_id>', views.UsersView.as_view(), name='id-users'),
    path('contacts/', views.ContactsView.as_view(), name='all-contacts'),
    path('login/', obtain_jwt_token)
]
