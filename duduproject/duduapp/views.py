from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm
from .models import Book
from .forms import BookForm
from .models import Date, DateImage
from .forms import DateForm
from .forms import DateImageForm
import random
from django.db import models
from calendar import HTMLCalendar
from datetime import date, datetime, timedelta, timezone
from django.utils.safestring import mark_safe
from .models import DiaryEintrag
from .forms import DiaryEntryForm
from collections import defaultdict
from .models import EmbarrassingMoment
from .forms import EmbarrassingMomentForm
from .models import Dream
from .forms import DreamForm
from .models import Recipe
from .forms import RecipeForm
from .models import TimeTogether, TimeEntry
from .forms import TimeEntryForm, TimeTogetherForm
from django.http import Http404
from .models import Vocabulary
from .forms import VocabularyForm
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.
def home(request):
    return render( request, 'home.html')

def introduction(request):
    return render(request, 'introduction.html')

def movie_list(request):
    # Hol dir alle Filme aus der Datenbank
    movies = Movie.objects.all()
    
    # Filtern nach Titel, falls ein Suchbegriff im GET-Parameter 'title' angegeben ist
    title_query = request.GET.get('title')
    if title_query:
        movies = movies.filter(title__icontains=title_query)  # Filter nach Teilstring im Titel
    
    # Filtern nach "Watched"-Status, falls im GET-Parameter 'watched' ein Wert gesetzt ist
    watched_status = request.GET.get('watched')
    if watched_status == 'watched':
        movies = movies.filter(watched_status=True)  # Nur Filme anzeigen, die als "Watched" markiert sind
    elif watched_status == 'not_watched':
        movies = movies.filter(watched_status=False)  # Nur Filme anzeigen, die noch nicht "Watched" sind

    # Filtern nach Typ (Movie oder TV-Show)
    type_query = request.GET.get('type')
    if type_query:
        movies = movies.filter(type=type_query)    

    return render(request, 'movie_list.html', {'movies': movies})

def book_list(request):
    books = Book.objects.all()

    # Filter nach Titel
    title_search = request.GET.get('title_search')
    if title_search:
        books = books.filter(title__icontains=title_search)

    # Filter nach Gelesen/Nicht gelesen
    filter_option = request.GET.get('filter')
    if filter_option == 'read':
        books = books.filter(read=True)
    elif filter_option == 'unread':
        books = books.filter(read=False)

    return render(request, 'book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Nach dem Hinzufügen wird zur Buchliste weitergeleitet
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Nach dem Löschen wird zur Buchliste weitergeleitet
    return render(request, 'delete_book.html', {'book': book})

def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Liste der Bücher
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})

def edit_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

def delete_movie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})


# datechecklist
def date_list(request):
    dates = Date.objects.all()
    for date in dates:
        images = date.images.all()  # Alle Bilder, die dem Date zugeordnet sind
        if images:
            date.random_image = random.choice(images)  # Zufälliges Bild auswählen
        else:
            date.random_image = None  # Falls keine Bilder vorhanden sind
    return render(request, 'date_list.html', {'dates': dates})

def date_add(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('date_list')
    else:
        form = DateForm()
    return render(request, 'date_form.html', {'form': form})

def date_detail(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    
    if request.method == 'POST':
        image_form = DateImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.date = date
            new_image.save()
            return redirect('date_detail', date_id=date_id)
    else:
        image_form = DateImageForm()

    images = date.images.all()  # Alle Bilder für dieses Date abrufen
    return render(request, 'date_detail.html', {'date': date, 'images': images, 'image_form': image_form})

def delete_image(request, image_id):
    image = get_object_or_404(DateImage, id=image_id)
    if request.method == 'POST':
        image.delete()
        return redirect(request.META.get('HTTP_REFERER', 'date_list'))  # Zurück zur vorherigen Seite

def edit_date(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    if request.method == 'POST':
        date_form = DateForm(request.POST, instance=date)
        image_form = DateImageForm(request.POST, request.FILES)

        if date_form.is_valid():
            date_form.save()
            return redirect('date_detail', date_id=date.id)

    else:
        date_form = DateForm(instance=date)
        image_form = DateImageForm()

    return render(request, 'edit_date.html', {
        'date_form': date_form,
        'image_form': image_form,
        'date': date,
        'images': date.images.all(),
    })

def add_dateimages(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    if request.method == 'POST':
        image_form = DateImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            date_image = image_form.save(commit=False)
            date_image.date = date  # Hier wird das Bild dem entsprechenden Date-Eintrag zugeordnet
            date_image.save()
            return redirect('add_dateimages', date_id=date.id)  # Um zurück zur Bilder-Seite zu navigieren
    else:
        image_form = DateImageForm()

    images = date.images.all()  # Alle Bilder, die diesem Date-Eintrag zugeordnet sind
    return render(request, 'add_dateimages.html', {
        'image_form': image_form,
        'date': date,
        'images': images,
    })


def delete_date(request, date_id):
    date = get_object_or_404(Date, id=date_id)
    date.delete()  # Löschen des Date-Eintrags
    return redirect('date_list')  # Nach dem Löschen zur Date-Liste umleiten

#Calendar
def calendar_view(request, year=None, month=None):
    # Setze Jahr und Monat auf das aktuelle Datum, wenn keine Parameter vorhanden sind
    if year is None or month is None:
        d = datetime.today()
        year = d.year
        month = d.month
    else:
        # Stelle sicher, dass Jahr und Monat ganze Zahlen sind
        try:
            year = int(year)
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("Monat muss zwischen 1 und 12 liegen.")
        except (ValueError, TypeError):
            d = datetime.today()
            year = d.year
            month = d.month

    # Kalender erstellen und Größe der Zellen anpassen
    cal = HTMLCalendar()
    html_calendar = cal.formatmonth(year, month, withyear=True)
    html_calendar = html_calendar.replace('<td ', '<td width="150" height="150"')

    # Navigation for previous and next month
    if month == 1:
        prev_month = datetime(year - 1, 12, 1)  # December of the previous year
    else:
        prev_month = datetime(year, month - 1, 1)  # Previous month

    if month == 12:
        next_month = datetime(year + 1, 1, 1)  # January of the next year
    else:
        next_month = datetime(year, month + 1, 1)  # Next month
    
    # Holen der Tagebucheinträge für den gegebenen Monat
    diary_entries = DiaryEintrag.objects.filter(date__year=year, date__month=month)
    

    # Kalender-HTML an das Template übergeben
    context = {
        'calendar': mark_safe(html_calendar),
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'next_month': next_month,
        'diary_entries': diary_entries,
    }
    return render(request, 'calendar_view.html', context)


def add_diary_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('calendar_view')  # Redirect zur Kalenderansicht
    else:
        date = request.GET.get('date')
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').date()  # Datumsformat anpassen
        else:
            date = None
        form = DiaryEntryForm(initial={'date': date})  # Setze das initiale Datum
    return render(request, 'add_diary_entry.html', {'form': form})


def edit_diary_entry(request, entry_id):
    diary_entry = get_object_or_404(DiaryEintrag, id=entry_id)

    if request.method == "POST":
        form = DiaryEntryForm(request.POST, request.FILES, instance=diary_entry)
        if form.is_valid():
            form.save()
            return redirect('calendar_view')  # Oder eine andere Seite, auf die du umleiten möchtest
    else:
        form = DiaryEntryForm(instance=diary_entry)

    context = {
        'form': form,
        'entry': diary_entry,
    }
    return render(request, 'edit_diary_entry.html', context)

def view_diary_entries(request, date):
    entries = DiaryEntry.objects.filter(date=date)
    return render(request, 'view_diary_entries.html', {'entries': entries})


def embarrassing_moments_list(request):
    moments = EmbarrassingMoment.objects.all()
    return render(request, 'embarrassing_moments_list.html', {'moments': moments})

def add_embarrassing_moment(request):
    if request.method == 'POST':
        form = EmbarrassingMomentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('embarrassing_moments_list')
    else:
        form = EmbarrassingMomentForm()
    return render(request, 'add_embarrassing_moment.html', {'form': form})

def delete_embarrassing_moment(request, pk):
    # Hole das Moment anhand der Primärschlüssel-ID (pk)
    moment = get_object_or_404(EmbarrassingMoment, pk=pk)

    if request.method == 'POST':
        moment.delete()
        return redirect('embarrasing_moments_list')  # Weiterleitung zur Momentenliste nach dem Löschen

    return render(request, 'confirm_delete.html', {'moment': moment})

def dream_list(request):
    dreams = Dream.objects.all()
    return render(request, 'dream_list.html', {'dreams': dreams})

def add_dream(request):
    if request.method == 'POST':
        form = DreamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dream_list')
    else:
        form = DreamForm()
    return render(request, 'add_dream.html', {'form': form})

def edit_dream(request, dream_id):
    dream = get_object_or_404(Dream, id=dream_id)
    if request.method == 'POST':
        form = DreamForm(request.POST, instance=dream)
        if form.is_valid():
            form.save()
            return redirect('dream_list')
    else:
        form = DreamForm(instance=dream)
    return render(request, 'edit_dream.html', {'form': form, 'dream': dream})

def delete_dream(request, dream_id):
    dream = get_object_or_404(Dream, id=dream_id)
    if request.method == 'POST':
        dream.delete()
        return redirect('dream_list')
    return render(request, 'delete_dream.html', {'dream': dream})


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_list.html', {'recipes': recipes})

def view_recipe(request, recipe_id):
    # Retrieve the recipe by its ID
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    # Split the ingredients and steps fields if they exist
    ingredients_list = recipe.ingredients.split(";") if recipe.ingredients else []
    steps_list = recipe.steps.split(".") if recipe.steps else []
    
    # Pass the recipe and the lists to the template
    context = {
        'recipe': recipe,
        'ingredients_list': ingredients_list,
        'steps_list': steps_list,
    }
    return render(request, 'recipe_detail.html', context)

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'add_recipe.html', {'form': form})

def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe})

def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect('recipe_list')

# View für die Übersicht aller gemeinsamen Zeiten
def time_together_list(request):
    time_togethers = TimeTogether.objects.all()
    return render(request, 'time_together_list.html', {'time_togethers': time_togethers})

# Detailansicht für eine bestimmte Zeit zusammen
def time_together_detail(request, pk):
    time_together = get_object_or_404(TimeTogether, pk=pk)
    
    # Hole alle Einträge für das spezifische TimeTogether-Objekt
    entries = TimeEntry.objects.filter(time_together=time_together)
    
    return render(request, 'time_together_detail.html', {
        'time_together': time_together,
        'entries': entries,
    })

# View zum Hinzufügen einer neuen TimeTogether
def add_time_together(request):
    if request.method == 'POST':
        form = TimeTogetherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time_together_list')  # Weiterleitung zur Liste der TimeTogethers
    else:
        form = TimeTogetherForm()

    return render(request, 'add_time_together.html', {'form': form})

def delete_time_together(request, pk):
    time_together = get_object_or_404(TimeTogether, pk=pk)

    if request.method == "POST":
        # Wenn der Benutzer die Bestätigung abgesendet hat, löschen wir den Eintrag
        time_together.delete()
        return redirect('time_together_list')  # Zur Liste der Einträge zurückkehren

    return render(request, 'delete_time_together.html', {'time_together': time_together})

def add_time_together_entry(request, pk):
    time_together = get_object_or_404(TimeTogether, pk=pk)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            # Speichern des neuen Eintrags
            new_entry = form.save(commit=False)
            new_entry.time_together = time_together
            new_entry.save()
            return redirect('time_together_detail', pk=time_together.pk)
    else:
        form = TimeEntryForm()
    
    return render(request, 'add_time_together_entry.html', {'form': form, 'time_together': time_together})

def delete_time_together_entry(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    entry.delete()
    return redirect('time_together_detail', pk=entry.time_together.pk)

def edit_time_together_entry(request, pk):
    entry = get_object_or_404(TimeEntry, pk=pk)
    
    if request.method == 'POST':
        form = TimeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('time_together_detail', pk=entry.time_together.pk)  # Nach der Bearbeitung zurück zur Detailansicht
    else:
        form = TimeEntryForm(instance=entry)
    
    return render(request, 'edit_time_together_entry.html', {'form': form, 'entry': entry})

def vocabulary_list(request):
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    
    vocabularies = Vocabulary.objects.all()
    
    # Filtern nach deutschem oder portugiesischem Wort
    if query:
        vocabularies = vocabularies.filter(
            german_word__icontains=query
        ) | vocabularies.filter(
            portuguese_word__icontains=query
        )

    # Filtern nach Kategorie
    if category:
        vocabularies = vocabularies.filter(category=category)

    # Alle verfügbaren Kategorien abrufen (falls du eine feste Kategorie-Auswahl benötigst)
    categories = Vocabulary.objects.values_list('category', flat=True).distinct()

    return render(request, 'vocabulary_list.html', {
        'vocabularies': vocabularies,
        'query': query,
        'categories': categories,
        'selected_category': category,
    })

def add_vocabulary(request):
    if request.method == 'POST':
        form = VocabularyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vocabulary_list')
    else:
        form = VocabularyForm()
    return render(request, 'add_vocabulary.html', {'form': form})

def edit_vocabulary(request, pk):
    vocabulary = Vocabulary.objects.get(pk=pk)
    if request.method == 'POST':
        form = VocabularyForm(request.POST, instance=vocabulary)
        if form.is_valid():
            form.save()
            return redirect('vocabulary_list')
    else:
        form = VocabularyForm(instance=vocabulary)
    return render(request, 'edit_vocabulary.html', {'form': form, 'vocabulary': vocabulary})

def delete_vocabulary(request, pk):
    vocabulary = get_object_or_404(Vocabulary, pk=pk)

    if request.method == 'POST':
        vocabulary.delete()  # Lösche das Vokabel
        return HttpResponseRedirect(reverse('vocabulary_list'))  # Weiterleitung zur Vokabelliste

    return render(request, 'vocabulary_confirm_delete.html', {'vocabulary': vocabulary})

def quiz_mode(request):
    # Lade die erste Vokabel oder die nächste Vokabel
    vocab = Vocabulary.objects.first()  # Beispiel: Erster Eintrag

    # Falls keine Vokabeln vorhanden sind, gebe eine Fehlermeldung aus
    if not vocab:
        return render(request, 'quiz_mode.html', {'message': 'Keine Vokabeln verfügbar'})

    return render(request, 'quiz_mode.html', {'vocab': vocab})

def check_answer(request):
    if request.method == 'POST':
        vocab_id = request.POST.get('vocab_id')
        user_answer = request.POST.get('user_answer')

        try:
            vocab = Vocabulary.objects.get(id=vocab_id)
        except Vocabulary.DoesNotExist:
            raise Http404("Vokabel nicht gefunden")

        correct_answer = vocab.portuguese_word  # Beispiel: Die richtige Antwort in Portugiesisch

        # Überprüfen, ob die Antwort korrekt ist
        if user_answer.lower() == correct_answer.lower():
            result = "Correct, Sir!"
        else:
            result = "Wrong, Sir"

        # Weiterleitung zur nächsten Vokabel (du kannst die Logik hier erweitern)
        next_vocab = Vocabulary.objects.exclude(id=vocab.id).first()  # Beispiel: Nächste Vokabel

        return render(request, 'quiz_mode.html', {'result': result, 'vocab': next_vocab})

    return redirect('quiz')  # Falls kein POST, zurück zur Quiz-Seite