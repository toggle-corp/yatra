import math

from django.contrib.auth.models import User
from tour.models import *
from tour.location import *


def average(values):
    return sum(values)/len(values) if len(values) != 0 else 0


def get_normal_diff(v1, v2):
    return float(v1-v2)/float(max(v1, v2))


def pearson(x, y):
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(map(lambda x: pow(x, 2), x))
    sum_y_sq = sum(map(lambda x: pow(x, 2), y))
    psum = sum(map(lambda x, y: x * y, x, y))
    num = psum - (sum_x * sum_y/n)
    den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n),
              0.5)
    return 0 if den == 0 else num/den


def get_plans_difference(p1, p2):
    # Difference in number of days.
    dist = get_normal_diff(p1.number_of_days, p2.number_of_days)**2 / 3

    # Difference in budget.
    if p1.budget and p2.budget:
        dist += get_normal_diff(p1.budget, p2.budget)**2 / 3

    # Difference in destination.
    # dist += get_dest_diff(p1.destination, p2.destination) / 5 / 1.5

    # Difference in category.
    dist += 0 if p1.category.pk == p2.category.pk else 1

    return math.sqrt(dist)


def get_content_based_rating(plan, user):
    reviews = Review.objects.filter(posted_by=user)
    scores = []

    for review in reviews:
        dist = get_plans_difference(plan, review.plan)
        if dist < 0.5:
            scores.append(review.rating/5 * (1-dist))

    return average(scores)


def get_collaborative_item_rating(plan, user):
    reviews = Review.objects.filter(posted_by=user)
    scores = []

    p1 = plan
    for review in reviews:
        p2 = review.plan
        overlap = User.objects.filter(review__plan=p1).filter(review__plan=p2)
        if len(overlap) > 0:
            r1s = []
            r2s = []
            for u in overlap:
                r1s.append(Review.objects.get(posted_by=u, plan=p1).rating)
                r2s.append(Review.objects.get(posted_by=u, plan=p2).rating)
            scores.append(review.rating/5 * max(0, pearson(r1s, r2s)))

    return average(scores)


def get_collaborative_user_rating(plan, user):
    users = User.objects.filter(review__plan=plan)
    scores = []

    u1 = user
    for u2 in users:
        rating = Review.objects.get(plan=plan, posted_by=u2).rating
        overlap = Plan.objects.filter(review__posted_by=u1) \
            .filter(review__posted_by=u2)
        dratings = []
        for p in overlap:
            r1 = Review.objects.get(plan=p, posted_by=u1).rating
            r2 = Review.objects.get(plan=p, posted_by=u2).rating
            dratings.append((r1-r2)/5)

        diff = average(dratings)
        scores.append(rating/5 * (1-diff))

    return average(scores)


def get_score(plan, user):
    w1, s1 = 0, 0
    w2, s2 = 0.5, get_content_based_rating(plan, user)
    w3, s3 = 0.6, get_collaborative_item_rating(plan, user)
    w4, s4 = 0.7, get_collaborative_user_rating(plan, user)
    w5, s5 = 0.5, Review.get_average_rating(plan)

    return w1*s1 + w2*s2 + w3*s3 + w4*s4 + w5*s5
