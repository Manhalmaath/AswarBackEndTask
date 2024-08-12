from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Service, Tag, User, Credential


class CredentialAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Register and login admin user
        admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password1': 'AdminPass123!',
            'password2': 'AdminPass123!',
            'first_name': 'Admin',
            'last_name': 'User'
        }
        response = self.client.post(reverse('register'), admin_data)
        self.admin_token = response.data['token']['access_token']
        self.admin_user = User.objects.get(username='admin')
        self.admin_user.is_superuser, self.admin_user.is_staff = True, True
        self.admin_user.save()

        # Register and login regular user
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(reverse('register'), user_data)
        self.user_token = response.data['token']['access_token']
        self.user = User.objects.get(username='testuser')

        # Create test service and tag
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        self.service_id = self.client.post(reverse('service-list-create'), {'name': 'TestService'}).data['id']
        self.tag_id = self.client.post(reverse('tag-list-create'), {'name': 'TestService'}).data['id']

        # Create test credential using API
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        response = self.client.post(reverse('create-credential'), {
            'name': 'TestCredential',
            'service': self.service_id,
            'username': 'testusername',
            'password': 'TestPass',
            'tags': [self.tag_id]
        })
        self.credential = response.data

    def tearDown(self):
        self.client.credentials()

    def test_list_credentials_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        response = self.client.get(reverse('list-credentials'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_credentials_unauthenticated(self):
        self.tearDown()
        response = self.client.get(reverse('list-credentials'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_credentials_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.admin_token)
        response = self.client.get(reverse('list-credentials'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_credentials_filter_by_service(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        response = self.client.get(reverse('list-credentials'), {'service': 'TestService'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_credentials_filter_by_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        response = self.client.get(reverse('list-credentials'), {'tag': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_credential_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        data = {
            'name': 'NewCredential',
            'service': self.service_id,
            'username': 'newusername',
            'password': 'NewPass123!',
            'tags': [self.tag_id]
        }
        response = self.client.post(reverse('create-credential'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Credential.objects.count(), 2)

    def test_update_credential_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.user_token)
        data = {
            'name': 'UpdatedCredential',
            'password': 'UpdatedPass123!'
        }
        response = self.client.patch(reverse('update-credential', kwargs={'pk': self.credential['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.credential = response.data
        self.assertEqual(self.credential['name'], 'UpdatedCredential')

    def test_update_credential_non_owner(self):
        # Create another user
        another_user_data = {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'password1': 'AnotherPass123!',
            'password2': 'AnotherPass123!',
            'first_name': 'Another',
            'last_name': 'User'
        }
        response = self.client.post(reverse('register'), another_user_data)
        another_user_token = response.data['token']['access_token']

        self.client.credentials(HTTP_AUTHORIZATION=another_user_token)
        data = {
            'name': 'UpdatedCredential',
            'password': 'UpdatedPass123!'
        }
        response = self.client.patch(reverse('update-credential', kwargs={'pk': self.credential['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_credential_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.admin_token)
        data = {
            'name': 'AdminUpdatedCredential',
            'password': 'AdminUpdatedPass123!'
        }
        response = self.client.patch(reverse('update-credential', kwargs={'pk': self.credential['id']}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.credential = response.data
        self.assertEqual(self.credential['name'], 'AdminUpdatedCredential')
