from .aiding_functions import *
from django.contrib.auth.mixins import UserPassesTestMixin

class AuthorizationMixin(UserPassesTestMixin):
    def test_func(self):
        return is_authorized(self.request.user)