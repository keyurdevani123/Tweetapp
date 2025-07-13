from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import CustomUser, Tweet, Notification, Like, Message, Comment

# Handle updating follower count on creation or update
@receiver(post_save, sender=CustomUser)
def update_followers_count(sender, instance, created, **kwargs):
    if created or instance.followers.count() != instance.followers_count:
        instance.followers_count = instance.followers.count()
        instance.save()

# # Handle new tweet creation - Notify followers (only if not duplicate)
# @receiver(post_save, sender=Tweet)
# def create_tweet_notification(sender, instance, created, **kwargs):
#     if created:
#         author = instance.user
#         followers = author.followers.exclude(id=author.id).all()
#         for follower in followers:
#             # Create notification if not already exists
#             Notification.objects.get_or_create(
#                 user=follower,
#                 sender=author,
#                 notification_type='tweet',
#                 message=f"{author.username} posted a new tweet: {instance.text[:50]}",
#                 related_tweet=instance
#             )

# # Handle like event - Notify tweet author
# @receiver(post_save, sender=Like)
# def create_like_notification(sender, instance, created, **kwargs):
#     if created:
#         tweet = instance.tweet
#         tweet_author = tweet.user
#         if instance.user != tweet_author:
#             # Create notification if not already exists
#             Notification.objects.get_or_create(
#                 user=tweet_author,
#                 sender=instance.user,
#                 notification_type='like',
#                 message=f"{instance.user.username} liked your tweet: {tweet.text[:50]}",
#                 related_tweet=tweet
#             )

# # Handle follow/unfollow event - Notify user of the follow/unfollow (only if not duplicate)
# @receiver(m2m_changed, sender=CustomUser.followers.through)
# def create_follow_unfollow_notification(sender, instance, action, reverse, model, pk_set, **kwargs):
#     if action in ["add", "remove"]:
#         for follower_id in pk_set:
#             follower = CustomUser.objects.get(id=follower_id)
#             if follower != instance:  # Don't notify the user themselves
#                 action_message = "followed" if action == "add" else "unfollowed"
#                 # Create notification if not already exists
#                 Notification.objects.get_or_create(
#                     user=instance,
#                     sender=follower,
#                     notification_type='follow',
#                     message=f"{follower.username} {action_message} you."
#                 )

# # Handle new message event - Notify recipient of new message
# @receiver(post_save, sender=Message)
# def create_message_notification(sender, instance, created, **kwargs):
#     if created:
#         recipient = instance.recipient
#         if instance.sender != recipient:
#             # Create notification if not already exists
#             Notification.objects.get_or_create(
#                 user=recipient,
#                 sender=instance.sender,
#                 notification_type='message',
#                 message=f"You have a new message from {instance.sender.username}: {instance.content[:50]}",
#                 related_message=instance
#             )

# # Handle comment on tweet event - Notify tweet author of new comment
# @receiver(post_save, sender=Comment)
# def create_comment_notification(sender, instance, created, **kwargs):
#     if created:
#         tweet = instance.tweet
#         tweet_author = tweet.user
#         if instance.user != tweet_author:
#             # Create notification if not already exists
#             Notification.objects.get_or_create(
#                 user=tweet_author,
#                 sender=instance.user,
#                 notification_type='comment',
#                 message=f"{instance.user.username} commented on your tweet: {instance.text[:50]}",
#                 related_tweet=tweet
#             )
