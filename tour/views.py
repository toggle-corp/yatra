from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from tour.models import *
from tour.search import *


class HomeView(View):
    def get(self, request):

        # If already logged-in, redirect to dashboard.
        if request.user and request.user.is_active:
            return redirect("dashboard")

        return render(request, 'tour/home.html')

    def post(self, request):
        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if not user or not user.is_active:
                error = "Invalid username and/or password."
                return render(request, 'tour/home.html',
                              {'login_error': error})
            login(request, user)
            return redirect('dashboard')

        elif "register" in request.POST:
            error = None

            first_name = request.POST.get("firstname")
            last_name = request.POST.get("lastname")
            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                error = "Username already exists."
            else:
                user = User.objects.create_user(username, email=email,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)

            if error:
                return render(request, 'tour/home.html',
                              {'register_error': error})

            user = authenticate(username=username, password=password)
            if not user:
                error = "Couldn't create user."
            login(request, user)
            return redirect('dashboard')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        plans = Plan.objects.all().exclude(review__posted_by__pk=user.pk)
        recommendations = sort_by_recommended(plans, user)[:5]
        for plan in recommendations:
            plan.rating = Review.get_average_rating(plan)
        return render(request, 'tour/dashboard.html', {
            'recommendations': recommendations,
            'destinations': Destination.objects.all(),
            "categories": Category.objects.all(),
        })


class SearchView(View):
    @method_decorator(login_required)
    def get(self, request):
        plan_filter = PlanFilter()

        categ = request.GET.get("category")
        dest = request.GET.get("destination")
        min_cost = request.GET.get("min_cost")
        max_cost = request.GET.get("max_cost")
        min_days = request.GET.get("min_days")
        max_days = request.GET.get("max_days")

        if dest != "":
            plan_filter.destination(Destination.objects.get(pk=dest))
        if categ != "":
            plan_filter.category(Category.objects.get(pk=categ))
        if min_days != "":
            plan_filter.min_days(int(min_days))
        if max_days != "":
            plan_filter.max_days(int(max_days))
        if min_cost != "":
            plan_filter.min_cost(int(min_cost))
        if max_cost != "":
            plan_filter.max_cost(int(max_cost))

        plans = sort_by_recommended(plan_filter.get(), request.user)
        for plan in plans:
            plan.rating = Review.get_average_rating(plan)

        return render(request, 'tour/search.html', {
            "destinations": Destination.objects.all(),
            "categories": Category.objects.all(),
            "plans": plans,
        })


class PlanView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'tour/plan.html')
