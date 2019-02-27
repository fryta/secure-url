from django.contrib.auth import get_user_model
from django.db import models


class UserAgentLog(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.user_agent, self.created)

    class Meta:
        ordering = ('-created',)
