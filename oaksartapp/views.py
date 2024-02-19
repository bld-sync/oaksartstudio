from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from .models import Profile
from django.db.models import Count, Q
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'oaksartapp/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()
            profile = Profile.objects.create(user=current_user)
            return redirect('my-login')
    context = {'form': form}

    return render(request, 'oaksartapp/register.html', context=context)


def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid Login')

    context = {'form': form}
    return render(request, 'oaksartapp/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect('')


@login_required(login_url='my-login')
def dashboard(request):
    profile_pic = Profile.objects.get(user=request.user)

    context = {'profilePic': profile_pic}
    return render(request, 'oaksartapp/dashboard.html', context=context)


@login_required(login_url='my-login')
def profile_management(request):
    # prepopulated fields
    user_form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.get(user=request.user)
    # profile_form = UpdateProfilePicForm(instance=profile)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        # profile_form = UpdateProfilePicForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')
        # if profile_form.is_valid():
        #     profile_form.save()
        #     return redirect('dashboard')

    # context = {'user_form': user_form, 'profile_form': profile_form}
    context = {'user_form': user_form, }
    return render(request, 'oaksartapp/profile-management.html', context=context)


@login_required(login_url='my-login')
def delete_account(request):
    if request.method == 'POST':
        delete_user = User.objects.get(username=request.user)
        delete_user.delete()
        return redirect("")

    return render(request, 'oaksartapp/delete-account.html')
