from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actions'
    )
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor} {self.verb} {self.target} → {self.recipient}" '