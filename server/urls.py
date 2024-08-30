"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import *

urlpatterns = [
    # Chat app
    path('', HomePageView.as_view()),
    path('chat-group', ChatGroupView.as_view(), name='chat_group'),
    path('chat-direct', ChatDirectView.as_view(), name='chat_direct'),
    path('chat-empty', ChatEmptyView.as_view(), name='chat_empty'),
    # Auth
    path(
        'chat-signin',
        auth_views.LoginView.as_view(template_name='auth/signin.html'),
        name='chat_signin',
    ),
    # path('logout', auth_views.LoginView.as_view(), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chat-signup', ChatSignUpView.as_view(), name='chat_signup'),
    path('chat-lockscreen', ChatLockScreenView.as_view(), name='chat_lockscreen'),
    path('password-reset', ChatPasswordResetView.as_view(), name='password_reset'),
    # Comman
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('api/auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
