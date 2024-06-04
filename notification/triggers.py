from django.contrib.auth import get_user_model

from app.models import Like, Comment, Follow
from .models import Notification, NotificationType
from django.contrib.contenttypes.models import ContentType
from .fcm import fcm_send_single, FCMBeam

LIKE_CONTENT_TYPE = ContentType.objects.get_for_model(Like)
COMMENT_CONTENT_TYPE = ContentType.objects.get_for_model(Comment)
FOLLOW_CONTENT_TYPE = ContentType.objects.get_for_model(Follow)


def trigger_like_notification(user_id, event_id, liked_by):
    title = "New Like"
    message = f"{liked_by} liked your post"
    type = "like"
    notification_data = FCMBeam(title, message, type, user_id, event_id)
    user = get_user_model().objects.get(id=user_id)
    notification = Notification.objects.create(
        actor_object_id=user_id,
        actor_content_type=LIKE_CONTENT_TYPE,
        verb=NotificationType.LIKE,
        target_object_id=event_id,
        target_content_type=LIKE_CONTENT_TYPE,
        user=user
    )
    notification.save()
    fcm_send_single(notification_data)


def trigger_comment_notification(user_id, event_id, commenter_name, comment_text):
    title = "New Comment"
    message = f"{commenter_name} commented on your post: {comment_text}"
    type = "comment"
    notification_data = FCMBeam(title, message, type, user_id, event_id)
    user = get_user_model().objects.get(id=user_id)
    notification = Notification.objects.create(
        actor_object_id=user_id,
        actor_content_type=COMMENT_CONTENT_TYPE,
        verb=NotificationType.COMMENT,
        target_object_id=event_id,
        target_content_type=COMMENT_CONTENT_TYPE,
        user=user
    )
    notification.save()
    fcm_send_single(notification_data)


def trigger_follow_notification(user_id, follower_id):
    title = "New Follower"
    message = f"{follower_id} started following you"
    type = "follow"
    notification_data = FCMBeam(title, message, type, user_id)
    user = get_user_model().objects.get(id=user_id)
    follower = get_user_model().objects.get(id=follower_id)
    notification = Notification.objects.create(
        actor_object_id=follower_id,
        actor_content_type=FOLLOW_CONTENT_TYPE,
        verb=NotificationType.FOLLOW,
        user=user
    )
    notification.save()
    fcm_send_single(notification_data)
