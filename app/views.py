from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from .forms import NewUserForm


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
        context={"register_form": form}
    )


def home(request):
    return HttpResponse(
        "HomePage",
        content_type="text/plain"
    )
