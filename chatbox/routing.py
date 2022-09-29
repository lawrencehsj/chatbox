from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from groupchat.consumers import GroupChatConsumer

application = ProtocolTypeRouter({
    # allow domains in settings.py only [ALLOWED_HOSTS]
	'websocket': AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter([
                path('groupchat/<room_id>/', GroupChatConsumer.as_asgi()),
            ]) 
		)
	),
})