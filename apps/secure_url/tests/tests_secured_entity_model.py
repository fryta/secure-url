import tempfile
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse

from ..constants import SecuredEntityTypes
from ..models import SecuredEntity


class SecuredEntityModelTest(TestCase):
    def setUp(self):
        username = 'test'
        password = '123qweasd'

        self.user = get_user_model().objects.create_user(username=username, password=password)

        self.url = 'https://www.facebook.com/'
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')

    def test_new_model_instance_has_proper_type__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertEqual(secured_entity.type, SecuredEntityTypes.LINK)

    def test_new_model_instance_has_proper_password_salt__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertEqual(len(secured_entity.password_salt), 32)

    def test_new_model_instance_has_proper_password__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertEqual(len(secured_entity.password), 12)

    def test_new_model_instance_has_empty_file_and_not_empty_url__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertFalse(secured_entity.file)
        self.assertTrue(secured_entity.url)

    def test_new_model_instance_is_accessible_after_create__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertTrue(secured_entity.is_accessible)

    def test_new_model_instance_is_accessible_just_before_expire__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        SecuredEntity.objects.filter(pk=secured_entity.pk).update(
            created=secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        secured_entity = SecuredEntity.objects.get(pk=secured_entity.pk)

        self.assertTrue(secured_entity.is_accessible)

    def test_new_model_instance_is_not_accessible_just_after_expire__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        SecuredEntity.objects.filter(pk=secured_entity.pk).update(
            created=secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        secured_entity = SecuredEntity.objects.get(pk=secured_entity.pk)

        self.assertFalse(secured_entity.is_accessible)

    def test_new_model_instance_generates_proper_absolute_url__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertEqual(secured_entity.get_absolute_url(), reverse('secure_url:secured-entity-detail-view',
                                                                    kwargs={'pk': secured_entity.pk}))

    def test_new_model_instance_generates_proper_redirect_url__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        self.assertEqual(secured_entity.get_redirect_url(), self.url)

    def test_new_model_instance_regenerates_password_properly__url(self):
        secured_entity = SecuredEntity(user=self.user,
                                       url=self.url)
        secured_entity.save()

        old_password = secured_entity.password
        secured_entity.regenerate_password()

        self.assertNotEqual(old_password, secured_entity.password)

    def test_new_model_instance_has_proper_type__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertEqual(secured_entity.type, SecuredEntityTypes.FILE)

    def test_new_model_instance_has_proper_password_salt__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertEqual(len(secured_entity.password_salt), 32)

    def test_new_model_instance_has_proper_password__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertEqual(len(secured_entity.password), 12)

    def test_new_model_instance_has_empty_url_and_not_empty_file__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertTrue(secured_entity.file)
        self.assertFalse(secured_entity.url)

    def test_new_model_instance_is_accessible_after_create__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertTrue(secured_entity.is_accessible)

    def test_new_model_instance_is_accessible_just_before_expire__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        SecuredEntity.objects.filter(pk=secured_entity.pk).update(
            created=secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        secured_entity = SecuredEntity.objects.get(pk=secured_entity.pk)

        self.assertTrue(secured_entity.is_accessible)

    def test_new_model_instance_is_not_accessible_just_after_expire__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        SecuredEntity.objects.filter(pk=secured_entity.pk).update(
            created=secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        secured_entity = SecuredEntity.objects.get(pk=secured_entity.pk)

        self.assertFalse(secured_entity.is_accessible)

    def test_new_model_instance_generates_proper_absolute_url__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertEqual(secured_entity.get_absolute_url(), reverse('secure_url:secured-entity-detail-view',
                                                                    kwargs={'pk': secured_entity.pk}))

    def test_new_model_instance_generates_proper_redirect_url__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        self.assertEqual(secured_entity.get_redirect_url(),
                         '{}{}'.format(settings.MEDIA_URL.rstrip('/'), self.tmp_file.name))

    def test_new_model_instance_regenerates_password_properly__file(self):
        secured_entity = SecuredEntity(user=self.user,
                                       file=self.tmp_file.name)
        secured_entity.save()

        old_password = secured_entity.password
        secured_entity.regenerate_password()

        self.assertNotEqual(old_password, secured_entity.password)
