from django import forms

from .models import Recipe, Entry

class RecipeForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ['text']
		labels = {'text':''}

class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text': ''}
		widgets = {'text': forms.Textarea(attrs={'cols': 80})}