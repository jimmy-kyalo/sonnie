from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Recipe, Entry
from .forms import RecipeForm, EntryForm

def index(request):
	"""The home page for learning log"""
	return render(request, 'sonnie_app/index.html')

@login_required
def recipes(request):
	# show all topics
	recipes = Recipe.objects.filter(owner=request.user).order_by('date_added')
	context = {'recipes': recipes}
	return render(request, 'sonnie_app/recipes.html', context)

@login_required
def recipe(request, recipe_id):
	# show a single topic and all its entries
	recipe = Recipe.objects.get(id=recipe_id)
	if recipe.owner != request.user:
		raise Http404
	entries = recipe.entry_set.order_by('-date_added')
	context = {'recipe': recipe, 'entries': entries}
	return render(request, 'sonnie_app/recipe.html', context)

@login_required
def new_recipe(request):
	# add a new topic
	if request.method != 'POST':
		# no data submitted, create blank form
		form = RecipeForm()
	else:
		# POST data submitted, process data
		form = RecipeForm(request.POST)
		if form.is_valid():
			new_recipe = form.save(commit=False)
			new_recipe.owner = request.user
			new_recipe.save()
			return HttpResponseRedirect(reverse('sonnie_app:recipes'))

	context = {'form': form}
	return render(request, 'sonnie_app/new_recipe.html', context)

@login_required
def new_entry(request, recipe_id):
	# add new entry for a particular topic
	recipe = Recipe.objects.get(id=recipe_id)

	if request.method != 'POST':
		# no data submitted , create blank form
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.recipe = recipe
			new_entry.save()
			return HttpResponseRedirect(reverse('sonnie_app:recipe', args=[recipe_id]))

	context = {'recipe': recipe, 'form': form}
	return render(request, 'sonnie_app/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	# add new entry for a particular topic
	entry = Entry.objects.get(id=entry_id)
	recipe = entry.recipe
	if recipe.owner != request.user:
		raise Http404

	if request.method != 'POST':
		# initial request, pre-fill form with current entry
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('sonnie_app:recipe', args=[recipe.id]))

	context = {'entry': entry,'recipe': recipe, 'form': form}
	return render(request, 'sonnie_app/edit_entry.html', context)