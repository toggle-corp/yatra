from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from tour.models import *


class HomeView(View):
    def get(self, request):

        # If already logged-in, redirect to dashboard.
        if request.user and request.user.is_active:
            return redirect("dashboard")

        return render(request, 'tour/home.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'tour/dashboard.html')


class PlanView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'tour/plan.html')
