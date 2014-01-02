from django.conf.urls import patterns, include, url

#from django.conf.urls.defaults import *
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('usuarios.views',
	(r'^register','register'),
	(r'^session/(?P<id>\w+)/$','session'),
	#(r'^lista','list'),
	(r'^session/(?P<iduser>\w+)/(?P<idlist>\w+)$','lista'),
	(r'^session/(?P<iduser>\w+)/add/(?P<idprod>\w+)','addproduct'),
	(r'^nosession','nosession'),
    (r'^login','login'),
    (r'^$','index'),
)
