from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.http import HttpResponse

# Create your forms here.
from app.models import Movie, Vote


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class MovieForm(ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        self.current_user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Movie
        fields = ['url', 'title', 'description']

    def save(self, commit=True):
        movie = super(MovieForm, self).save(commit=False)

        movie.user = self.current_user

        if commit:
            movie.save()

        return movie


class VoteForm(ModelForm):

    def __init__(self, customData=None, *args, **kwargs):
        self.customData = customData
        super().__init__(*args, **kwargs)

    class Meta:
        model = Vote
        fields = ['vote']

    def save(self, commit=True):
        vote = super(VoteForm, self).save(commit=False)

        existsVote = Vote.objects.filter(
            user=self.customData['user'],
            movie=Movie.objects.get(pk=self.customData['movie_id'])
        )

        existsVote.delete()

        vote.user = self.customData['user']
        vote.movie = Movie.objects.get(pk=self.customData['movie_id'])
        vote.vote = self.customData['vote']

        if commit:
            vote.save()

        return vote
