from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from tour.models import *
from tour.search import *

import json


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

            email = request.POST.get("email")
            username = request.POST.get("username")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                error = "Username already exists."
            else:
                user = User.objects.create_user(username, email=email,
                                                password=password)

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


def delete_point(point):
    if point.next_point:
        delete_point(point.next_point)
    point.delete()


class PlanView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        plan.rating = Review.get_average_rating(plan)

        points = [plan.starting_point]
        point = plan.starting_point
        while point.next_point:
            point = point.next_point
            points.append(point)

        try:
            review = Review.objects.get(plan=plan, posted_by=request.user)
        except:
            review = None
        return render(request, 'tour/plan.html', {
            'plan': plan,
            'edit': plan.created_by == request.user,
            'points': points,
            'review': review,
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        plan = Plan.objects.get(pk=pk)

        if "vote" in request.POST:
            try:
                review = Review.objects.get(plan=plan, posted_by=request.user)
                review.rating = request.POST["vote"]
                review.save()
            except:
                review = Review(plan=plan, rating=request.POST["vote"],
                                posted_by=request.user)
                review.save()
            return redirect('plan', pk)

        if "review" in request.POST:
            try:
                review = Review.objects.get(plan=plan, posted_by=request.user)
                review.review = request.POST["review"]
                review.save()
            except:
                review = Review(plan=plan, rating=1, review=request.POST["review"],
                                posted_by=request.user)
                review.save()
            return redirect('plan', pk)

        if "title" in request.POST:
            plan.title = request.POST["title"]

        if "description" in request.POST:
            plan.description = request.POST["description"]
        plan.save()

        if "points" in request.POST:
            to_delete = plan.starting_point.next_point

            points = json.loads(request.POST["points"])
            if len(points) > 0:
                plan.starting_point.latitude = points[0][0]
                plan.starting_point.longitude = points[0][1]
                plan.starting_point.day = points[0][2]
                plan.starting_point.description = points[0][3]
                plan.starting_point.next_point = None
                plan.starting_point.save()
            pt = plan.starting_point

            if to_delete:
                delete_point(to_delete)

            for point in points[1:]:
                tp = TripPoint()
                tp.latitude = point[0]
                tp.longitude = point[1]
                tp.day = point[2]
                tp.description = point[3]
                tp.save()
                pt.next_point = tp
                pt.save()
                pt = tp
        return redirect('plan', pk)


class VisualizeView(View):
    def get(self, request):
        destinations = Destination.objects.all()
        destinations = \
            sorted(destinations,
                   key=lambda d: Plan.objects.filter(destination=d).count(),
                   reverse=True)

        return render(request, 'tour/visualize.html', {
            'destinations': destinations
        })
