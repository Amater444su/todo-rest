import datetime
from django.core.cache import cache
from django.conf import settings
import ipdb
from django.utils.deprecation import MiddlewareMixin
from .models import Profile


# class ActiveUserMiddleware(MiddlewareMixin):
#
#     def process_request(self, request):
#         current_user = request.user
#         user_last_login = current_user.last_login
#         user_last_login += datetime.timedelta(seconds=1)
#         if current_user.is_authenticated and current_user.last_login:
#             if user_last_login == current_user.last_login:
#                 pass
#             elif user_last_login < current_user.last_login:
#                 profile = Profile.objects.filter(username=current_user.username).first()
#                 profile.login_count += 1
#                 user_last_login = current_user
#
#         # ipdb.set_trace()