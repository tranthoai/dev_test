from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm, MovieForm, VoteForm
from django.http import HttpResponse

from .models import Movie, Vote


def home(request):
    form = AuthenticationForm()

    movieList = Movie.objects.all()

    for movie in movieList:

        totalVoteUp = Vote.objects.filter(
            movie=movie,
            vote=1
        )

        totalVoteDown = Vote.objects.filter(
            movie=movie,
            vote=0
        )

        movie.total_vote_up = totalVoteUp.count()
        movie.total_vote_down = totalVoteDown.count()

        if request.user.is_authenticated:
            userVote = Vote.objects.filter(
                user=request.user,
                movie=movie
            )

            movie.userVote = userVote.count()

            movie.voted_up = userVote.count() and (userVote.first().vote == 1)

            movie.voted_down = userVote.count() and (userVote.first().vote == 0)

    return render(
        request=request,
        template_name="home.html",
        context={
            "login_form": form,
            'movieList': movieList
        }
    )


def register_request(request):
    if request.method == "POST":

        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Registration successful."
            )

            return redirect("app:home")

        messages.error(
            request,
            "Unsuccessful registration. Invalid information."
        )

    form = NewUserForm()

    return render(
        request=request,
        template_name="register.html",
        context={
            "register_form": form
        }
    )


def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            user = authenticate(username=username, password=password)

            if user is not None:

                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("app:home")

            else:
                messages.error(request, "Invalid username or password.")
                return redirect("app:register")

        else:

            messages.error(request, "Invalid username or password.")
            return redirect("app:register")

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="login.html",
        context={
            "login_form": form
        }
    )


def logout_request(request):
    logout(request)

    messages.info(request, "You have successfully logged out.")

    return redirect("app:home")


def share_request(request):
    if request.method == "POST":

        form = MovieForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            messages.info(
                request, "You have successfully shared."
            )
            return redirect("app:home")

    form = MovieForm

    return render(
        request=request,
        template_name="share.html",
        context={
            'form': form
        }
    )


def vote_request(request):
    if request.method == "GET":
        form = VoteForm(
            customData={
                'user': request.user,
                'movie_id': request.GET['movie_id'],
                'vote': request.GET['vote']
            },
            data=request.GET
        )

        form.save()

        messages.info(
            request, "You have successfully voted."
        )

        return redirect("app:home")

    return redirect("app:home")
