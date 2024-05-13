"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin,auth
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, auth
from . import views
from django.contrib.auth import views as auth_views

'''from rest_framework import routers
from magasin.views import ProductViewset, Category
 
# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé 'category' et notre view
# afin que lurl générée soit celle que nous souhaitons '/api/category/'
router.register('produit', ProductViewset, basename='produit')'''





#from ManafeStudent22 import ManageStudent
from . import views
urlpatterns = [
    path('', views.index),
    path("admin/", admin.site.urls),
     #path('api-auth/', include('rest_framework.urls')),
    path('magasin/',include('magasin.urls')) ,
    #path('api/', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    
     path('Login/', auth_views.LoginView.as_view(template_name='magasin/registration/Login.html'), name='Login'),
    path('Logout/', auth_views.LogoutView.as_view(template_name='magasin/registration/Logout.html'), name='Logout'),

    path('accounts/password_reset_complete/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password_reset_email/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_email.html'), name='password_reset_email'),
    path('accounts/password_reset/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('api-auth/', include('rest_framework.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

