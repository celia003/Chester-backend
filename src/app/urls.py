"""
URL configuration for thalos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # path('', include(router.urls)),
    path('', include('management.urls')),
    path('api/management/', include('management.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # urlpatterns += [path(r'^silk/', include('silk.urls', namespace='silk'))]
    # urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.urls import re_path
    from django.views.static import serve
    #from django.conf import settings
    urlpatterns += [
        # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]