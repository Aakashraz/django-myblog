"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from blog.sitemaps import PostSitemap, TagSitemap


sitemaps = {
    # maps 'posts' section to PostSitemap class
    'posts': PostSitemap,
    'tags': TagSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path(
        'sitemap.xml',  # URL will be your_site.com/sitemap.xml
        sitemap,        # Django's built-in view called (sitemap) located in django.contrib.sitemaps.views
        {'sitemaps': sitemaps},     # Passes our sitemap dictionary
        name='django.contrib.sitemaps.views.sitemap'
        # the name given to a URL pattern is an internal identifier used for reverse URL lookup and does not
        # affect the actual URL that users type in their browsers.
    )
]
