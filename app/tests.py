from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user_model


class AnimalTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username='test',
            password='12test12',
            email='test@example.com'
        )

        self.user = get_user_model().objects.create_user(
            username='ThoaiTran_will_pass_devtest',
            password='12test12',
            email='test@example.com'
        )

    def tearDown(self):
        self.user.delete()

    def test_auth_correct(self):
        user = authenticate(
            username='test',
            password='12test12'
        )
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_auth_wrong_username(self):
        user = authenticate(
            username='wrong',
            password='12test12'
        )
        self.assertFalse(user is not None and user.is_authenticated)

    def test_auth_wrong_password(self):
        user = authenticate(
            username='test',
            password='wrong'
        )
        self.assertFalse(user is not None and user.is_authenticated)

    def test_integration_login(self):
        # Test login and check homepage has Welcome message
        self.client.login(
            username='ThoaiTran_will_pass_devtest',
            password='12test12'
        )

        response = self.client.get('/')

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertTemplateUsed(
            response,
            'home.html'
        )

        self.assertContains(
            response,
            'ThoaiTran_will_pass_devtest'
        )
