from ..models import Subscribe


def get_followings(user):
    return Subscribe.objects.filter(subscriber=user)


def get_followers(user):
    return Subscribe.objects.filter(target=user)


def get_subscribe_detail(uuid):
    subscribe = Subscribe.objects.get(uuid=uuid)
    return subscribe

