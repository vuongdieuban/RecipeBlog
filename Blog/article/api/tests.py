# unit test, new blank database

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from article.models import Article
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.test import Client

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER



User = get_user_model()

class ArticleAPITestCase(APITestCase):
    def setUp(self):
        user = User(username='bdvuong', email='bdvuong@gmail.com')
        password = user.set_password('bdvuong1997')
        username = user.username
        user.save()

        # self.client = Client()
        # self.client.login(username=username, password=password)

        article = Article.objects.create(author= user,
                                         title='Original testing recipe',
                                         description='Original description',
                                         ingredient='Original ingres',)


    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)


    def test_single_article(self):
        article_count = Article.objects.count()
        self.assertEqual(article_count, 1)

    # test the get list
    def test_get_list(self):
        data = {}
        url = api_reverse('article-api:article-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    # test the post method
    def test_post_item(self):
        data = {
            'title': 'New title',
            'description':'New stuff',
            'ingredient': 'New ingredient',
        }
        url = api_reverse('article-api:article-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(response.data)
        # somehow giving not authentication were not provided, even in the below with JWT this error occur again

    # get individual item
    def test_get_item(self):
        article = Article.objects.first()
        data = {}
        url = article.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #print(response.data)

    #
    # # Test update and post at this endpoint without authentication
    # def test_update_item(self):
    #     article = Article.objects.first()
    #     url = article.get_api_url()
    #     data = {
    #         'title': 'New title',
    #         'description': 'More New stuff',
    #         'ingredient': 'More new ingredient',
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    #     # Method not allowed expected because we cannot post at this endpoint
    #     #print(response.data)
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     #print(response.data)
    #
    #
    # # Test with authentication thru JWT
    # def test_update_item_with_user(self):
    #     article = Article.objects.first()
    #     print(article.description)
    #     url = article.get_api_url()
    #     data = {
    #         'title': 'New title',
    #         'description': 'More New stuff',
    #         'ingredient': 'More new ingredient',
    #     }
    #     user = User.objects.first()
    #     payload = payload_handler(user)
    #     token_response = encode_handler(payload)
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_response) # setting JWT token headers, JWT <token>
    #     #print(token_response)
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     print(response.data)

    # def test_post_item_with_user(self):
    #     article = Article.objects.first()
    #     #print(article.description)
    #     data = {
    #         'title': 'New title',
    #         'description': 'More New stuff',
    #         'ingredient': 'More new ingredient',
    #     }
    #     user = User.objects.first()
    #     payload = payload_handler(user)
    #     token_response = encode_handler(payload)
    #     self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_response) # setting JWT token headers, JWT <token>
    #     print(token_response)
    #     url = article.get_api_url()
    #     response = self.client.put(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     print(response.data)
