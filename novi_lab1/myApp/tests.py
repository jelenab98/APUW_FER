from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status

from .models import Author, Quote

HOST = 'http://127.0.0.1:8000'
SUPERUSER_NAME = "Jane"
SUPERUSER_EMAIL = "jane.doe@tests.dev"
SUPERUSER_PASSWORD = "password123"


def get_url(url: str):
    if not url.endswith("/"):
        url += "/"
    if not url.startswith("/"):
        url += "/"
    return HOST + url


class TestAPI(APITestCase):

    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    def login(self):
        self.client.login(username=SUPERUSER_NAME, password=SUPERUSER_PASSWORD)

    def logout(self):
        self.client.logout()

    def test_get_api_not_authorized(self):
        url = get_url("/api/")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_api(self):
        self.login()
        url = get_url("/api/")
        response = self.client.get(url, format="json")
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthorTestAPI(APITestCase):

    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    def login(self):
        self.client.login(username=SUPERUSER_NAME, password=SUPERUSER_PASSWORD)

    def logout(self):
        self.client.logout()

    def make_test_Author(self, data={'name': 'TestingAuthor', 'surname': 'Test'}):
        url = get_url("/api/authors/")
        self.login()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.logout()
        return response

    def test_get_Authors_not_authorized(self):
        url = get_url('/api/authors/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_Authors(self):
        url = get_url('/api/authors/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_Author(self):
        self.make_test_Author()
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'TestingAuthor')

    def test_create_Authors(self):
        self.make_test_Author(data={'name': 'TestingAuthor', 'surname': 'Test'})
        self.make_test_Author(data={'name': 'TestingAuthor2', 'surname': 'Test'})
        self.login()
        self.assertEqual(Author.objects.count(), 2)
        Authors = Author.objects.all()
        self.assertEqual(Authors[0].name, 'TestingAuthor')
        self.assertEqual(Authors[1].name, 'TestingAuthor2')
        self.logout()

    def test_get_single_Author(self):
        self.make_test_Author()
        url = get_url('/api/authors/1/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_single_Author(self):
        self.make_test_Author()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/authors/1/')
        data = {'name': 'TestingAuthorUpdated', 'surname': 'Test'}

        self.login()
        response = self.client.put(url, data, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().name, 'TestingAuthorUpdated')

    def test_delete_Author(self):
        self.make_test_Author()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/authors/1/')

        self.login()
        response = self.client.delete(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_create_Author_not_authorized(self):
        url = get_url('/api/authors/')
        data = {'name': 'TestingAuthor', 'surname': 'Test'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_Author_not_authorized(self):
        self.make_test_Author()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/authors/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_single_Author_not_authorized(self):
        self.make_test_Author()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/authors/1/')
        data = {'name': 'TestingAuthorUpdated', 'email': 'test@test.com'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class QuoteTestAPI(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    def login(self):
        self.client.login(username=SUPERUSER_NAME, password=SUPERUSER_PASSWORD)

    def logout(self):
        self.client.logout()

    def make_test_Quote(self, data={"message": "Test message", "author": 1,
                                    "author_name": "Test", "author_surname": "Test"}):
        url_authors = get_url("/api/authors/")
        url_quotes = get_url("/api/quotes/")
        self.login()
        response = self.client.post(url_authors, {"name": data["author_name"],
                                                  "surname": data["author_surname"]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_quotes, {"message": data["message"], "author": data["author"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.logout()
        return response

    def test_get_Quotes_not_authorized(self):
        url = get_url('/api/quotes/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_Quotes(self):
        url = get_url('/api/quotes/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_Quote(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.get().message, 'Test message')

    def test_create_Quotes(self):
        self.make_test_Quote(data={'message': 'Test message 1', 'author': '1', 'author_name': 'TestingAuthor',
                                   'author_surname': 'Test'})
        self.make_test_Quote(data={'message': 'Test message 2', 'author': '2',  'author_name': 'TestingAuthor2',
                                   'author_surname': 'Test'})

        self.assertEqual(Quote.objects.count(), 2)
        Quotes = Quote.objects.all()
        self.assertEqual(Quotes[0].message, 'Test message 1')
        self.assertEqual(Quotes[1].message, 'Test message 2')

    def test_get_single_Quote(self):
        self.make_test_Quote()
        url = get_url('/api/quotes/1/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_single_Quote(self):
        self.make_test_Quote()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/quotes/1/')
        data = {'message': 'Testing Message Updated', 'author': 1}

        self.login()
        response = self.client.put(url, data, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.get().message, 'Testing Message Updated')

    def test_delete_Quote(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/quotes/1/')

        self.login()
        response = self.client.delete(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quote.objects.count(), 0)

    def test_create_Quote_not_authorized(self):
        url = get_url('/api/quotes/')
        data = {'message': 'Testing Message', 'author': None}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_Quote_not_authorized(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/quotes/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_single_Quote_not_authorized(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/quotes/1/')
        data = {'message': 'Testing Message Updated', 'author': '1'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthorQuoteAPI(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(SUPERUSER_NAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD)

    def login(self):
        self.client.login(username=SUPERUSER_NAME, password=SUPERUSER_PASSWORD)

    def logout(self):
        self.client.logout()

    def make_test_Quote(self, data={"message": "Test message", "author": 1,
                                    "author_name": "Test", "author_surname": "Test"}):
        url_authors = get_url("/api/authors/")
        url_quotes = get_url("/api/quotes/")
        self.login()
        if "author_name" in data and "author_surname" in data:
            response = self.client.post(url_authors, {"name": data["author_name"],
                                                      "surname": data["author_surname"]}, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_quotes, {"message": data["message"], "author": data["author"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.logout()
        return response

    def test_get_Quotes_not_authorized(self):
        self.make_test_Quote()
        url = get_url('/api/authors/1/quotes/')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_Quotes(self):
        self.make_test_Quote()
        url = get_url('/api/authors/1/quotes/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_Quotes(self):
        self.make_test_Quote(data={'message': 'Test message 1', 'author': '1', 'author_name': 'TestingAuthor',
                                   'author_surname': 'Test'})
        self.make_test_Quote(data={'message': 'Test message 2', 'author': '1'})

        self.assertEqual(Quote.objects.count(), 2)
        Quotes = Quote.objects.all()
        self.assertEqual(Quotes[0].message, 'Test message 1')
        self.assertEqual(Quotes[1].message, 'Test message 2')

        url = get_url('/api/authors/1/quotes/1')
        self.login()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = get_url('/api/authors/1/quotes/2')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.logout()

    def test_get_single_Quote(self):
        self.make_test_Quote()
        url = get_url('/api/authors/1/quotes/1/')
        self.login()
        response = self.client.get(url, format='json')
        self.logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_single_Quote(self):
        self.make_test_Quote()
        self.assertEqual(Author.objects.count(), 1)

        url = get_url('/api/authors/1/quotes/1/')
        data = {'message': 'Testing Message Updated', 'author': 1}

        self.login()
        response = self.client.put(url, data, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(Quote.objects.get().message, 'Testing Message Updated')

    def test_delete_Quote(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/authors/1/quotes/1/')

        self.login()
        response = self.client.delete(url, format='json')
        self.logout()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quote.objects.count(), 0)

    def test_create_Quote_not_authorized(self):
        url = get_url('/api/authors/1/quotes/')
        data = {'message': 'Testing Message', 'author': None}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_Quote_not_authorized(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/authors/1/quotes/1/')
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_single_Quote_not_authorized(self):
        self.make_test_Quote()
        self.assertEqual(Quote.objects.count(), 1)

        url = get_url('/api/authors/1/quotes/1/')
        data = {'message': 'Testing Message Updated', 'author': '1'}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
