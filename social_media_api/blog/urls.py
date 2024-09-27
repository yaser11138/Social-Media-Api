from django.urls import path
from .api.product import ProductView
from .api.post import PostApi, PostDetailApi

app_name = 'blog'

urlpatterns = [
    path("product", ProductView.as_view(),  name="product"),
    path("post/", PostApi.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail" )
]