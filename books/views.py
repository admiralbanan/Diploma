from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book, Genre

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Пока такого URL нет — создадим позже
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def home(request):
    return render(request, 'home.html')


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user
            book.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

def home(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, 'home.html', {'books': books, 'genres': genres, 'selected_genre': None})



def genre_books(request, genre_id):
    selected_genre = Genre.objects.get(id=genre_id)
    books = Book.objects.filter(genre=selected_genre)
    genres = Genre.objects.all()
    return render(request, 'home.html', {
        'books': books,
        'genres': genres,
        'selected_genre': selected_genre
    })


from django.db.models import Q

def search(request):
    query = request.GET.get('q')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    genres = Genre.objects.all()
    return render(request, 'home.html', {
        'books': books,
        'genres': genres,
        'selected_genre': None,
        'query': query
    })


from django.contrib.auth.decorators import login_required
from .models import Profile, Book

from .models import Profile

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    user_books = Book.objects.filter(added_by=request.user).order_by('-created_at')

    if request.method == 'POST':
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')

        if bio is not None:
            profile.bio = bio

        if avatar is not None:
            profile.avatar = avatar

        profile.save()
        return redirect('profile')

    return render(request, 'profile.html', {'profile': profile, 'user_books': user_books})



def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'book_detail.html', {'book': book})





