from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from core.views import AboutView


urlpatterns = [
    url(r'^about/$', AboutView.as_view(), name='about'),
    url(r'', include('blog.urls', namespace='blog')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
