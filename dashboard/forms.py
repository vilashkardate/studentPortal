from django import forms
from .models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject','title','description','due','is_finished']
        widgets = {
            'due':DateInput()
        }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length =  100,label = 'Enter your search : ')


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']