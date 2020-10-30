from django.contrib import admin
from user_handler.models import UserBase, Profile
admin.site.register(UserBase)
admin.site.register(Profile)