from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=70, primary_key=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class TripPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    day = models.IntegerField()
    next_point = models.OneToOneField('TripPoint', null=True, blank=True,
                                      default=None)
    description = models.TextField(blank=True, default="")


class Destination(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    # parent = models.ForeignKey('Destination', null=True, blank=True,
    #                            default=None)

    def __str__(self):
        return self.name

    @staticmethod
    def get_or_create(name):
        try:
            return Destination.objects.get(name=name)
        except:
            dest = Destination()
            dest.name = name
            dest.save()
            return dest


class Plan(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=True, default="")
    destination = models.ForeignKey(Destination)
    starting_point = models.OneToOneField(TripPoint)
    budget = models.IntegerField(null=True, blank=True, default=None)
    public = models.BooleanField(default=True)
    number_of_days = models.IntegerField()

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk) + " " + self.title


class Review(models.Model):
    plan = models.ForeignKey(Plan)
    review = models.TextField(blank=True, default="")
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])
    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('plan', 'posted_by',)

    def __str__(self):
        return self.plan.title + " by " + self.posted_by.username + \
            " Rating: " + str(self.rating)

    @staticmethod
    def get_average_rating(plan):
        ratings = Review.objects.filter(plan=plan).values_list('rating',
                                                               flat=True)
        return 0 if len(ratings) == 0 else sum(ratings)/len(ratings)
