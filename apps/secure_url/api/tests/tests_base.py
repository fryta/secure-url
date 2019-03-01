import tempfile
from base64 import b64encode

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BaseApiTestCase(APITestCase):
    def setUp(self):
        username = 'test'
        password = '123qweasd'

        self.list_create_url = reverse('secure_url.api:secured-entity-list')
        self.user = get_user_model().objects.create_user(username=username, password=password)
        self.extra = {
            'HTTP_USER_AGENT': 'Test Browser'
        }
        self.extra_with_permissions = dict(self.extra, HTTP_AUTHORIZATION='Basic {}'.format(
            b64encode('{}:{}'.format(username, password).encode()).decode('utf-8')))
        self.data_with_url = {
            'url': 'https://www.facebook.com'
        }

    def _get_tmp_file(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')

        image = Image.new('RGB', (100, 100))
        image.save(tmp_file)

        return tmp_file
