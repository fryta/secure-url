from rest_framework import status
from django.urls.base import reverse
from django.conf import settings
from datetime import timedelta
from .tests_base_view import BaseViewTest
from ..models import SecuredEntity


class SecuredEntityAccessViewTest(BaseViewTest):
    def __finish_create_secured_entity(self, response):
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.secured_entity = SecuredEntity.objects.first()

        self.access_url = reverse('secure_url:secured-entity-access-view', args=(self.secured_entity.pk,))

        self.client.logout()

    def _create_secured_entity_from_url(self):
        self._login_user()

        response = self.client.post(self.create_url, self.data_with_url)

        self.__finish_create_secured_entity(response)

    def _create_secured_entity_from_file(self):
        self._login_user()

        self.tmp_file = self._get_tmp_file()

        with open(self.tmp_file.name, 'rb') as file:
            response = self.client.post(self.create_url, {'file': file})

        self.__finish_create_secured_entity(response)

    def test_access_secured_entity_from_url_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Please provide password in order to access this secured entity.')
        self.assertContains(response, '<input id="id_password" name="password" type="text">')
        self.assertContains(response, 'Go go go!')

    def test_access_secured_entity_from_url_without_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk})

        self.assertContains(response, 'This field is required')

    def test_access_secured_entity_from_url_wrong_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk, 'password': 'xxx'})

        self.assertContains(response, 'Password do not match')

    def test_access_secured_entity_from_url_correct_password_results_in_302__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_url_correct_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response['Location'], self.secured_entity.url)


    def test_access_secured_entity_from_url_correct_password_just_before_deadline_results_in_302__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response['Location'], self.secured_entity.url)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_url_just_after_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_file_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Please provide password in order to access this secured entity.')
        self.assertContains(response, '<input id="id_password" name="password" type="text">')
        self.assertContains(response, 'Go go go!')

    def test_access_secured_entity_from_file_without_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk})

        self.assertContains(response, 'This field is required')

    def test_access_secured_entity_from_file_wrong_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk, 'password': 'xxx'})

        self.assertContains(response, 'Password do not match')

    def test_access_secured_entity_from_file_correct_password_results_in_302__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_file_correct_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertIn(settings.MEDIA_URL, response['Location'])
        self.assertIn(self.tmp_file.name.split('/')[-1], response['Location'])


    def test_access_secured_entity_from_file_correct_password_just_before_deadline_results_in_302__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertIn(settings.MEDIA_URL, response['Location'])
        self.assertIn(self.tmp_file.name.split('/')[-1], response['Location'])

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_file_just_after_deadline_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()
        self._login_user()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_url_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Please provide password in order to access this secured entity.')
        self.assertContains(response, '<input id="id_password" name="password" type="text">')
        self.assertContains(response, 'Go go go!')

    def test_access_secured_entity_from_url_without_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk})

        self.assertContains(response, 'This field is required')

    def test_access_secured_entity_from_url_wrong_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk, 'password': 'xxx'})

        self.assertContains(response, 'Password do not match')

    def test_access_secured_entity_from_url_correct_password_results_in_302__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_url_correct_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response['Location'], self.secured_entity.url)


    def test_access_secured_entity_from_url_correct_password_just_before_deadline_results_in_302__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response['Location'], self.secured_entity.url)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_url_just_after_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_file_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Please provide password in order to access this secured entity.')
        self.assertContains(response, '<input id="id_password" name="password" type="text">')
        self.assertContains(response, 'Go go go!')

    def test_access_secured_entity_from_file_without_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk})

        self.assertContains(response, 'This field is required')

    def test_access_secured_entity_from_file_wrong_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk, 'password': 'xxx'})

        self.assertContains(response, 'Password do not match')

    def test_access_secured_entity_from_file_correct_password_results_in_302__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_file_correct_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertIn(settings.MEDIA_URL, response['Location'])
        self.assertIn(self.tmp_file.name.split('/')[-1], response['Location'])


    def test_access_secured_entity_from_file_correct_password_just_before_deadline_results_in_302__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertIn(settings.MEDIA_URL, response['Location'])
        self.assertIn(self.tmp_file.name.split('/')[-1], response['Location'])

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'id': self.secured_entity.pk,
                                                      'password': self.secured_entity.password})

        self.assertContains(response, 'Sorry, this secured entity is no longer available')

    def test_access_secured_entity_from_file_just_after_deadline_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.get(self.access_url)

        self.assertContains(response, 'Sorry, this secured entity is no longer available')
