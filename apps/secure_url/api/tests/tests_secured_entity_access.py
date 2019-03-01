from datetime import timedelta

from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse

from .tests_base import BaseApiTestCase
from ...models import SecuredEntity


class SecuredEntityAccessApiTest(BaseApiTestCase):
    def __finish_create_secured_entity(self):
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)

        self.secured_entity = SecuredEntity.objects.get(pk=self.response.data['id'])

        self.access_url = reverse('secure_url.api:secured-entity-get-access-api-view', args=(self.response.data['id'],))

    def _create_secured_entity_from_url(self):
        self.response = self.client.post(self.list_create_url, self.data_with_url, format='json',
                                         **self.extra_with_permissions)

        self.__finish_create_secured_entity()

    def _create_secured_entity_from_file(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            self.response = self.client.post(self.list_create_url, {'file': file}, format='multipart',
                                             **self.extra_with_permissions)

        self.__finish_create_secured_entity()

    def test_access_secured_entity_from_url_without_password_results_in_400__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_without_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'password': ['This field is required.']}, response.data)

    def test_access_secured_entity_from_url_wrong_password_results_in_400__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_wrong_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'password': ['Password do not match.']}, response.data)

    def test_access_secured_entity_from_url_correct_password_results_in_200__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_url_correct_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'secured_entity': self.data_with_url['url']}, response.data)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_results_in_200__authorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_returns_correct_response__authorized(
            self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'secured_entity': self.data_with_url['url']}, response.data)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_results_in_400__authorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_returns_correct_response__authorized(
            self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({
            "non_field_errors": [
                "Sorry, this secured entity is no longer available."
            ]
        }, response.data)

    def test_access_secured_entity_from_file_without_password_results_in_400__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_without_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'password': ['This field is required.']}, response.data)

    def test_access_secured_entity_from_file_wrong_password_results_in_400__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_wrong_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({'password': ['Password do not match.']}, response.data)

    def test_access_secured_entity_from_file_correct_password_results_in_200__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_file_correct_password_returns_correct_response__authorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertIn('secured_entity', response.data)
        self.assertIn('http://testserver/media/secure_url/files/', response.data['secured_entity'])

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_results_in_200__authorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_returns_correct_response__authorized(
            self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertIn('secured_entity', response.data)
        self.assertIn('http://testserver/media/secure_url/files/', response.data['secured_entity'])

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_results_in_400__authorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_returns_correct_response__authorized(
            self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra_with_permissions)

        self.assertDictEqual({
            "non_field_errors": [
                "Sorry, this secured entity is no longer available."
            ]
        }, response.data)

    def test_access_secured_entity_from_url_without_password_results_in_400__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_without_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra)

        self.assertDictEqual({'password': ['This field is required.']}, response.data)

    def test_access_secured_entity_from_url_wrong_password_results_in_400__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_wrong_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra)

        self.assertDictEqual({'password': ['Password do not match.']}, response.data)

    def test_access_secured_entity_from_url_correct_password_results_in_200__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_url_correct_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_url()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertDictEqual({'secured_entity': self.data_with_url['url']}, response.data)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_results_in_200__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_url_correct_password_just_before_deadline_returns_correct_response__unauthorized(
            self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertDictEqual({'secured_entity': self.data_with_url['url']}, response.data)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_results_in_400__unauthorized(self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_url_correct_password_just_after_deadline_returns_correct_response__unauthorized(
            self):
        self._create_secured_entity_from_url()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertDictEqual({
            "non_field_errors": [
                "Sorry, this secured entity is no longer available."
            ]
        }, response.data)

    def test_access_secured_entity_from_file_without_password_results_in_400__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_without_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {}, format='json',
                                    **self.extra)

        self.assertDictEqual({'password': ['This field is required.']}, response.data)

    def test_access_secured_entity_from_file_wrong_password_results_in_400__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_wrong_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': 'xxx'}, format='json',
                                    **self.extra)

        self.assertDictEqual({'password': ['Password do not match.']}, response.data)

    def test_access_secured_entity_from_file_correct_password_results_in_200__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_file_correct_password_returns_correct_response__unauthorized(self):
        self._create_secured_entity_from_file()

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertIn('secured_entity', response.data)
        self.assertIn('http://testserver/media/secure_url/files/', response.data['secured_entity'])

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_results_in_200__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_access_secured_entity_from_file_correct_password_just_before_deadline_returns_correct_response__unauthorized(
            self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME + timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertIn('secured_entity', response.data)
        self.assertIn('http://testserver/media/secure_url/files/', response.data['secured_entity'])

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_results_in_400__unauthorized(self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_access_secured_entity_from_file_correct_password_just_after_deadline_returns_correct_response__unauthorized(
            self):
        self._create_secured_entity_from_file()

        SecuredEntity.objects.filter(pk=self.secured_entity.pk).update(
            created=self.secured_entity.created - settings.SECURED_ENTITY_ACCESSIBLE_TIME - timedelta(seconds=1))

        response = self.client.post(self.access_url, {'password': self.response.data['password']}, format='json',
                                    **self.extra)

        self.assertDictEqual({
            "non_field_errors": [
                "Sorry, this secured entity is no longer available."
            ]
        }, response.data)
