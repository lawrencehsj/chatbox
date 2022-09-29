from sqlite3 import Timestamp
from django.utils import timezone
from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
import json

from django.core.serializers.python import Serializer
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday

from groupchat.models import GroupChat, GroupChatMessage

User = get_user_model()

MESSAGE_TYPE_MESSAGE = 0  # For standard messages
MESSAGE_TYPE_CONNECTED_USER_COUNT = 1 # for checking user count message type
DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE = 30


# Example taken from:
# https://github.com/andrewgodwin/channels-examples/blob/master/multichat/chat/consumers.py
class GroupChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Open connection to websocket.
        """
        await self.accept()
        self.room_id = None

    async def disconnect(self, code):
        """
        Close connection to websocket.
        """
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception:
            pass

    async def receive_json(self, content):
        """
        Receive json with different command inputs to send message, join room, leave room, or retrieve messages.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        try:
            if command == "send":
                if len(content["message"].lstrip()) > 0: # if empty message, wont send
                    await self.send_room(content["room_id"],content["message"])

            elif command == 'join':
                await self.join_room(content["room_id"])

            elif command == 'leave':
                await self.leave_room(content["room_id"])

            elif command == "get_group_chat_messages":
                await self.display_progress_spinner(True) # show progress bar
                # retrieve the chat messages from db
                room = await get_room(content['room_id'])
                payload = await get_group_chat_messages(room, content['page_number'])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_messages_payload(payload['messages'], payload['new_page_number'])
                await self.display_progress_spinner(False) # hide progress bar

        except ClientError as e:
            await self.display_progress_spinner(False)
            await self.handle_client_error(e)

    async def send_room(self,room_id,message):
        """
        Called by receive_json when someone sends a message to a room
        """
        if self.room_id != None: #if in room
            if str(room_id) != str(self.room_id): #if room id dont match
                raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
            if not self.scope["user"].is_authenticated:
                raise ClientError("AUTH_ERROR", "User not authenticated")
        else:
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")

        room = await get_room(room_id)
        await create_group_chat_message(room, self.scope['user'], message)

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                "user_id": self.scope["user"].id,
                "message": message,
            }
        )

    async def chat_message(self, event):
        """
        Message created by user.
        """
        # Send a message down to the client
        timestamp = calculate_timestamp(timezone.now())
        await self.send_json(
            {
                "message_type": MESSAGE_TYPE_MESSAGE,
                "profile_image": event["profile_image"],
                "username": event["username"],
                "user_id": event["user_id"],
                "message": event["message"],
                "timestamp" : timestamp,
            },
        )

    async def join_room(self,room_id):
        """
        Connects user to the chat room.
        """
        try:
            room = await get_room(room_id)
        except ClientError as e:
            await self.handle_client_error(e)
        
        # add user to list for room
        if self.scope['user'].is_authenticated:
            await connect_user(room,self.scope['user'])
        
        self.room_id = room_id # room.id or room_id?

        # add to the group to receive room messages
        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name,
        )

        # finish opening the room
        await self.send_json({
            "join": str(room_id),
            # "username": self.scope['user'].username,
        })

        # send the new user count to the room
        # num_connected_users = get_num_connected_users(room)
        await self.channel_layer.group_send(
            room.group_name,
            {
                # the type key is special here because
                # "connected.user.count" will be interpreted as connected_user_count() function
                "type": "connected.user.count", 
                "connected_user_count": get_num_connected_users(room),
                # "connected_user_count": num_connected_users,
            }
        )

    async def leave_room(self,room_id):
        """
        Command sent when a user leaves the room.
        """

        try:
            room = await get_room(room_id)
        except ClientError as e:
            await self.handle_client_error(e)
        
        # remove user from list
        if self.scope['user'].is_authenticated:
            await disconnect_user(room,self.scope['user'])

        self.room_id = None

        # remove from the group
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )

        await self.channel_layer.group_send(
            room.group_name,
            {
                # the type key is special here because
                # "connected.user.count" will be interpreted as connected_user_count() function
                "type": "connected.user.count", 
                "connected_user_count": get_num_connected_users(room),
            }
        )

    async def handle_client_error(self, e):
        """
        Sends error data when faced with existing error.
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
            await self.send_json(errorData)
        return

    async def send_messages_payload(self, messages, new_page_number):
        await self.send_json(
            {
                "messages_payload": "messages_payload",
                "messages": messages,
                "new_page_number": new_page_number,
            },
        )

    async def display_progress_spinner(self, isDisplayed):
        await self.send_json(
            {
                "display_progress_spinner": isDisplayed
            }
        )

    async def connected_user_count(self, event):
        # Send a message down to the client
        await self.send_json(
            {
                "message_type": MESSAGE_TYPE_CONNECTED_USER_COUNT, # 0 for sending message payload, 1 for sending this payload
                "connected_user_count": event["connected_user_count"]
            },
        )


# ============ THIS IS NOT WORKING =================
# @sync_to_async
def get_num_connected_users(room):
    return 20
    # return len(room.users.all())
    # if room.users:
    # 	return len(room.users.all())
    # return 10

    # try:
    # 	if room.users:
    # 		return len(room.users.all())
    # 	return 10
    # except Exception :
    # 	raise ClientError("GET_CONNECTED_USERS_ERROR", "Unable to get connected users.")

@database_sync_to_async
def create_group_chat_message(room,user, message):
    return GroupChatMessage.objects.create(user=user, room=room, content=message)

@database_sync_to_async #accessing db is usually sync, so have to change
def connect_user(room,user):
    return room.connect_user(user) #models function

@database_sync_to_async
def disconnect_user(room,user):
    return room.disconnect_user(user) #models function

@database_sync_to_async
def get_room(room_id):
    try:
        room = GroupChat.objects.get(pk=room_id)
    except GroupChatConsumer.DoesNotExist:
        raise ClientError("ROOM_INVALID", "Invalid room.")
    return room

@database_sync_to_async
def get_group_chat_messages(room, page_number):
    try:
        qs = GroupChatMessage.objects.by_room(room)
        p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

        payload = {}
        new_page_number = int(page_number)  
        if new_page_number <= p.num_pages:
            new_page_number = new_page_number + 1
            s = ChatMessageEncoder()
            payload['messages'] = s.serialize(p.page(page_number).object_list)
        else:
            payload['messages'] = "None"
        payload['new_page_number'] = new_page_number
        return json.dumps(payload)
    except Exception as e:
        print("EXCEPTION: " + str(e))
        return None

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code, message):
        super().__init__(code)
        self.code = code
        if message:
            self.message = message

# Function sourced from codingwithmitch.com
def calculate_timestamp(timestamp):
    """
    1. Today or yesterday:
        - EX: 'today at 10:56 AM'
        - EX: 'yesterday at 5:19 PM'
    2. other:
        - EX: 05/06/2020
        - EX: 12/28/2020
    """
    ts = ""
    # Today or yesterday
    if (naturalday(timestamp) == "today") or (naturalday(timestamp) == "yesterday"):
        str_time = datetime.strftime(timestamp, "%I:%M %p")
        str_time = str_time.strip("0")
        ts = f"{naturalday(timestamp)} at {str_time}"
    # other days
    else:
        str_time = datetime.strftime(timestamp, "%m/%d/%Y")
        ts = f"{str_time}"
    return str(ts)

class ChatMessageEncoder(Serializer):
    def get_dump_object(self, obj):
        dump_object = {}
        dump_object.update({'message_type': MESSAGE_TYPE_MESSAGE})
        dump_object.update({'user_id': str(obj.user.id)})
        dump_object.update({'username': str(obj.user.username)})
        dump_object.update({'message': str(obj.content)})
        dump_object.update({'profile_image': str(obj.user.profile_image.url)})
        dump_object.update({'timestamp': calculate_timestamp(obj.timestamp)})
        return dump_object