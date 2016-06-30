from tour.models import *
from django.contrib.auth.models import User
from tour.search import *
from tour.testdata import *


def run():
    user = User.objects.get(username="Trekking_user_3")
    print(sort_by_recommended(Plan.objects.all().exclude(review__posted_by__pk=user.pk), user))
