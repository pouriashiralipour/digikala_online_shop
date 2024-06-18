from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm
from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     form = CustomUserCreationForm
#     model = CustomUser

# fieldsets = UserAdmin.fieldsets + (
#     (
#         None,
#         {"fields": ("phone_number",)},
#     ),
# )
# add_fieldsets = UserAdmin.add_fieldsets + (
#     (
#         None,
#         {"fields": ("phone_number",)},
#     ),
# )


admin.site.register(CustomUser)

# Register your models here.
