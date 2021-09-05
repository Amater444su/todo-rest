import ipdb
from django.contrib.auth.signals import user_logged_in
from djoser.utils import login_user
from todo.models import Profile
from django.dispatch import receiver
from django.core.cache import cache


@receiver(user_logged_in, sender=Profile)
def login_success(sender, request, user, **kwargs):
    user.login_count += 1
    user.save()


    # ct = cache.get('count', 0, version=user.pk)
    # newcount = ct + 1
    # cache.set('count', newcount, 60*60*24, version=user.pk)
