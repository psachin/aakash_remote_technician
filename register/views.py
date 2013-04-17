from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from models import UserProfile
from forms import Register

def profile(request, pID):
    users = User.objects.all()
    user_profiles = users.get(id=pID)
    user_profile = user_profiles.get_profile()
    return render_to_response('profile.html',{'users':users,'user_profile':user_profile},context_instance=RequestContext(request))

# ====================

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

def index(request):
    return HttpResponseRedirect('/register')











