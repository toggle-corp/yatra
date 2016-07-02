from django.contrib.auth.models import User
from tour.models import *
from tour.score import *
from tour.location import *


def sort_by_recommended(plans, user):
    return sorted(plans, key=lambda p: get_score(p, user), reverse=True)


# def get_close_plans(plans, destination):
#     pks = []
#     dists = {}
#     for p in plans:
#         dist = get_dest_diff(destination, p.destination)
#         if dist < 5:
#             dists[p.pk] = dist
#             pks.append(p.pk)
#
#     return sorted(pks, key=lambda p: dists[p])


class PlanFilter:
    def __init__(self, plans=None):
        self.plans = plans if plans else Plan.objects.all()
        self.pk_order = None

    def min_cost(self, cost):
        self.plans = self.plans.filter(budget__gte=cost)

    def max_cost(self, cost):
        self.plans = self.plans.filter(budget__lte=cost)

    def min_days(self, days):
        self.plans = self.plans.filter(number_of_days__gte=days)

    def max_days(self, days):
        self.plans = self.plans.filter(number_of_days__lte=days)

    def destination(self, destination):
        # plans = get_close_plans(self.plans, destination)
        # self.pk_order = plans
        # return PlanFilter(self.plans.filter(pk__in=plans))
        self.plans = self.plans.filter(destination=destination).filter(
            destination__district=destination.district
        )

    def district(self, district):
        self.plans = self.plans.filter(destination__district=district)

    def category(self, category):
        self.plans = self.plans.filter(category=category)

    def get(self):
        if self.pk_order:
            objects = dict([(p.pk, p) for p in self.plans])
            return [objects[pk] for pk in self.pk_order]

        else:
            return list(self.plans)
