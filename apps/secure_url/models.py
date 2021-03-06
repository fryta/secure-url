import uuid
from hashlib import md5

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .constants import SecuredEntityTypes


class SecuredEntity(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    password_salt = models.CharField(max_length=32)
    url = models.TextField(null=True, default=None, blank=True, validators=[URLValidator()])
    file = models.FileField(upload_to='secure_url/files', null=True, default=None, blank=True)
    type = models.CharField(max_length=10, choices=SecuredEntityTypes.get_choices(), default=SecuredEntityTypes.LINK)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def password(self):
        return md5('{}-{}'.format(self.password_salt, self.pk).encode('utf-8')).hexdigest()[:12]

    @property
    def is_accessible(self):
        return self.created + settings.SECURED_ENTITY_ACCESSIBLE_TIME > timezone.now()

    def save(self, *args, **kwargs):
        if not self.password_salt:
            self.password_salt = self.generate_password_salt()

        self.type = SecuredEntityTypes.LINK if self.url else SecuredEntityTypes.FILE

        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('secure_url:secured-entity-detail-view', kwargs={'pk': self.pk})

    def get_redirect_url(self):
        return self.url if self.url else self.file.url

    def regenerate_password(self):
        self.password_salt = self.generate_password_salt()
        self.save(update_fields=['password_salt'])

    def generate_password_salt(self):
        return md5('SecureUrlHashing{}-z`xcvge-{}--{}'.format(settings.SECRET_KEY,
                                                              timezone.now(),
                                                              self.created).encode('utf-8')).hexdigest()

    def __str__(self):
        return '{} - {}'.format(self.user, self.created)

    class Meta:
        ordering = ('-created',)


class SecuredEntityAccessLog(models.Model):
    secured_entity = models.ForeignKey(SecuredEntity, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Secured item: {} visited: {}'.format(self.secured_entity, self.created)

    class Meta:
        ordering = ('-created',)
