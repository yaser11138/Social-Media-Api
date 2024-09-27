from django.shortcuts import reverse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.views import extend_schema
from social_media_api.api.mixins import ApiAuthMixin
from social_media_api.api.pagination import LimitOffsetPagination, get_paginated_response
from ..models import Post
from ..services.post import create_post
from ..selectors.post import post_list, get_post


class PostDetailApi(ApiAuthMixin,APIView):
    class PostDetailOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.email

    @extend_schema(
        responses=PostDetailOutputSerializer,
    )
    def get(self, request, slug):
        post = get_post(slug=slug)
        if not post:
            return Response(data={"message": "Post Not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=self.PostDetailOutputSerializer(instance=post), status=status.HTTP_200_OK)


class PostApi(ApiAuthMixin, APIView):

    class Pagination(LimitOffsetPagination):
        limit = 10

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        author__in = serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)
        content = serializers.CharField(required=False, max_length=1000)

    class PostInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=10)
        content = serializers.CharField(max_length=10000)

    class PostOutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Post
            fields = ["url", "author", "title", "content"]

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("api:blog:post_detail", args=(post.slug,))
            return request.build_absolute_uri(path)

        def get_author(self, post):
            return post.author.email

    @extend_schema(request=PostInputSerializer, responses=PostOutputSerializer)
    def post(self, request):
        post_data = self.PostInputSerializer(data=request.data)
        try:
            post_data.is_valid(raise_exception=True)
            post = create_post(user=request.user,
                               title=post_data.validated_data["title"],
                               content=post_data.validated_data["content"])
            return Response(data=self.PostOutputSerializer(instance=post, context={"request": request}).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"Something went Wrong Here is Your error {e}"},
                            status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[FilterSerializer],
        responses=PostOutputSerializer,
    )
    def get(self, request):
        filters = self.FilterSerializer(data=request.query_params)
        try:
            filters.is_valid(raise_exception=True)
            posts = post_list(filters=filters.validated_data, user=request.user)
        except Exception as e:
            return Response(
                data={"message": f"Something went wrong!!!  please try again. Your error {e}"},
                status=status.HTTP_400_BAD_REQUEST)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.PostOutputSerializer,
            queryset=posts,
            request=request,
            view=self
        )