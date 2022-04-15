import hashlib
import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.utils.http import urlencode

logger = logging.getLogger("engine")


def upload_avatar_to(instance, filename, uid=None):
    filename, ext = os.path.splitext(filename)
    uid = uid or uuid.uuid4()
    return os.path.join(
        "avatar_images",
        "avatar_{uuid}_{filename}{ext}".format(
            uuid=uid,
            filename=filename,
            ext=ext,
        ),
    )


def get_bot_user():
    User = get_user_model()
    bot_username = getattr(settings, "BOT_USERNAME", None)
    if bot_username:
        bot = User.objects.get(username=bot_username)
    else:
        bot = User.objects.filter(is_superuser=True).first()
    return bot


def get_perms(actions, model):
    """returns"""
    from django.contrib.auth import get_permission_codename
    from django.contrib.auth.models import Permission

    perms = []
    for act in actions:
        perm_name = get_permission_codename(act, model._meta)
        try:
            perm = Permission.objects.get(codename=perm_name)
            perms.append(perm)
        except Permission.DoesNotExist:
            continue
    return tuple(perms)


def get_perms_dict(actions, model):
    """returns"""
    from django.contrib.auth import get_permission_codename
    from django.contrib.auth.models import Permission

    perms = dict()
    for act in actions:
        perm_name = get_permission_codename(act, model._meta)
        try:
            perm = Permission.objects.filter(codename=perm_name).first()
            perms[act] = perm
        except Permission.DoesNotExist:
            continue
    return perms


def add_perms(group_names, permission_list):
    for perm_obj in permission_list:
        if isinstance(group_names, list):
            actors = group_names
        else:
            actors = [group_names]
        for actor in actors:
            actor.permissions.add(perm_obj)


def add_group_perms(group, perm_dict, actions):
    perms = list()
    for key in actions:
        perms.append(perm_dict[key])
    add_perms(group, perms)


def get_gravatar_url(email, size=50):
    default = "mm"
    size = int(size) * 2  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = "//www.gravatar.com/avatar"

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip("/"),
        hash=hashlib.md5(email.lower().encode("utf-8")).hexdigest(),
        params=urlencode({"s": size, "d": default}),
    )
    return gravatar_url


def get_users_online(request):
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get("_auth_user_id", None))
    # Query all logged in users based on id list
    return get_user_model().objects.filter(id__in=uid_list)


def create_demo_users(users_and_group):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    User = get_user_model()
    password = "demo_pwd"
    for username, group_name in users_and_group.items():
        try:
            user = User.objects.get(username=username)
            print("%s has been created" % user)
        except User.DoesNotExist:
            name = username.split("_")
            print(name)
            first_name = name[0]
            last_name = name[1]
            user = User.objects.create_user(
                username=username,
                password=password,
                email="%s@gmail.com" % username,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=False,
            )
            print("Create new user %s" % user)
        user.save()

        if group_name is not None:
            group, _ = Group.objects.get_or_create(name=group_name)
            group.user_set.add(user)
            print("Add %s to '%s' group" % (user, group))
