"""yatra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from tour.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^dashboard/$', DashboardView.as_view(), name="dashboard"),
    url(r'^search/$', SearchView.as_view(), name="search"),
    url(r'^plan/(?P<pk>\d+)/$', PlanView.as_view(), name="plan"),

    url(r'^visualize/$', VisualizeView.as_view(), name="visualize"),
]
