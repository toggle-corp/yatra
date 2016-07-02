from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=70, primary_key=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Agency(models.Model):
    user = models.OneToOneField(User)
    title = models.CharField(max_length=100)
    address = models.TextField(blank=True, default="")
    phone = models.CharField(max_length=25, null=True, blank=True,
                             default=None)
    website = models.CharField(max_length=200, null=True, blank=True,
                               default=None)
    score = models.IntegerField(default=5, validators=[MinValueValidator(0),
                                MaxValueValidator(5)])

    class Meta:
        verbose_name_plural = "agencies"

    def __str__(self):
        return self.title


class TripPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    day = models.IntegerField()
    next_point = models.OneToOneField('TripPoint', null=True, blank=True,
                                      default=None)
    description = models.TextField(blank=True, default="")


class District(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_or_create(name):
        try:
            return District.objects.get(name=name)
        except:
            district = District()
            district.name = name
            district.save()
            return district


class Destination(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    district = models.ForeignKey(District)
    # parent = models.ForeignKey('Destination', null=True, blank=True,
    #                            default=None)

    def __str__(self):
        return self.name

    @staticmethod
    def get_or_create(name, district):
        try:
            return Destination.objects.get(name=name)
        except:
            dest = Destination()
            dest.name = name
            dest.district = District.get_or_create(district)
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
    text = models.TextField(blank=True, default="")
    rating = models.IntegerField(validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])
    posted_by = models.ForeignKey(User)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('plan', 'posted_by',)

    def __str__(self):
        return self.text

    @staticmethod
    def get_average_rating(plan):
        ratings = Review.objects.filter(plan=plan).values_list('rating',
                                                               flat=True)
        return 0 if len(ratings) == 0 else sum(ratings)/len(ratings)
