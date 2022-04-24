"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('', include("movie.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

"""
we used djoser for authentication

available routes:
    auth/users/
    auth/users/me/
    auth/users/confirm/
    auth/users/resend_activation/
    auth/users/set_password/
    auth/users/reset_password/
    auth/users/reset_password_confirm/
    auth/users/set_username/
    auth/users/reset_username/
    auth/users/reset_username_confirm/
    auth/jwt/create/ (JSON Web Token Authentication)
    auth/jwt/refresh/ (JSON Web Token Authentication)
    auth/jwt/verify/ (JSON Web Token Authentication)

documentation: https://djoser.readthedocs.io/

"""