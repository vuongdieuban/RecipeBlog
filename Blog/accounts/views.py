from django.shortcuts import render, redirect, reverse
from django.contrib.auth import (
                                    authenticate,
                                    get_user_model,
                                    login,
                                    logout,
                                 )

from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
def login_view(request):
    title = 'Login'
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/./')  # back to homepage
    context = {'form': form,
               'title': title,
               }
    return render(request, 'accounts/login.html', context)


def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')  # pre-hashed, save password so we can pass into authenticate later
        user.set_password(password)  # hashing the password
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('/./')
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/./')