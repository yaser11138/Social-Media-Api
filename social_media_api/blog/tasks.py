from time import sleep
from celery import shared_task
from celery import shared_task
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from social_media_api.blog.models import Post

User = get_user_model()

@shared_task
def generate_user_feed(user_id):
    """
    Generate and cache a user's feed
    """
    try:
        user = User.objects.get(id=user_id)

        # Get posts from followed users and the user's own posts
        followed_users = user.following.all()
        posts = Post.objects.filter(
            Q(author__in=followed_users) | Q(author=user)
        ).order_by("-created_at")[
            :50
        ]  # Limit to 50 most recent posts

        # Prepare feed data
        feed_data = []
        for post in posts:
            feed_data.append(
                {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "author": {"id": post.author.id, "username": post.author.username},
                    "created_at": post.created_at,
                }
            )

        # Cache the feed
        cache_key = f"user_feed_{user_id}"
        cache.set(cache_key, feed_data, timeout=300)  # Cache for 5 minutes

        return f"Feed generated for user {user.username}"
    except User.DoesNotExist:
        return "User not found"


@shared_task
def update_feeds_for_followers(user_id, post_id):
    """
    Update feeds for all followers when a user creates a new post
    """
    try:
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)

        # Get all followers
        followers = user.followers.all()

        for follower in followers:
            # Trigger feed generation for each follower
            generate_user_feed.delay(follower.id)

        return f"Feeds updated for {followers.count()} followers"
    except (User.DoesNotExist, Post.DoesNotExist):
        return "User or Post not found"

@shared_task
def send_follow_notification(follower_id, followed_id):
    """
    Send notification when a user follows another user
    """
    try:
        follower = User.objects.get(id=follower_id)
        followed = User.objects.get(id=followed_id)

        # to-do:
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



@shared_task
def cleanup_old_notifications():
    """
    Clean up notifications older than 7 days
    """
    # This is a periodic task that should be run daily
    cutoff_date = timezone.now() - timedelta(days=7)

    #to-do

    return "Old notifications cleaned up"
