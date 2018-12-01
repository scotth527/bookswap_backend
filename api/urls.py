from django.contrib import admin
from django.urls import path, include
from api import views
from rest_framework_jwt.views import obtain_jwt_token

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
   
#    public=True,
   
# )

urlpatterns = [
    # path('profile/<int:profile_id>', views.ProfileView.as_view(), name='id-users'),
    # path('contacts/', views.ContactsView.as_view(), name='all-contacts'),
    path('login/', obtain_jwt_token),
    #path('requests/', views.RequestsView.as_view(), name="add-request"),
    path('requests/<int:given_id>', views.RequestsView.as_view(), name='given_id'),
    path('trades/<int:given_id>', views.TradesView.as_view(), name='given_id'),
    path('books/<int:book_id>', views.BooksView.as_view(), name='books_id'),
    path('books/', views.BooksView.as_view(), name='all-books'),
    path('inv/<int:profile_id>', views.LibraryView.as_view(), name='inventory'),
    path('page/<int:book_id>', views.PageView.as_view(), name='bookpage'),
    path('library/<int:profile_id>', views.LibraryView.as_view(), name='person_library'),
    # path('library/', views.LibraryView.as_view(), name='library'),
    path('profile/<int:profile_id>', views.ProfileView.as_view(), name='profile_id')
    #path('trades/<int:profile_id>', views.TradesView.as_view(), name='trade_id')
    # path('trade/<int:profile_id>', views.TradesView.as_view(), name=''),
]
