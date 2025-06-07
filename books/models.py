from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField("Название жанра", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Название книги", max_length=200)
    author = models.CharField("Автор", max_length=200)
    year = models.IntegerField("Год издания")
    description = models.TextField("Описание")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, verbose_name="Жанр")
    cover = models.ImageField("Обложка", upload_to='covers/')
    file = models.FileField("Файл книги", upload_to='books/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Добавлено пользователем")
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Профиль {self.user.username}"
    


from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

