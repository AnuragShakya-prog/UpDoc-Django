from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
# Create your views here.



def logout_view(request):
    if (request.user.is_authenticated):

        if request.method=="GET":
             return render(request,"accounts/logout.html")
        elif request.method=="POST":
            logout(request)
            return redirect(settings.LOGOUT_REDIRECT_URL)
    
    else:
        return redirect("/accounts/login")


def login_view(request):
    if (request.user.is_authenticated):
        return redirect("/")
    else:
        return LoginView.as_view(template_name="accounts/login.html")(request)


def signup(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method=='POST':
        
        form=SignupForm(request.POST)
        
        if form.is_valid():
            messages.add_message(request,messages.SUCCESS,"Account created successfully")
            user=form.save()
            return redirect("/accounts/login")

    else:
        form=SignupForm()

    return render(request,"accounts/signup.html",{"form":form})

    

        
