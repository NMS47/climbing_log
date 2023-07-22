from django.contrib import admin
from .models import ClimbEntry, ClimbPlaces

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter = ("gender", "age")
    list_display = ("username", "email")


class ClimbEntryAdmin(admin.ModelAdmin):
    list_filter = ("username","date_of_climb", "place_name" )
    list_display = ("username", "grade")

class ClimbPlacesAdmin(admin.ModelAdmin):
    list_filter = ("place_name","enviroment")
    list_display = ("place_name","enviroment")

# class ClimbAdmin(ClimbEntry, ClimbPlaces):
#     pass


# admin.site.register(User, UserAdmin)
admin.site.register(ClimbEntry, ClimbEntryAdmin)
admin.site.register(ClimbPlaces, ClimbPlacesAdmin)
