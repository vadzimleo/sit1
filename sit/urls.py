"""
URL configuration for sit project.

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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users.views import register as reg, profile as pro

from django.conf import settings
from django.conf.urls.static import static
#playground/hello
urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('registration/', reg, name="userregister"),
    path('my_profile/', pro, name="profil"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name ="users/logout.html"), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name ="users/password_reset.html"), name="resetpassword"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name ="users/password_reset_done.html"), name="password_reset_done"),
    #//{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name ="users/password_reset_confirm.html"), name="password_reset_confirm"),
    # NoReverseMatch at /password-reset-confirm/Mg/set-password/
    # Reverse for 'password_reset_complete' not found. 'password_reset_complete' is not a valid view function or pattern name. 
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name ="users/password_reset_complete.html"), name="password_reset_complete"),
    #path('', include('users.urls')),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


#{% load i18n %}{% autoescape off %}
# 2	{% blocktranslate %}You're receiving this email because you requested a password reset for your user account at {{ site_name }}.{% endblocktranslate %}
# 3	
# 4	{% translate "Please go to the following page and choose a new password:" %}
# 5	{% block reset_link %}
# 6	{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
# 7	{% endblock %}
# 8	{% translate 'Your username, in case you’ve forgotten:' %} {{ user.get_username }}
# 9	
# 10	{% translate "Thanks for using our site!" %}
# 11	
# 12	{% blocktranslate %}The {{ site_name }} team{% endblocktranslate %}
# 13	
# 14	{% endautoescape %}