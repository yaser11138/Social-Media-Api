from django.core.cache import cache
from django.db.models import Q
from django.contrib.auth import get_user_model

from social_media_api.blog.models import Post
from social_media_api.tasks.tasks import generate_user_feed

User = get_user_model()

class FeedSelector:
    FEED_GENERATION_COOLDOWN = 120  # 2 minute cooldown

    def __init__(self, user):
        self.user = user
        self.cache_key = f"user_feed_{user.id}"

    def get_user_feed(self) -> list:
        """
        Get user's feed from cache or generate new feed
        """
        feed = cache.get(self.cache_key)

        if feed is None:
            feed = self._generate_feed()
            cache.set(self.cache_key, feed, timeout=300)  # Cache for 5 minutes

        return feed

    def _generate_feed(self) -> list:
        """
        Generate fresh feed data for a user
        """
        followed_users = self.user.following.all()
        posts = (
            Post.objects.filter(Q(author__in=followed_users) | Q(author=self.user))
            .select_related("author")
            .order_by("-created_at")[:50]
        )

        return posts
        

    def _handle_async_generation(self, user_id: int):
        """Handle async feed generation with cooldown
            This is for feed generation  in background for feature requests
            so user dosen't have to wait for feed generation when request
        """
        cooldown_key = f"feed_generation_cooldown_{user_id}"
        if not cache.get(cooldown_key):
            generate_user_feed.delay(user_id)
            cache.set(cooldown_key, True, timeout=self.FEED_GENERATION_COOLDOWN)