from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('genre/<int:genre_id>/', views.genre_books, name='genre_books'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('add-book/', views.add_book, name='add_book'),
    path('search/', views.search, name='search'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),


]
