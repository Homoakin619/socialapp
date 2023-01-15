from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import json
from datetime import date
from chat.models import ChatDate,ChatMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        friend_id = self.scope['url_route']['kwargs']['id']
        if int(user_id) > int(friend_id):
            room_name = f'{user_id}-{friend_id}'
        else:
            room_name = f'{friend_id}-{user_id}'
        self.room_group_name = 'chat_%s' % room_name

        await self.channel_layer.group_add(
            self.room_group_name,self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,self.channel_name
        )
        

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'username':data['username'],
                'message':data['message']
            }
        )

        await self.save_message(data['username'],data['message'],self.room_group_name)
        

    async def chat_message(self,event):
        await self.send(
            text_data=json.dumps({
                'username':event['username'],
                'message':event['message']
            })
        )
    @database_sync_to_async
    def save_message(self,sender,message,chatroom):
        today = date.today()
        chatdate,created = ChatDate.objects.get_or_create(timestamp=today)

        chat = ChatMessage.objects.create(date=chatdate,sender=sender,
                                chatroom=chatroom,message=message)
        chat.save()