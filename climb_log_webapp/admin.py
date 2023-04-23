from django.contrib import admin
from .models import Climb_entry

# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     list_filter = ("gender", "age")
#     list_display = ("username", "email")

class Climb_entryAdmin(admin.ModelAdmin):
    list_filter = ("username","date_of_climb" )
    list_display = ("username", "grade", "enviroment")


# admin.site.register(User, UserAdmin)
admin.site.register(Climb_entry, Climb_entryAdmin)
