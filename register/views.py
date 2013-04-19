from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import UserProfile
from forms import Register

def index(request):
    return HttpResponseRedirect('/login')


def register(request):
    """my register"""
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            success="<html>sign_up_success</html>"
            return HttpResponse(success)
    else:
        form = Register()
        
    return render_to_response('sign_up.html', {'form':form}, context_instance=RequestContext(request))

def profile(request, pID):
    users = User.objects.all()
    user_profiles = users.get(id=pID)
    user_profile = user_profiles.get_profile()
    return render_to_response('profile.html',{'users':users,'user_profile':user_profile},context_instance=RequestContext(request))

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            login_success="<html><h1 align=center>Welcome user</h1></html>"
            return HttpResponse(login_success)
        else:
            login_disabled="<html>Your login is disabled</html>"
            return HttpResponse(login_disabled)
    else:
        login_error="<html>Username or password mismatch</html>"
        return HttpResponse(login_error)

@login_required
def user_home(request):
    users = User.objects.all()
    users_profile = request.user.get_profile()
    return render_to_response('registration/profile.html',{'users':users, 'users_profile':users_profile},context_instance=RequestContext(request))

def logout_view(request):
    logout_then_login(request)
    return HttpResponseRedirect('/login')










