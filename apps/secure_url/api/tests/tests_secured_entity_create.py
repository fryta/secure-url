from rest_framework import status
from rest_framework.reverse import reverse

from .tests_base import BaseApiTestCase
from ...constants import SecuredEntityTypes
from ...models import SecuredEntity


class SecuredEntityCreateApiTest(BaseApiTestCase):
    def test_create_secured_entity_has_to_be_authenticated(self):
        response = self.client.post(self.list_create_url, self.data_with_url, format='json', **self.extra)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_unauthenticated_create_secured_entity_returns_correct_response(self):
        response = self.client.post(self.list_create_url, self.data_with_url, format='json', **self.extra)

        self.assertEqual(u'Authentication credentials were not provided.', response.data['detail'])

    def test_create_secured_entity_without_payload_results_in_400(self):
        response = self.client.post(self.list_create_url, {}, format='json', **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_secured_entity_without_payload_returns_correct_response(self):
        response = self.client.post(self.list_create_url, {}, format='json', **self.extra_with_permissions)

        self.assertDictEqual({
            "non_field_errors": [
                "You have to provide either url or file."
            ]
        }, response.data)

    def test_create_secured_entity_with_wrong_url_results_in_400(self):
        response = self.client.post(self.list_create_url, {'url': 'xxx'}, format='json', **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_secured_entity_with_wrong_url_returns_correct_response(self):
        response = self.client.post(self.list_create_url, {'url': 'xxx'}, format='json', **self.extra_with_permissions)

        self.assertDictEqual({
            "url": [
                "Enter a valid URL."
            ]
        }, response.data)

    def test_successful_create_secured_entity_from_url_results_in_201(self):
        response = self.client.post(self.list_create_url, self.data_with_url, format='json',
                                    **self.extra_with_permissions)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_successful_create_secured_entity_from_url_creates_proper_object(self):
        response = self.client.post(self.list_create_url, self.data_with_url, format='json',
                                    **self.extra_with_permissions)

        secured_entity = SecuredEntity.objects.get(pk=response.data['id'])

        self.assertTrue(secured_entity.password_salt)
        self.assertEqual(secured_entity.user, self.user)
        self.assertEqual(SecuredEntityTypes.LINK, secured_entity.type)
        self.assertEqual(self.data_with_url['url'], secured_entity.url)
        self.assertFalse(secured_entity.file)

    def test_successful_create_secured_entity_from_url_creates_proper_response(self):
        response = self.client.post(self.list_create_url, self.data_with_url, format='json',
                                    **self.extra_with_permissions)

        self.assertListEqual(['id', 'type', 'created', 'password', 'is_accessible', 'access_url'],
                             list(response.data.keys()))
        self.assertEqual(SecuredEntityTypes.LINK, response.data['type'])
        self.assertTrue(response.data['is_accessible'])
        self.assertEqual('http://testserver{}'.format(
            reverse('secure_url.api:secured-entity-get-access-api-view', args=(response.data['id'],))),
            response.data['access_url'])
        self.assertTrue(response.data['password'])

    def test_successful_create_secured_entity_from_file_results_in_201(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.list_create_url, {'file': file}, format='multipart',
                                        **self.extra_with_permissions)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_successful_create_secured_entity_from_file_creates_proper_object(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.list_create_url, {'file': file}, format='multipart',
                                        **self.extra_with_permissions)

        secured_entity = SecuredEntity.objects.get(pk=response.data['id'])

        self.assertTrue(secured_entity.password_salt)
        self.assertEqual(secured_entity.user, self.user)
        self.assertEqual(SecuredEntityTypes.FILE, secured_entity.type)
        self.assertTrue(secured_entity.file)
        self.assertFalse(secured_entity.url)

    def test_successful_create_secured_entity_from_file_creates_proper_response(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.list_create_url, {'file': file}, format='multipart',
                                        **self.extra_with_permissions)

        self.assertListEqual(['id', 'type', 'created', 'password', 'is_accessible', 'access_url'],
                             list(response.data.keys()))
        self.assertEqual(SecuredEntityTypes.FILE, response.data['type'])
        self.assertTrue(response.data['is_accessible'])
        self.assertEqual('http://testserver{}'.format(
            reverse('secure_url.api:secured-entity-get-access-api-view', args=(response.data['id'],))),
            response.data['access_url'])
        self.assertTrue(response.data['password'])

    def test_create_secured_entity_from_file_and_url_results_in_400(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.list_create_url, dict(self.data_with_url, file=file),
                                        format='multipart',
                                        **self.extra_with_permissions)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_secured_entity_from_file_and_url_returns_correct_response(self):
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.list_create_url, dict(self.data_with_url, file=file),
                                        format='multipart',
                                        **self.extra_with_permissions)

        self.assertDictEqual({
            "non_field_errors": [
                "You can't provide both url or file."
            ]
        }, response.data)
