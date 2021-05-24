from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import *


# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password1, email=email)
                    user.save()
                    messages.info(request, 'Account created successfully')
                    return redirect('login')
            else:
                messages.info(request, 'Password not matching....')
                return redirect('register')

        else:
            return render(request, 'register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid credentials!!')
                return redirect('login')

        else:
            return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(user=user)
        form = TaskForm(request.POST)

        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                todo = form.save(commit=False)
                todo.user = user
                todo.save()
                print(todo)
            return redirect("/")

        context = {'tasks': tasks, 'form': form}
        return render(request, 'list.html', context)


@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = UpdateForm(instance=task)

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'update_task.html', context)


@login_required(login_url='login')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {'item': item}
    return render(request, 'delete.html', context)


def logout(request):
    auth.logout(request)
    return redirect('login')


