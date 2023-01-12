from django.shortcuts import render
from django.contrib.auth.models import User


def chat_view(request,username):
    friend_id = User.objects.get(username=username)
    

    return render(request,'chat/chat.html',{'friend_id':friend_id})