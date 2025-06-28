from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Жанр")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год выпуска")
    description = models.TextField(verbose_name="Описание")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Обложка")
    file = models.FileField(upload_to='books/', verbose_name="Файл книги")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Добавил")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Профиль {self.user.username}'

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Книга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Текст отзыва")
    stars = models.PositiveSmallIntegerField(default=0, verbose_name="Оценка (звёзды)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f'Отзыв от {self.user.username} к "{self.book.title}"'

class ReviewComment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
