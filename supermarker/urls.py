from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('supermarker',
    (r'^', include('usuarios.urls')),
	
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)