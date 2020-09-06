"""Certifie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView # <--
from certificates.views import certificate_list_view,next_post, generate,userlogin,userlogout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/', certificate_list_view,name='home'),
    re_path('next/(?P<certid>[a-z0-9-]*)/',next_post,name='next-post'),
    path('success/',generate),
    path('', userlogin ,name='userlogin'),
    path('logout/', userlogout ,name='userlogout'),

    #path('form/', form_data),
    #path('home/',home),
    #path('register/',register,name='register'),

    #path('', TemplateView.as_view(template_name="googlesignup.html")), # <-- for google sign in
    path('accounts/', include('allauth.urls')), # <-- for google sign in


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)