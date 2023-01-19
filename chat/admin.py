from django.contrib import admin
from chat.models import ChatDate,ChatMessage,Message

admin.site.register(ChatDate)
admin.site.register(ChatMessage)
admin.site.register(Message)
