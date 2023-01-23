from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

import json
from datetime import date
from chat.models import ChatDate,ChatMessage,Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        self.friend_id = self.scope['url_route']['kwargs']['id']
        if int(user_id) > int(self.friend_id):
            room_name = f'{user_id}-{self.friend_id}'
        else:
            room_name = f'{self.friend_id}-{user_id}'
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
        await self.notify_message(
            self.friend_id,
            self.scope['user'],
            data['message']
        )

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

    @database_sync_to_async
    def notify_message(self,receiver,sender,message):
        
        receiver = get_object_or_404(User,id=int(receiver))
        message_obj = Message.objects.create(
            receiver=receiver,sender=sender.username,content=message
        )
        message_obj.save()