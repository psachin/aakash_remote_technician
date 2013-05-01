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
                       url(r'^register/$','register.views.register'),
                       url(r'^tr/$','register.views.technician_register'),
                       url(r'^$','django.contrib.auth.views.login', 
                           {'template_name': 'registration/login.html'}
                           ),
                       url(r'^logout/$','register.views.logout_view'),
                       url(r'^profiles/home', 'register.views.user_home'),
                       url(r'^logged_in', 'register.views.render_logged_in_user_list'),
                       # complaint
                       url(r'^complaint/$','register.views.complaint_form'),
                       # password reset
                       url(r'resetpassword/passwordreset/$','django.contrib.auth.views.password_reset_done'),
                       url(r'resetpassword/$','django.contrib.auth.views.password_reset'),
                       url(r'resetpassword/done/$','django.contrib.auth.views.password_reset_complete'),
                       url(r'resetpassword/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)$','django.contrib.auth.views.password_reset_confirm'),
                       )
