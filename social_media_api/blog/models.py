from django.db import models
from social_media_api.common.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=10)