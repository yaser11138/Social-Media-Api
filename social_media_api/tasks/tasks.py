from celery import shared_task
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from social_media_api.blog.models import Post

User = get_user_model()


@shared_task
def send_follow_notification(follower_id, followed_id):
    """
    Send notification when a user follows another user
    """
    try:
        follower = User.objects.get(id=follower_id)
        followed = User.objects.get(id=followed_id)

        # Here you would typically:
        # 1. Create a notification record
        # 2. Send push notification if enabled
        # 3. Send email notification if enabled

        notification_data = {
            "type": "follow",
            "follower_name": follower.username,
            "follower_id": follower.id,
            "timestamp": timezone.now(),
        }

        # Store notification in cache for real-time access
        cache_key = f"notifications_{followed_id}"
        notifications = cache.get(cache_key, [])
        notifications.append(notification_data)
        cache.set(cache_key, notifications, timeout=3600)  # Cache for 1 hour

        return f"Notification sent to {followed.username} about new follower {follower.username}"
    except User.DoesNotExist:
        return "User not found"


