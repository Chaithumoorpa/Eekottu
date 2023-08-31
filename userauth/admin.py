from django.contrib import admin
from userauth.models import User


# Register your models here.
class Useradmin(admin.ModelAdmin):
    list_display=['username', 'email','is_active' ]

admin.site.register(User, Useradmin)
