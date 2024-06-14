from django.shortcuts import render
from datetime import date as dt
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.models import User
from mptt.templatetags.mptt_tags import cache_tree_children
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.management import call_command




class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employee_list.html'
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by.startswith('-'):
                queryset = queryset.order_by(F(sort_by[1:]).desc(nulls_last=True))
            else:
                queryset = queryset.order_by(F(sort_by).asc(nulls_last=True))
        return queryset

class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    template_name = 'employee_create.html'
    fields = ['name', 'position', 'date', 'email', 'manager']
    success_url = reverse_lazy('index')
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        managers = Employee.objects.select_related('manager').all()
        context['managers'] = managers
        return context


    
class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    template_name = 'employee_edit.html'
    form_class = EmployeeForm
    success_url = reverse_lazy('employee_list')
    login_url = '/login/'


@login_required(login_url='login')
def employee_delete(request, pk):
    Employee.objects.get(pk=pk).delete()
    return redirect(reverse('employee_list'))


@login_required(login_url='login')
def index(request):
    nodes = Employee.objects.all()
    if request.method == 'POST':
        generate_number = request.POST['generate_number']
        if generate_number:
            try:
                generate_number = int(generate_number)
                call_command('seed', generate_number)
                return redirect(reverse('index'))
            except:
                messages.error(request, "Something bad happened")
                return redirect(reverse('index'))

    return render(request, 'index.html', {'nodes': nodes})


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_2 = request.POST['password2']
        if password == password_2:
            User.objects.create_user(username=username, password=password, email='')
            return redirect('login')
        else:
            messages.warning(request, "Your password is not matching")
            return redirect('register')
    return render(request, 'register.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')