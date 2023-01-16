from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm
import tiledb


# Create your views here.
def LoginPage(request):
    form = UserForm()
    context = {'form': form, 'errors': None}
    if request.method == "POST":
        #here somebody is trying to login, so validate that the username is real
        #I opt here to fetch the data from the request object itself, but in general, it would probably be best to fetch it
        #from the form object
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return redirect('LandingPage')
            else:
                context = {'form': form, 'errors': "Incorrect Password"}
                return render(request, "LoginPage.html", context)
                
        except:
            #in this case the username does not exist in the DB
            context = {'form': form, 'errors': "Username does not exist in the DB"}
            return render(request, "LoginPage.html", context)
    return render(request, "LoginPage.html", context)


def LandingPage(request):
    context = {}
    if request.method == "POST":
        pass
    return render(request, "LandingPage.html", context)