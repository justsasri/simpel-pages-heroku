from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from .utils import get_gravatar_url


class User(AbstractUser):
    @cached_property
    def avatar(self):
        return self.get_avatar()

    def get_avatar(self):
        return get_gravatar_url(self.email)
