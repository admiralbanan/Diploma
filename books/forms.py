from django import forms
from .models import Book, Review

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'description', 'genre', 'cover', 'file']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ваш отзыв...'})
        }
