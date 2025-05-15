from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.cache import cache
from django.contrib.auth import get_user_model

from social_media_api.blog.models import Post
from social_media_api.blog.selectors.feed import FeedSelector

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "slug"]


class FeedResponseSerializer(serializers.Serializer):
    feed = PostSerializer(many=True)
    count = serializers.IntegerField()
    is_cached = serializers.BooleanField()


class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedResponseSerializer

    def get(self, request: Request) -> Response:
        """
        Get the authenticated user's feed
        """
        try:
            selector = FeedSelector(user=request.user)
            feed_data = selector.get_user_feed()

            # Handle async generation
            selector._handle_async_generation(request.user.id)

            # Add metadata
            response_data = {
                "feed": feed_data,
                "count": len(feed_data),
                "is_cached": bool(feed_data),
            }

            serializer = self.serializer_class(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshFeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedResponseSerializer

    def post(self, request: Request) -> Response:
        """
        Force refresh the authenticated user's feed
        """
        try:
            selector = FeedSelector(user=request.user)
            # Clear cache
            cache.delete(selector.cache_key)
            # Get fresh feed
            feed_data = selector.get_user_feed()

            # Handle async generation
            selector._handle_async_generation(request.user.id)

            # Add metadata
            response_data = {
                "feed": feed_data,
                "count": len(feed_data),
                "is_cached": bool(feed_data),
            }

            serializer = self.serializer_class(response_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
