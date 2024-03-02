from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy, gettext as _


class CustomUser(AbstractUser):
    pass

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _("accounts")
