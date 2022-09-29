import json

from django.test import TestCase
from django.urls import reverse #allows us to take a path in our urls file to turn it into a url string
from django.urls import reverse_lazy

# rest api testing packages
from rest_framework.test import APIRequestFactory 
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

# any function that starts with test will be run automatically
# ==================== ACCOUNT TESTING ======================
class AccountTest(APITestCase):
    account = None

# create account object 
    def setUp(self):
        # instantiate factory objects
        self.account = AccountFactory.create(pk=999)

        # instantiate serializer objects
        self.AccountSerializer = AccountSerializer(instance=self.account)

    def tearDown(self):
        # AccountFactory.objects.all().delete()
        AccountFactory.reset_sequence(0)

    # =================== SET OF SERIALIZER TESTS ===========================
    # =================== comment out when necessary =======================
    # ======================================================================
    def test_AccountSerializer(self):
        data = self.AccountSerializer.data
        # check for correct keys
        self.assertEqual(set(data.keys()), set(['pk', 'email', 'username', 'profile_image', 'is_superuser'])) 
        # check for correct existing account data
        self.assertEqual(data['pk'],999)


# ==================== ROUTE TESTING ======================
class RouteTest(APITestCase):
    account = None

    # setup class variables to use for testing
    # override
    def setUp(self):
        # instantiate factory objects
        self.account = AccountFactory.create(pk=999)

        # urls (actions) to handle requests and responses for testing
        self.create_url = "/account/api/"
        self.account_details_url = reverse('account:account_details_list', kwargs={'pk': 999})
        self.bad_url = "/account/api/XXX/"

    # override
    def tearDown(self):
        # Account.objects.all().delete()
        AccountFactory.reset_sequence(0)

    # ======================= SET OF ROUTE TESTS ===========================
    # ===================== comment out when necessary =====================
    # ======================================================================

    def test_AccountDetailsReturnsSuccess(self):
        response = self.client.get(self.account_details_url, format='json') 
        response.render() 
        # check for correct arrived data
        data = json.loads(response.content)
        # print(data)
        self.assertTrue('username' in data) # check for username value 
        self.assertEqual(data['username'], 'test') # check for existing username value loaded