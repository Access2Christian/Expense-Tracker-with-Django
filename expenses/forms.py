from django import forms
from .models import Expense, Category

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'date', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
