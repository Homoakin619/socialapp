from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404

from chat.models import Message,ChatMessage,ChatDate
from core.models import Notification,Notify

import json

class RefreshConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.user_id = self.scope['user'].id

        await self.accept()

    async def disconnect(self, code):
        return await super().disconnect(code)


    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        
        if data['type'] == 'refresh':

            counts = await self.refresh_count()
            messages = counts['message_count']
            notifications = counts['notification_count']
            self.friend_id = data['friend_id']

            if self.friend_id:
                return_value = await self.refresh_chat_history()
                history = return_value['history']
                dates = return_value['dates']
                dates = json.loads(dates)
                history = json.loads(history)
                
                await self.send(text_data=json.dumps({
                'message_count':messages,'notification_count':notifications,
                'friend_username':self.friend_name,
                'chat_history':history, 'chat_dates':dates
            }))
            else:
                await self.send(text_data=json.dumps({
                    'message_count':messages,'notification_count':notifications,
                }))
        
        elif data['type'] == 'read':
            print(data)
            response = await self.read_message(data['username'])

            if response['response'] == 'success':
                await self.send(text_data=json.dumps({
                    'response':'success','user_id':response['user_id'],'message':'Message read successfully'
                }));
            else:
                await self.send(text_data=json.dumps({
                    'response':'fail','message':'Failed to read message, error occured'
                }));

        else:
            print(data)
            id = data['id']
            action = data['action']
            if action == 'subscribe':
                response = await self.subscribe_notification(id)
                await self.send(text_data=json.dumps({
                    'response':response['response']
                }))

            else:
                response = await self.disable_notification(id)
                await self.send(text_data=json.dumps({
                    'response':response['response']
                }))

        
#  amoxilin syrup unbranded

    @database_sync_to_async
    def refresh_count(self):
        message_instance = Message.objects.filter(is_read=False,receiver=self.user)
        message_count = message_instance.count()

        notification_query = Notification.objects.filter(subscriber=self.user,is_read=False)
        notification_count = notification_query.count()
        return {'message_count':message_count,'notification_count':notification_count}

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


    @database_sync_to_async
    def subscribe_notification(self,id):
        creator = get_object_or_404(User,id=id)
        subscribe_user = Notify.objects.create(subscriber=self.user,post_creator=creator)
        subscribe_user.save()
        return {'response':'suscribed successfully'}

    @database_sync_to_async
    def disable_notification(self,id):
        creator = get_object_or_404(User,id=id)
        subscribe_user = Notify.objects.get(subscriber=self.user,post_creator=creator)
        subscribe_user.delete()
        return {'response':'successfully unsuscribed'}

    @database_sync_to_async
    def read_message(self,username):
        try:
            friend = get_object_or_404(User,username=username)
            message_instance = Message.objects.filter(receiver=self.user,sender=friend,is_read=False)
            
            for message in message_instance:
                message.is_read = True
                message.save()
            return {'response':'success','user_id':friend.id}
        except:
            return {'response':'failed'}