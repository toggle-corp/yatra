from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class TripPoint(models.Model):
    day = models.IntegerField()
    next_point = models.OneToOneField('TripPoint', null=True, blank=True)
    description = models.TextField(blank=True)


class Plan(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    destination = models.CharField(max_length=200)
    starting_point = models.OneToOneField(TripPoint)
    budget = models.IntegerField(null=True, blank=True)
    public = models.BooleanField(default=True)
    number_of_days = models.IntegerField()

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    plan = models.ForeignKey(Plan)
    review = models.TextField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])
    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('plan', 'posted_by',)

    def __str__(self):
        return self.plan.title + self.review[:30]
