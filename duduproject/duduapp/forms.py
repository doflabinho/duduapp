from django import forms
from .models import Movie
from .models import Book
from .models import Date
from .models import DateImage
from .models import DiaryEintrag
from .models import EmbarrassingMoment
from .models import Dream
from .models import Recipe
from .models import TimeTogether, TimeEntry
from .models import Vocabulary


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'type', 'watched_date', 'watched_status', 'dudu_rating', 'bubu_rating', 'notes']
        widgets = {
            'watched_date': forms.DateInput(attrs={'type': 'date'}),  # Kalender hinzufügen
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'read', 'dudu_rating', 'bubu_rating', 'dudu_notes', 'bubu_notes']


class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ['title', 'status', 'notes', 'image_url']


class DateImageForm(forms.ModelForm):
    class Meta:
        model = DateImage
        fields = ['image']


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEintrag
        fields = ['date', 'title', 'description_dudu', 'description_bubu', 'mood_dudu', 'mood_bubu', 'photo']

class EmbarrassingMomentForm(forms.ModelForm):
    class Meta:
        model = EmbarrassingMoment
        fields = ['description', 'embarrassment_level']
        labels = {
            'description': 'description',
            'embarrassment_level': 'Embarrasment scale (1-10)',
        }

class DreamForm(forms.ModelForm):
    class Meta:
        model = Dream
        fields = ['title', 'description']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'steps', 'tried', 'rating_dudu', 'rating_bubu']

class TimeTogetherForm(forms.ModelForm):
    class Meta:
        model = TimeTogether
        fields = ['title', 'start_time', 'end_time']

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['date', 'description', 'special_notes']

class VocabularyForm(forms.ModelForm):
    class Meta:
        model = Vocabulary
        fields = ['german_word', 'portuguese_word', 'category', 'difficulty']

