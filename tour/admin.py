from django.contrib import admin
from tour.models import *


class ReviewInline(admin.StackedInline):
    model = Review


class PlanAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ]


admin.site.register(Agency)
admin.site.register(TripPoint)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(District)
admin.site.register(Destination)
