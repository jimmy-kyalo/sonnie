"""Defines URL patterns for sonnie_app."""

from django.urls import path

from . import views

app_name = 'sonnie_app'
urlpatterns = [
	# home page
	path('', views.index, name='index'),

	# show all recipes
	path('recipes/', views.recipes, name='recipes'),

	# detail page for a single topic
	path('recipes/<int:recipe_id>', views.recipe, name='recipe'),

	# page for adding a new topic
	path('new_recipe/', views.new_recipe, name='new_recipe'),

	# page for adding a new entry
	path('new_entry/<int:recipe_id>', views.new_entry, name='new_entry'),

	# page for editing an entry
	path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
	
]