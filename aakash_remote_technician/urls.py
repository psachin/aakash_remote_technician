from django.conf.urls import patterns, include, url
from register.views import profile, index, register, user_home, logout_view
#from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples
                       url(r'^$',index),
                       # url(r'^aakash_remote_technician/', include('aakash_remote_technician.register.urls')),
                       
                       # Uncomment the admin/doc line below to enable admin documentation
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^profile/(?P<pID>\d+)/$',profile),
                       url(r'^register/$',register),
                       url(r'^login/$','django.contrib.auth.views.login', 
                           {'template_name': 'registration/login.html'}
                           ),
                       url(r'^logout/$',logout_view),
                       url(r'^profiles/home', user_home),
                       )
