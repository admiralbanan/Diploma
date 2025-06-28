from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('genre/<int:genre_id>/', views.genre_books, name='genre_books'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('add-book/', views.add_book, name='add_book'),
    path('profile/', views.profile, name='profile'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('profile/<int:user_id>/', views.other_profile, name='other_profile'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorite/add/<int:book_id>/', views.add_favorite, name='add_favorite'),
    path('favorite/remove/<int:book_id>/', views.remove_favorite, name='remove_favorite'),
    path('members/', views.members_list, name='members_list'),

    # API
    path('api/books/', views.api_books, name='api_books'),
    path('api/genres/', views.api_genres, name='api_genres'),
]
