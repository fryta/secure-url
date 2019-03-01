import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls.base import reverse


class BaseViewTest(TestCase):
    def setUp(self):
        self.create_url = reverse('secure_url:secured-entity-create-view')
        self.login_url = reverse('accounts-login')

        self.username = 'test'
        self.password = '123qweasd'

        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

        self.data_with_url = {
            'url': 'https://www.facebook.com/'
        }

    def _get_tmp_file(self):
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')

        image = Image.new('RGB', (100, 100))
        image.save(tmp_file)

        return tmp_file

    def _login_user(self):
        self.client.login(username=self.username, password=self.password)
