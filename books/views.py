from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .forms import BookForm, ReviewForm
from .models import Book, Genre, Profile, Favorite
from .serializers import BookSerializer, GenreSerializer
from .models import Book, Genre, Profile, Review, ReviewComment, ReviewLike, Favorite

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    books = Book.objects.all()
    genres = Genre.objects.all()

    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    genre_id = request.GET.get('genre', '')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    sort = request.GET.get('sort', '')
    date_filter = request.GET.get('date_filter', '')

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre_id:
        books = books.filter(genre_id=genre_id)
    if year_from:
        books = books.filter(year__gte=year_from)
    if year_to:
        books = books.filter(year__lte=year_to)
    if date_filter in ['7', '30', '90']:
        days = int(date_filter)
        date_limit = datetime.now() - timedelta(days=days)
        books = books.filter(created_at__gte=date_limit)
    if sort in ['year', 'created_at', 'title']:
        books = books.order_by(sort)

    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Добавляем атрибут is_favorited
    if request.user.is_authenticated:
        favorites = set(Favorite.objects.filter(user=request.user, book__in=page_obj).values_list('book_id', flat=True))
        for book in page_obj:
            book.is_favorited = book.id in favorites
    else:
        for book in page_obj:
            book.is_favorited = False

    genre_stats = {genre.name: Book.objects.filter(genre=genre).count() for genre in genres}
    total_books = Book.objects.count()

    return render(request, 'home.html', {
        'books': page_obj,
        'genres': genres,
        'selected_genre': None,
        'books_count': paginator.count,
        'current_sort': sort,
        'page_obj': page_obj,
        'genre_stats': genre_stats,
        'total_books': total_books
    })

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

def genre_books(request, genre_id):
    selected_genre = Genre.objects.get(id=genre_id)
    books = Book.objects.filter(genre=selected_genre)
    genres = Genre.objects.all()

    paginator = Paginator(books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'books': page_obj,
        'genres': genres,
        'selected_genre': selected_genre,
        'books_count': paginator.count,
        'current_sort': '',
        'page_obj': page_obj
    })

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    user_books = Book.objects.filter(added_by=request.user).order_by('-created_at')

    if request.method == 'POST':
        bio = request.POST.get('bio', '')
        avatar = request.FILES.get('avatar')

        profile.bio = bio
        if avatar:
            profile.avatar = avatar
        profile.save()

        return redirect('profile')

    return render(request, 'profile.html', {
        'profile': profile,
        'user_books': user_books,
        'user_books_count': user_books.count()
    })

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews,
        'form': form
    })

@api_view(['GET'])
def api_books(request):
    books = Book.objects.all()

    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    genre_id = request.GET.get('genre', '')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    date_filter = request.GET.get('date_filter', '')

    if title:
        books = books.filter(title__icontains=title)
    if author:
        books = books.filter(author__icontains=author)
    if genre_id:
        books = books.filter(genre_id=genre_id)
    if year_from:
        books = books.filter(year__gte=year_from)
    if year_to:
        books = books.filter(year__lte=year_to)
    if date_filter in ['7', '30', '90']:
        days = int(date_filter)
        date_limit = datetime.now() - timedelta(days=days)
        books = books.filter(created_at__gte=date_limit)

    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def api_genres(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

def other_profile(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    books = Book.objects.filter(added_by=other_user).order_by('-created_at')
    return render(request, 'profile_other.html', {
        'other_user': other_user,
        'books': books
    })

@login_required
def add_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Favorite.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f'Книга "{book.title}" добавлена в избранное.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Favorite.objects.filter(user=request.user, book=book).delete()
    messages.success(request, f'Книга "{book.title}" удалена из избранного.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book')
    return render(request, 'favorites.html', {'favorites': favorites})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    # Подготовка атрибутов для звёзд и лайков
    for review in reviews:
        review.star_range = range(review.stars)
        review.empty_star_range = range(5 - review.stars)
        review.likes_count = review.likes.filter(is_like=True).count()
        review.dislikes_count = review.likes.filter(is_like=False).count()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'review_text' in request.POST:
            text = request.POST.get('review_text')
            stars = int(request.POST.get('stars', 0))
            Review.objects.create(book=book, user=request.user, text=text, stars=stars)
            return redirect('book_detail', book_id=book.id)
        elif 'comment_text' in request.POST:
            review_id = request.POST.get('review_id')
            review = get_object_or_404(Review, id=review_id)
            ReviewComment.objects.create(review=review, user=request.user, text=request.POST.get('comment_text'))
            return redirect('book_detail', book_id=book.id)
        elif 'like' in request.POST or 'dislike' in request.POST:
            review_id = request.POST.get('review_id')
            is_like = 'like' in request.POST
            review = get_object_or_404(Review, id=review_id)
            like_obj, created = ReviewLike.objects.get_or_create(
                review=review, user=request.user,
                defaults={'is_like': is_like}
            )
            if not created:
                like_obj.is_like = is_like
                like_obj.save()
            return redirect('book_detail', book_id=book.id)

    return render(request, 'book_detail.html', {
        'book': book,
        'reviews': reviews
    })


from django.contrib.auth.models import User
from django.db.models import Count

def members_list(request):
    members = User.objects.annotate(book_count=Count('book')).order_by('date_joined')
    return render(request, 'members.html', {'members': members})
