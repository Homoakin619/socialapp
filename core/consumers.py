from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User
from django.core.serializers import serialize

from chat.models import Message,ChatMessage,ChatDate

import json

class RefreshConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id

        await self.accept()

    async def disconnect(self, code):
        return await super().disconnect(code)

    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        messages = await self.refresh_count()
        self.friend_id = data['friend_id']

        if self.friend_id:
            return_value = await self.refresh_chat_history()
            history = return_value['history']
            dates = return_value['dates']
            dates = json.loads(dates)
            history = json.loads(history)
            
            await self.send(text_data=json.dumps({
            'count':messages,'friend_username':self.friend_name,
            'chat_history':history, 'chat_dates':dates
        }))
        else:
            await self.send(text_data=json.dumps({
                'count':messages
            }))
        

    @database_sync_to_async
    def refresh_count(self):
        self.user = User.objects.get(id=self.user_id)
        message_instance = Message.objects.filter(is_read=False,receiver=self.user)
        message_count = message_instance.count()
        return message_count

    @database_sync_to_async
    def refresh_chat_history(self):
        if self.user_id > self.friend_id:
            chat_room = f'chat_{self.user_id}-{self.friend_id}'
        else:
            chat_room = f'chat_{self.friend_id}-{self.user_id}'

        get_user_chats_query = ChatMessage.objects.filter(chatroom=chat_room).order_by('-id')
        chat_date = ChatDate.objects.all()
        friend_name_query = User.objects.get(id=self.friend_id)
        self.friend_name = friend_name_query.username
        

        chat_date = serialize("json",list(chat_date))
        chat_history = serialize('json',list(get_user_chats_query))
        

        return {'history':chat_history,'dates':chat_date}