from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User
from chat.models import Message

import json

class RefreshConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.userId = self.scope['user'].id

        await self.accept()

    async def disconnect(self, code):
        return await super().disconnect(code)

    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        messages = await self.refresh_count()
        await self.send(text_data=json.dumps({
            'count':messages
        }))
        

    @database_sync_to_async
    def refresh_count(self):
        user = User.objects.get(id=self.userId)
        message_instance = Message.objects.filter(is_read=False,receiver=user)
        message_count = message_instance.count()
        return message_count