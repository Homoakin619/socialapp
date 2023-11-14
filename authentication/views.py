from django.shortcuts import render

from .forms import UserRegistrationForm

def loginUser(request):
    if request.method == "POST":
        loginForm = UserRegistrationForm(request.POST)
        print(loginForm)
    return 1;