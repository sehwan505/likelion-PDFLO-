from django.contrib import admin
from MECboard.models import Board,Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class BoardAdmin(admin.ModelAdmin):
    list_display = ("writer", "title", "content","win_score","is_finished")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nickname")

admin.site.register(Board, BoardAdmin)
admin.site.register(Profile, ProfileAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile
    con_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)