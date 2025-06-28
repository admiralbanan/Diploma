from rest_framework import serializers
from .models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'author',
            'year',
            'description',
            'genre',
            'created_at'
        ]
