from rest_framework import status

from .tests_base_view import BaseViewTest
from ..constants import SecuredEntityTypes
from ..models import SecuredEntity


class SecuredEntityCreateViewTest(BaseViewTest):
    def test_create_secured_entity_has_to_be_authenticated(self):
        response = self.client.get(self.create_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_unauthenticated_create_secured_entity_returns_correct_response(self):
        response = self.client.get(self.create_url)

        self.assertEqual(response['Location'], '/login/?next={}'.format(self.create_url))

    def test_create_secured_entity_renders_proper_form(self):
        self._login_user()

        response = self.client.get(self.create_url)

        self.assertContains(response, 'Please insert URL or upload a file you want to secure.')
        self.assertContains(response,
                            '<textarea class="materialize-textarea" cols="40" id="id_url" name="url" rows="10"></textarea>')
        self.assertContains(response, 'type="file" name="file"')
        self.assertContains(response, '<button type="submit" class="btn">Submit</button>')

    def test_create_secured_entity_without_payload_returns_correct_response(self):
        self._login_user()

        response = self.client.post(self.create_url, {})

        self.assertContains(response, 'You have to provide either url or file.')

    def test_create_secured_entity_with_wrong_url_returns_correct_response(self):
        self._login_user()

        response = self.client.post(self.create_url, {'url': 'xxx'})

        self.assertContains(response, 'Enter a valid URL')

    def test_successful_create_secured_entity_from_url_results_in_302(self):
        self._login_user()

        response = self.client.post(self.create_url, self.data_with_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_successful_create_secured_entity_from_url_returns_correct_redirect(self):
        self._login_user()

        response = self.client.post(self.create_url, self.data_with_url)

        self.assertRegexpMatches(response['Location'], r'^\/secure-url\/[a-zA-Z0-9-]{36}\?created=1')

    def test_successful_create_secured_entity_from_url_returns_correct_response(self):
        self._login_user()

        response = self.client.post(self.create_url, self.data_with_url, follow=True)

        self.assertContains(response, 'Thank you for uploading this item.')
        self.assertContains(response, 'Secured URL for uploaded entity:')
        self.assertContains(response, 'Password:')

    def test_successful_create_secured_entity_from_url_creates_proper_object(self):
        self._login_user()

        self.client.post(self.create_url, self.data_with_url)

        secured_entity = SecuredEntity.objects.first()

        self.assertTrue(secured_entity.password_salt)
        self.assertEqual(secured_entity.user, self.user)
        self.assertEqual(SecuredEntityTypes.LINK, secured_entity.type)
        self.assertEqual(self.data_with_url['url'], secured_entity.url)
        self.assertFalse(secured_entity.file)

    def test_successful_create_secured_entity_from_file_results_in_302(self):
        self._login_user()
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.create_url, {'file': file})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_successful_create_secured_entity_from_file_returns_correct_redirect(self):
        self._login_user()
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.create_url, {'file': file})

        self.assertRegexpMatches(response['Location'], r'^\/secure-url\/[a-zA-Z0-9-]{36}\?created=1')

    def test_successful_create_secured_entity_from_file_returns_correct_response(self):
        self._login_user()
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.create_url, {'file': file}, follow=True)

        self.assertContains(response, 'Thank you for uploading this item.')
        self.assertContains(response, 'Secured URL for uploaded entity:')
        self.assertContains(response, 'Password:')

    def test_successful_create_secured_entity_from_file_creates_proper_object(self):
        self._login_user()
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            self.client.post(self.create_url, {'file': file})

        secured_entity = SecuredEntity.objects.first()

        self.assertTrue(secured_entity.password_salt)
        self.assertEqual(secured_entity.user, self.user)
        self.assertEqual(SecuredEntityTypes.FILE, secured_entity.type)
        self.assertTrue(secured_entity.file)
        self.assertFalse(secured_entity.url)

    def test_create_secured_entity_from_file_and_url_returns_correct_response(self):
        self._login_user()
        tmp_file = self._get_tmp_file()

        with open(tmp_file.name, 'rb') as file:
            response = self.client.post(self.create_url, dict(self.data_with_url, file=file))

        self.assertContains(response, 'provide both url or file.')
