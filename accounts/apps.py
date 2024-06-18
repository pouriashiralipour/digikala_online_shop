from django.apps import AppConfig
from django.core.signals import request_finished
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from .models import CustomUser
        from .signals import create_new_user, my_callback, update_user

        request_finished.connect(my_callback)
        post_save.connect(create_new_user, sender=CustomUser)
        post_save.connect(update_user, sender=CustomUser)
