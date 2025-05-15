from typing import Dict, Any
from django.core.cache import cache
from social_media_api.blog.selectors.feed import FeedSelector
from social_media_api.tasks.tasks import generate_user_feed
from social_media_api.users.models import User


class FeedService:
    FEED_GENERATION_COOLDOWN = 120  # 2 minute cooldown

    def __init__(self, user: User):
        self.user = user
        self.selector = FeedSelector(user=user)

    def get_user_feed(self) -> Dict[str, Any]:
        """
        Get user's feed with additional metadata
        """
        feed_data = self.selector.get_user_feed()

        # Only trigger async generation if cooldown has passed
        cooldown_key = f"feed_generation_cooldown_{self.user.id}"
        if not cache.get(cooldown_key):
            generate_user_feed.delay(self.user.id)
            # Set cooldown
            cache.set(cooldown_key, True, timeout=self.FEED_GENERATION_COOLDOWN)

        return {
            "feed": feed_data,
            "count": len(feed_data),
            "is_cached": bool(feed_data),
        }

    def refresh_user_feed(self) -> Dict[str, Any]:
        """
        Force refresh user's feed
        """
        # Clear cache
        cache.delete(self.selector.cache_key)

        # Get fresh feed
        return self.get_user_feed()
