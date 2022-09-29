from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models

from groupchat.models import GroupChat, GroupChatMessage

class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['id','title', ]
    search_fields = ['id', 'title', ]

    class Meta:
        model = GroupChat

admin.site.register(GroupChat, GroupChatAdmin)

# Resource: http://masnun.rocks/2017/03/20/django-admin-expensive-count-all-queries/
class CachingPaginator(Paginator):
    """
    caches the number of messages displayed in the chat room to limit excessive loading
    """
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)
            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

class GroupChatMessageAdmin(admin.ModelAdmin):
    list_filter = ['room',  'user', "timestamp"]
    list_display = ['room',  'user', 'content',"timestamp"]
    search_fields = ['room__title', 'user__username','content']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = GroupChatMessage

admin.site.register(GroupChatMessage, GroupChatMessageAdmin)