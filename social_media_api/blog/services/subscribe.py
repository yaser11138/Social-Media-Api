from django.contrib.auth import get_user_model
from django.contrib.auth import PermissionDenied
from ..models import Subscribe

User = get_user_model()


def create_subscribe(subscriber, target_email):
    target = User.objects.get(email=target_email)
    sub = Subscribe(subscriber=subscriber, target=target)
    sub.full_clean()
    sub.save()
    return sub


def delete_subscribe(uuid, user):
    subscribe = Subscribe.objects.get(uuid=uuid)
    if subscribe.subscriber == user:
        subscribe.delete()
    else:
        raise PermissionDenied("You don't have permission to delete this")
