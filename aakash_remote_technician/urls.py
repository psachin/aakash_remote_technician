from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset_done
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples
                       #url(r'^$','register.views.index'),
                       # url(r'^aakash_remote_technician/', include('aakash_remote_technician.register.urls')),
                       # Uncomment the admin/doc line below to enable admin documentation
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       # Uncomment the next line to enable the admin
                       url(r'^admin/', include(admin.site.urls)),
                       # custom URLs
                       # url(r'^list/(?P<pID>\d+)/$','register.views.list'),
                       url(r'^list/$','register.views.list'),
                       url(r'^logged_in', 'register.views.render_logged_in_user_list'),
                       # user regi
                       url(r'^register/$','register.views.register'),
                       url(r'^tr/$','register.views.register_technician'),
                       # login
                       url(r'^$','django.contrib.auth.views.login', 
                           {'template_name': 'registration/login.html'}
                           ),
                       # logout
                       url(r'^logout/$','register.views.logout_view'),
                       # user's home
                       url(r'^profiles/home', 'register.views.user_home'),
                       # complaint
                       url(r'^complaint/(?P<username>\w+)/$','register.views.user_complaints'),
                       # take complaint from user
                       url(r'^assign/(?P<user_id>\d+)/(?P<complaint_id>\d+)/(?P<technician_id>\d+)/$','register.views.assign'),
                       # complaint form
                       url(r'^complaint/$','register.views.complaint_form'),
                       # 
                       url(r'^tech/complaints/$','register.views.handle_complaint'),
                       # password reset
                       url(r'resetpassword/passwordreset/$','django.contrib.auth.views.password_reset_done'),
                       url(r'resetpassword/$','django.contrib.auth.views.password_reset'),
                       url(r'resetpassword/done/$','django.contrib.auth.views.password_reset_complete'),
                       url(r'resetpassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$','django.contrib.auth.views.password_reset_confirm'),
                       # jq testing
                       url(r'^jq/$','register.views.jq'),
                       # shell access
                       url(r'^shell/$','register.views.shell'),
                       )



