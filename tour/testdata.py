from django.contrib.auth.models import User
from django.conf import settings

import random
import json
import os

from tour.models import *


def add_test_data():

    destinations = ["Kathmandu", "Annapurna", "Everest"]
    districts = ["Kathmandu", "Mustang", "Solukhumbu"]

    categories = Category.objects.all()
    user_categories = {}
    category_plans = {}

    all_users = list(User.objects.all())

    for category in categories:
        category_plans[category.pk] = []
        for i in range(5):
            user = User.objects.create_user(category.name+"_user_" + str(i),
                                            password='danphe123')
            user.save()
            user_categories[user.pk] = category.pk

            plan = Plan()
            plan.category = category
            plan.title = "Test plan - " + category.name + " #" + str(i)
            dd = random.randint(0, len(destinations)-1)
            plan.destination = Destination.get_or_create(
                destinations[dd], districts[dd]
            )
            plan.number_of_days = random.choice(list(range(5, 30)))
            plan.budget = random.choice(list(range(250, 10250, 250)))

            tp = TripPoint()
            tp.day = 1
            tp.latitude = 0
            tp.longitude = 0
            tp.save()
            plan.starting_point = tp
            plan.created_by = random.choice(all_users)
            plan.save()

            category_plans[category.pk].append(plan.pk)

    for user in user_categories:
        for category in categories:
            for plan in category_plans[category.pk]:
                review = Review()
                review.posted_by = User.objects.get(pk=user)
                review.rating = 5 if category.pk == user_categories[user] \
                    else random.choice(range(1, 5))
                review.plan = Plan.objects.get(pk=plan)
                if random.randint(1, 8) == 3:
                    review.save()


def add_districts():
    file_path = os.path.join(settings.BASE_DIR,
                             'static/gis/nepal/admin_level_6.geojson')
    text = open(file_path, 'r').read()
    text = text[text.find('=')+1:]
    data = json.loads(text)
    for feature in data["features"]:
        district = feature["properties"]["name:en"]
        District.get_or_create(district)
