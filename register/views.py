from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import UserProfile
from forms import Register#, TechnicianRegister
from logged_in import get_all_logged_in_users

def index(request):
    return HttpResponseRedirect('/login')

def register(request):
    """
    Generate user registration form
    """

    # is user is already registered
    '''
    if request.user.is_authenticated():
    return HttpResponseRedirect('/profiles/home')
    '''
    # user is submitting the form
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            user = form.save()
            form.group_save()
            if user:
                #success="<html>sign_up_success</html>"
                #return HttpResponse(success)
                #messages.info(request, "Thanks for registering. You are now logged in.")
                user = authenticate(username=request.POST['username'],
                                        password=request.POST['password1'])
                login(request, user)
                return HttpResponseRedirect('/profiles/home')
    else:
        # user is NOT submitting the from, show him a blank form
        form = Register()

    context = {'form':form}
    return render_to_response('sign_up.html', 
                              context, 
                              context_instance=RequestContext(request))

def technician_register(request):
    """
    Generate technician registration form
    """
    if request.method == 'POST':
        form = TechnicianRegister(request.POST)
        if form.is_valid():
            technician = form.save()
            if technician:
                success="<html>sign_up_success</html>"
                return HttpResponse(success)
    else:
        form = TechnicianRegister()
    return render_to_response('sign_up.html', 
                              {'form':form}, 
                              context_instance=RequestContext(request))

#def list(request, pID):
def list(request):
    users = User.objects.all()
#    user_profiles = users.get(id=pID)
#    user_profile = user_profiles.get_profile()
    context = {'users':users,
#               'user_profile':user_profile,
               }
    return render_to_response('list.html',
                              context,
                              context_instance=RequestContext(request))

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
    # logged_in_users = request.user
    # if logged_in_users.is_authenticated():
    #     logged_in_user = logged_in_users
    # get profile for user = models.OneToOneField(User)
    users_profile = request.user.get_profile()
    user_group = request.user.groups.values_list('name',flat=True)
    for groups in user_group:
        print groups
    
    context = {'users':users, 
               'users_profile':users_profile,
               'user_group':user_group,
               }
    return render_to_response('registration/profile.html',
                              context,
                              context_instance=RequestContext(request))

def render_logged_in_user_list(request):
    return render_to_response('logged_in.html',
                              {'users':get_all_logged_in_users, 
                               },
                              context_instance=RequestContext(request))

def logout_view(request):
    logout_then_login(request)
    return HttpResponseRedirect('/login')










