from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class NotificationType(models.IntegerChoices):
    LIKE = 1, 'Like'
    COMMENT = 2, 'Comment'
    FOLLOW = 3, 'Follow'


class Notification(models.Model):
    verb = models.IntegerField(choices=NotificationType.choices, help_text="Type of notification")
    actor_content_type = models.ForeignKey(ContentType, related_name='actor_notifications', on_delete=models.CASCADE)
    actor_object_id = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'actor_object_id')
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_notifications',
                                            on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')
    action_object_content_type = models.ForeignKey(ContentType, blank=True, null=True,
                                                   related_name='action_object_notifications',
                                                   on_delete=models.CASCADE)
    action_object_object_id = models.PositiveIntegerField(null=True, blank=True)
    action_object = GenericForeignKey('action_object_content_type', 'action_object_object_id')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image = models.ImageField(upload_to='notification', null=True, blank=True)
    is_read = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.get_verb_display())
