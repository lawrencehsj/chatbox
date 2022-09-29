# import json

# from django.test import TestCase
# from django.urls import reverse #allows us to take a path in our urls file to turn it into a url string
# from django.urls import reverse_lazy

# # rest api testing packages
# from rest_framework.test import APIRequestFactory 
# from rest_framework.test import APITestCase

# from .model_factories import *
# from .serializers import *

# # any function that starts with test will be run automatically
# # ==================== ACCOUNT TESTING ======================
# class GroupChatTest(APITestCase):
#     groupchat = None
#     groupchat_message = None

# # create groupchat object 
#     def setUp(self):
#         # instantiate factory objects
#         self.groupchat = GroupChatFactory.create(title='room name')
#         self.groupchat_message = GroupChatMessageFactory.create(pk=123)

#         # instantiate serializer objects
#         self.GroupChatSerializer = GroupChatSerializer(instance=self.groupchat)
#         self.GroupChatMessageSerializer = GroupChatMessageSerializer(instance=self.groupchat_message)

#     def tearDown(self):
#         # GroupChatFactory.objects.all().delete()
#         # GroupChatMessageFactory.objects.all().delete()
#         GroupChatFactory.reset_sequence(0)
#         GroupChatMessageFactory.reset_sequence(0)

#     # =================== SET OF SERIALIZER TESTS ===========================
#     # =================== comment out when necessary =======================
#     # ======================================================================
#     def test_GroupChatSerializer(self):
#         data = self.GroupChatSerializer.data
#         # check for correct keys
#         self.assertEqual(set(data.keys()), set(['title', 'users'])) 
#         # check for correct existing group chat data
#         self.assertEqual(data['title'],'room name')

#     def test_GroupChatMessageSerializer(self):
#         data = self.GroupChatMessageSerializer.data
#         # check for correct keys
#         self.assertEqual(set(data.keys()), set(['user', 'room', 'timestamp', 'content'])) 
#         # check for correct existing group chat data
#         self.assertEqual(data['room'], self.groupchat)


# # ==================== ROUTE TESTING ======================
# class RouteTest(APITestCase):
#     account = None

#     # setup class variables to use for testing
#     # override
#     def setUp(self):
#         # instantiate factory objects
#         self.groupchat = GroupChatFactory.create(title='room name')
#         self.groupchat_message = GroupChatMessageFactory.create(pk=123)

#         # instantiate serializer objects
#         self.GroupChatSerializer = GroupChatSerializer(instance=self.groupchat)
#         self.GroupChatMessageSerializer = GroupChatMessageSerializer(instance=self.groupchat_message)

#         # urls (actions) to handle requests and responses for testing
#         self.create_url = "/groupchat/api/gc"
#         self.account_details_url = reverse('groupchat:groupchat_details_list', kwargs={'pk': 1})
#         self.bad_url = "/groupchat/api/gc/XXX/"

#     # override
#     def tearDown(self):
#         # GroupChatFactory.objects.all().delete()
#         # GroupChatMessageFactory.objects.all().delete()
#         GroupChatFactory.reset_sequence(0)
#         GroupChatMessageFactory.reset_sequence(0)

#     # ======================= SET OF ROUTE TESTS ===========================
#     # ===================== comment out when necessary =====================
#     # ======================================================================

#     def test_GroupChatDetailsReturnsSuccess(self):
#         response = self.client.get(self.groupchat_details_list, format='json') 
#         response.render() 
#         # check for correct arrived data
#         data = json.loads(response.content)
#         # print(data)
#         self.assertTrue('user' in data) # check for username value 
#         self.assertEqual(data['user'], self.account) # check for existing username value loaded