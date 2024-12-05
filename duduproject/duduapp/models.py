from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Movie(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('tv-show', 'TV Show'),
    ]
    title = models.CharField(max_length=255)
    watched_date = models.DateField()
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='movie')  # Neue Spalte für Typ
    watched_status = models.BooleanField(default=False)
    dudu_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # Wert zwischen 0 und 10
    bubu_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # Wert zwischen 0 und 10
    notes = models.TextField(blank=True)


    def __str__(self):
        self.title

class Book(models.Model):
    title = models.CharField(max_length=255)
    read = models.BooleanField(default=False)  # Gelesen oder nicht
    dudu_rating = models.IntegerField(default=0)  # Dudu-Rating (0-10)
    bubu_rating = models.IntegerField(default=0)  # Bubu-Rating (0-10)
    dudu_notes = models.TextField(blank=True, null=True)  # Notizen Dudu
    bubu_notes = models.TextField(blank=True, null=True)  # Notizen Bubu

    def __str__(self):
        return self.title

class Date(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[('not yet', 'Not yet'), ('we did', 'We did')])
    notes = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class DateImage(models.Model):
    title = models.CharField(max_length=100)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='date_images/')  # Speicherort der Bilder

    def __str__(self):
        return self.title

class DiaryEintrag(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=200)
    description_dudu = models.TextField()
    description_bubu = models.TextField()
    mood_dudu = models.CharField(max_length=50)
    mood_bubu = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='diary_photos/', blank=True, null=True)  # Neues Feld für Fotos

class EmbarrassingMoment(models.Model):
    description = models.TextField()
    embarrassment_level = models.PositiveSmallIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"{self.description[:50]} - Peinlichkeitsstufe {self.embarrassment_level}"

class Dream(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text="List of ingredients")
    steps = models.TextField(help_text="Steps for cooking/baking")
    tried = models.BooleanField(default=False)
    rating_dudu = models.PositiveIntegerField(null=True, blank=True)
    rating_bubu = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class TimeTogether(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateField()
    end_time = models.DateField()

    def __str__(self):
        return self.title

class TimeEntry(models.Model):
    time_together = models.ForeignKey(TimeTogether, related_name='entries', on_delete=models.CASCADE)
    date = models.DateField()  # Das Datum des Eintrags
    description = models.TextField()
    special_notes = models.TextField()

    def __str__(self):
        return f"Entry on {self.date} for {self.time_together.title}"


class Vocabulary(models.Model):
    german_word = models.CharField(max_length=100, verbose_name="german word")
    portuguese_word = models.CharField(max_length=100, verbose_name="portuguese word")
    category = models.CharField(max_length=50, verbose_name="category", null=True, blank=True)
    difficulty = models.IntegerField(verbose_name="difficulty", choices=[(1, 'easy'), (2, 'medium'), (3, 'hard')], default=1)

    def __str__(self):
        return f"{self.german_word} - {self.portuguese_word}"