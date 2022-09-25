"""All url pattern for the webpage main."""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name="main"),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home')
]
