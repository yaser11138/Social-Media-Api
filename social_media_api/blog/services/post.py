from ..models import Post
from django.utils.text import slugify


def create_post(user,title,content):
    slug = slugify(title)
    post = Post(slug=slug,title=title,content=content,author=user)
    post.save()
    return post