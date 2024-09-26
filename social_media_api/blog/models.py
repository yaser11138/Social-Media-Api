from django.db import models
from social_media_api.common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(BaseModel):
    name = models.CharField(max_length=10)


class Post(BaseModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=10)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Subscribe(BaseModel):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

