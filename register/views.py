from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import logout_then_login

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import Profile, DeviceUser, Technician, Complaint
from forms import RegisterDeviceUser, LogComplaint
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
        form = RegisterDeviceUser(request.POST)
        #profile = request.user.get_profile()
        if form.is_valid():
            user = form.save()
            if user:
                # success="<html>sign_up_success</html>"
                # return HttpResponse(success)
                #messages.info(request, "Thanks for registering. You are now logged in.")
                user = authenticate(username=request.POST['username'],
                                        password=request.POST['password1'])
                login(request, user)
                return HttpResponseRedirect('/profiles/home')
    else:
        # user is NOT submitting the from, show him a blank form
        form = RegisterDeviceUser()

    context = {'form':form}
    return render_to_response('sign_up.html', 
                              context, 
                              context_instance=RequestContext(request))

def complaint_form(request):
    """
    show complaint box after user logs in
    """
    if request.method == 'POST':
        form = LogComplaint(request.POST)
        #profile = request.user.get_profile()
        if form.is_valid():
            user = form.save()
            if user:
                success="<html>Complaint registered</html>"
                return HttpResponse(success)
    else:
        form = LogComplaint()

    context = {
        'form':form
        }
    
    return render_to_response('complaint.html', 
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

    '''
    # print request.user
    user_obj = users.get(username=request.user)
    # print user_obj
    # if DeviceUser.objects.exists():
    user_profile = Profile.objects.get(user=user_obj)
    # print user_profile
    dev_obj = DeviceUser.objects.get(user=user_profile)
    # print dev_obj
    '''
    
    user_group = request.user.groups.values_list('name',flat=True)
    for group in user_group:
        # print "Group: %s" % (group)
        if group:
            if group == "aakash_user":
                print "%s belongs to %s group" %(request.user,group)
                # print request.user
                user_obj = users.get(username=request.user)
                print user_obj
                # if DeviceUser.objects.exists():
                user_profile = Profile.objects.get(user=user_obj)
                print user_profile
                dev_obj = DeviceUser.objects.get(user=user_profile)
                print dev_obj
            elif group == "technician":
                print "%s belongs to %s group" %(request.user,group)
                # print request.user
                user_obj = users.get(username=request.user)
                print user_obj
                # if DeviceUser.objects.exists():
                user_profile = Profile.objects.get(user=user_obj)
                print user_profile
                dev_obj = DeviceUser.objects.get(user=user_profile)
                print dev_obj
        else:
            print "%s dont belongs to any group"


    context = {'users':users, 
               'dev_obj':dev_obj,
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
    return HttpResponseRedirect('/')










