from django.db import models
from django.conf import settings


class GroupChat(models.Model):
	title = models.CharField(max_length=255, unique=True, blank=False,)
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="connected users to chat room.")

	def __str__(self):
		return self.title #return room name

	def connect_user(self, user):
		"""
		return true if user is added to the users list
		"""
		is_user_added = False
		if not user in self.users.all():
			self.users.add(user)
			self.save()
			is_user_added = True
		elif user in self.users.all():
			is_user_added = True
		return is_user_added 

	def disconnect_user(self, user):
		"""
		return true if user is removed from the users list
		"""
		is_user_removed = False
		if user in self.users.all():
			self.users.remove(user)
			self.save()
			is_user_removed = True
		return is_user_removed 

	@property
	def group_name(self):
		"""
		Returns the Channels Group name that sockets should subscribe to to get sent
		messages as they are generated.
		"""
		return "GroupChat-%s" % self.id


class GroupChatManager(models.Manager):
    def by_room(self, room):
		# filter and order by timestamp
        qs = GroupChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs

class GroupChatMessage(models.Model):
    """
    Chat message created by a user inside a GroupChat
    """
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room       = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    timestamp  = models.DateTimeField(auto_now_add=True)
    content    = models.TextField(unique=False, blank=False,)

    objects = GroupChatManager()

    def __str__(self):
        return self.content