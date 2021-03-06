"""
Signals for User Manager app.
"""
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserManagerRole


def _upgrade_manager_role_entry(created, user):
    """
    Upgrade an email link to a proper FK link when a manager registers.
    """
    if created and user:
        UserManagerRole.objects.filter(
            unregistered_manager_email=user.email
        ).update(
            unregistered_manager_email=None,
            manager_user=user,
        )


@receiver(post_save, sender=User)
def upgrade_manager_role_entry(sender, **kwargs):  # pylint: disable=unused-argument
    """
    Call function to upgrade user-manager link to proper FK.
    """
    created = kwargs.get('created')
    user = kwargs.get('instance')
    _upgrade_manager_role_entry(created, user)
