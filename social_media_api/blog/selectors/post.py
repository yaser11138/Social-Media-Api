from ..models import Post
from ..filter import PostFilter


def get_post(*,slug):
    try:
        return Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return None


def post_list(*, filters, user):
    following_users = user.following.all().values_list('target', flat=True)
    posts = Post.objects.filter(author__in=following_users)
    if posts:
        return PostFilter(filters, posts)
    else:
        return Post.objects.none()
