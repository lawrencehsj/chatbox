from enum import Enum
from friend.models import FriendRequest


class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = -1
	SENT_TO_YOU = 0
	SENT_TO_THEM = 1


def get_friend_request_or_false(sender, receiver):
	try:
		return FriendRequest.objects.get(sender=sender, receiver=receiver, is_active=True)
	except FriendRequest.DoesNotExist:
		return False