from django.urls import path
from .api.product import ProductView
from .api.post import PostApi, PostDetailApi
from .api.subscribe import SubscribeApi, SubscribeDetailApi

app_name = 'blog'

urlpatterns = [
    path("product", ProductView.as_view(),  name="product"),
    path("post/", PostApi.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailApi.as_view(), name="post-detail"),
    path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
    path("subscribe/<uuid:uuid>",SubscribeDetailApi.as_view(), name="subscribe-detail")
]