import uuid
from django.core.exceptions import ValidationError
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
    uuid = models.UUIDField(default=uuid.uuid4(), editable=False, primary_key=True)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ('subscriber', 'target')

    def clean(self):
        if self.subscriber == self.target:
            raise ValidationError({"subscriber": ("subscriber cannot be equal to target")})

