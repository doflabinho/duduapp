from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('introduction/', views.introduction, name='introduction'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/<int:id>/edit/', views.edit_movie, name='edit_movie'),
    path('movies/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('book_list/', views.book_list, name='book_list'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('books/edit/<int:id>/', views.edit_book, name='edit_book'),
    path('date_list/', views.date_list, name='date_list'),
    path('add/', views.date_add, name='date_add'),
    path('date/<int:date_id>/', views.date_detail, name='date_detail'),
    path('images/delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('date/<int:date_id>/edit/', views.edit_date, name='edit_date'),
    path('date/<int:date_id>/add_dateimages/', views.add_dateimages, name='add_dateimages'),
    path('date/<int:date_id>/delete/', views.delete_date, name='delete_date'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar_by_month'),
    path('diary/edit/<int:entry_id>/', views.edit_diary_entry, name='edit_diary_entry'),
    path('add_entry/str:<date>/', views.add_diary_entry, name='add_diary_entry'),
    path('diary/<str:date>/', views.view_diary_entries, name='view_diary_entries'),
    path('moments/', views.embarrassing_moments_list, name='embarrassing_moments_list'),
    path('moments/add/', views.add_embarrassing_moment, name='add_embarrassing_moment'),
    path('moments/delete/<int:pk>/', views.delete_embarrassing_moment, name='delete_moment'),
    path('dreams/', views.dream_list, name='dream_list'),
    path('dreams/add/', views.add_dream, name='add_dream'),
    path('dreams/edit/<int:dream_id>/', views.edit_dream, name='edit_dream'),
    path('dreams/delete/<int:dream_id>/', views.delete_dream, name='delete_dream'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('recipes/add/', views.add_recipe, name='add_recipe'),
    path('recipes/edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('recipes/delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('time-together/', views.time_together_list, name='time_together_list'),
    path('time-together/<int:pk>/', views.time_together_detail, name='time_together_detail'),
    path('add_time_together/', views.add_time_together, name='add_time_together'),
    path('delete_time_together/<int:pk>/', views.delete_time_together, name='delete_time_together'),
    path('add_time_together_entry/<int:pk>/', views.add_time_together_entry, name='add_time_together_entry'),  # Neue URL für das Hinzufügen von Einträgen
    path('delete_time_together_entry/<int:pk>/', views.delete_time_together_entry, name='delete_time_together_entry'),
    path('time_together_entry/edit/<int:pk>/', views.edit_time_together_entry, name='edit_time_together_entry'),
    path('vocabularies/', views.vocabulary_list, name='vocabulary_list'),
    path('vocabularies/add/', views.add_vocabulary, name='add_vocabulary'),
    path('vocabularies/edit/<int:pk>/', views.edit_vocabulary, name='edit_vocabulary'),
    path('vocabularies/delete/<int:pk>/', views.delete_vocabulary, name='delete_vocabulary'),
    path('quiz/', views.quiz_mode, name='quiz_mode'),
    path('quiz/check/', views.check_answer, name='check_answer'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)