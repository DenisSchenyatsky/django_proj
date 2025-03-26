from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
# Register your models here.

class ProfileInline(admin.TabularInline):
    model = Profile 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = [
    #     ProfileInline,
    # ]
    list_display = "pk", "user", "bio", "agreement_accepted", "avatar"
    #list_display_links = "pk", "name"
    ordering = "pk", 
    fieldsets = [
        (None, {
            "fields": ("user", "bio"),
        }),
        ("Avatar", {
            "fields": ("avatar", )
            
        }),
        ("Options", {
            "fields": ("agreement_accepted",),
            "classes": ("collapse",),
            "description": ("Options Field Agreement Accepted")
        }),
    ]
