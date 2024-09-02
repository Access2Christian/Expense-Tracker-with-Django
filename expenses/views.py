from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm  # Make sure this is correct

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('expense_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/add_category.html', {'form': form})

@login_required
def dashboard(request):
    total_expenses = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum']
    return render(request, 'expenses/dashboard.html', {'total_expenses': total_expenses})
