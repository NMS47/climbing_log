from django.contrib import admin
from .models import Users, Climb_entry

# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_filter = ("gender", "age")
    list_display = ("username", "email")

class Climb_entryAdmin(admin.ModelAdmin):
    list_filter = ("username","date" )
    list_display = ("username", "grade", "enviroment")


admin.site.register(Users, UsersAdmin)
admin.site.register(Climb_entry, Climb_entryAdmin)
