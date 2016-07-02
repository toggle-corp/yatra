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
        recommendations = sort_by_recommended(plans, user)[:8]
        for plan in recommendations:
            plan.rating = Review.get_average_rating(plan)
        return render(request, 'tour/dashboard.html', {
            'recommendations': recommendations,
            'destinations': Destination.objects.all(),
            "categories": Category.objects.all(),
        })

    @method_decorator(login_required)
    def post(self, request):
        plan = Plan()
        plan.destination = Destination.objects.get(
            pk=request.POST["destination"]
        )
        plan.category = Category.objects.get(
            pk=request.POST["category"]
        )
        plan.title = request.POST["title"]
        plan.created_by = request.user
        plan.save()
        return reditect('plan', plan.pk)


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

        data = {}

        if dest != "":
            plan_filter.destination(Destination.objects.get(pk=dest))
            data["dest"] = dest
        if categ != "":
            plan_filter.category(Category.objects.get(pk=categ))
            data["categ"] = categ
        if min_days != "":
            plan_filter.min_days(int(min_days))
            data["min_days"] = min_days
        if max_days != "":
            plan_filter.max_days(int(max_days))
            data["max_days"] = max_days
        if min_cost != "":
            plan_filter.min_cost(int(min_cost))
            data["min_cost"] = min_cost
        if max_cost != "":
            plan_filter.max_cost(int(max_cost))
            data["max_cost"] = max_cost

        plans = sort_by_recommended(plan_filter.get(), request.user)
        for plan in plans:
            plan.rating = Review.get_average_rating(plan)

        data.update({
            "destinations": Destination.objects.all(),
            "categories": Category.objects.all(),
            "plans": plans,
        })
        return render(request, 'tour/search.html', data)


def delete_point(point):
    if point.next_point:
        delete_point(point.next_point)
    point.delete()


class PlanView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        plan = Plan.objects.get(pk=pk)
        plan.rating = Review.get_average_rating(plan)

        points = []
        point = plan.next_point
        while point:
            points.append(point)
            point = point.next_point

        try:
            review = Review.objects.get(plan=plan, posted_by=request.user)
        except:
            review = None
        return render(request, 'tour/plan.html', {
            'plan': plan,
            'edit': plan.created_by == request.user,
            'points': points,
            'review': review,
            'all_reviews': Review.objects.all(),
        })

    @method_decorator(login_required)
    def post(self, request, pk):
        plan = Plan.objects.get(pk=pk)

        if "delete" in request.POST:
            plan.delete()
            return redirect('dashboard')

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
                review.text = request.POST["review"]
                review.save()
            except:
                review = Review(plan=plan, rating=1,
                                text=request.POST["review"],
                                posted_by=request.user)
                review.save()
            return redirect('plan', pk)

        if "title" in request.POST:
            plan.title = request.POST["title"]

        if "description" in request.POST:
            plan.description = request.POST["description"]
        plan.save()

        if "points" in request.POST:
            if plan.next_point:
                to_delete = plan.next_point
                plan.next_point = None
                plan.save()
                delete_point(to_delete)

            points = json.loads(request.POST["points"])

            pt = plan
            for point in points:
                tp = TripPoint()
                tp.latitude = point[0]
                tp.longitude = point[1]
                tp.day = point[2]
                tp.description = point[3]
                tp.save()
                pt.next_point = tp
                pt.save()
                pt = tp
            plan.number_of_days = max([x[2] for x in points]) \
                if len(points) > 0 else 0
            plan.save()
        return redirect('plan', pk)


class VisualizeView(View):
    def get(self, request):
        plans = None
        order = "popular"
        if "destination-order" in request.GET:
            order = request.GET["destination-order"]

        if order == "popular":
            destinations = Destination.objects.all()
            destinations = \
                sorted(
                    destinations,
                    key=lambda d: Plan.objects.filter(destination=d).count(),
                    reverse=True
                )
        elif order == "rating":
            plans = Plan.objects.all()
            plans = \
                sorted(
                    plans, key=lambda p: Review.get_average_rating(p),
                    reverse=True
                )
            destinations = []
            for p in plans:
                if p.destination not in destinations:
                    destinations.append(p.destination)

        destination_order = order

        order = "popular"
        if "category-order" in request.GET:
            order = request.GET["category-order"]

        if order == "popular":
            categories = Category.objects.all()
            categories = \
                sorted(
                    categories,
                    key=lambda c: Plan.objects.filter(category=c).count(),
                    reverse=True
                )
        elif order == "rating":
            if not plans:
                plans = Plan.objects.all()
                plans = \
                    sorted(
                        plans, key=lambda p: Review.get_average_rating(p),
                        reverse=True
                    )
            categories = []
            for p in plans:
                if p.category not in categories:
                    categories.append(p.category)

        category_order = order

        return render(request, 'tour/visualize.html', {
            'destinations': destinations,
            'destination_order': destination_order,
            'categories': categories,
            'category_order': category_order,
        })
