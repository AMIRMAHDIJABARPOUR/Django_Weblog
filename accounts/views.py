from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def user_login(request):

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                messages.success(request, f"Welcome {username}")

                return redirect("/")

        else:
            messages.error(request, "Username or password is incorrect.")

    return render(request, "accounts/login.html")


@login_required(login_url="/accounts/login/")
def user_logout(request):

    username = request.user.username
    logout(request)
    messages.success(request, f"goodbye {username}")
    return redirect("/")


def user_signup(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            username = user.username

            login(request, user)

            messages.success(request, f"Welcome to our blog {username}")

            return redirect("/")

        else:

            for field in form:
                for error in field.errors:

                    messages.error(request, f"{field.label}: {error}")

            for error in form.non_field_errors():

                messages.error(request, error)

    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})
