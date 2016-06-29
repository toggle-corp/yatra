from django.contrib import admin
from tour.models import *


class ReviewInline(admin.StackedInline):
    model = Review


class PlanAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ]


admin.site.register(TripPoint)
admin.site.register(Plan, PlanAdmin)
