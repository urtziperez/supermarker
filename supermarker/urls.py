from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
#from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('supermarker',
    (r'^', include('usuarios.urls')),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
