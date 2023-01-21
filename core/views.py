from multiprocessing import context
from django.contrib.auth import login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize 

from chat.models import ChatDate,ChatMessage,Message

from core.models import Notification, Post,Comment,Notify
from core.forms import PostForm,ProfileForm,EditProfileForm,EditProfileImageForm,CommentForm

from authentication.models import Profile


import json
from datetime import date

class IndexView(LoginRequiredMixin,generic.View):
    template_name = 'core/home.html'
    def get(self,request,*args,**kwargs):
        form = PostForm()
        comment_form = CommentForm()
        user_profile = get_object_or_404(Profile,user=request.user)
        context = {'all_posts':Post.objects.filter(tag=user_profile.niche).order_by('-created'),'form':form,'comment_form':comment_form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        form = PostForm(request.POST,request.FILES)
        comment_form = CommentForm(request.POST)
        comment = request.POST.get('comment')
        pstf = request.POST.get('pstf')
        
        # Process Comments
        if comment:
            pid = request.POST.get('post_id')
            post = get_object_or_404(Post,id=pid)
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = request.user
                instance.post_id = post
                instance.save()
                return HttpResponseRedirect(reverse('home'))

        # Process create post
        else:
            if form.is_valid():
                post_form = form.save(commit=False)
                post_form.user = request.user
                post_form.save()
                return HttpResponseRedirect(reverse('home'))
        return HttpResponseRedirect(reverse('home'))
        
class EditPostView(generic.View):
    template_name = 'core/edit_post.html'
    def get(self,request,*args,**kwargs):
        query = get_object_or_404(Post,pk=kwargs['pk'])
        edit_post_form = PostForm(instance=query)
        context = {'edit_form':edit_post_form}
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        query = get_object_or_404(Post,pk=kwargs['pk'])
        edit_post_form = PostForm(request.POST,request.FILES,instance=query)
        if edit_post_form.is_valid():
            edit_post_form.save()
            return HttpResponseRedirect(reverse('home'))
        return render(request,self.template_name)


def delete_post(request,*args,**kwargs):
        query = get_object_or_404(Post,pk=kwargs['pk'])
        query.delete()
        return HttpResponseRedirect(reverse('home'))


class ProfileView(generic.View):
    template_name = 'core/profile.html'
    def get(self,request,*args,**kwargs):
        comment_form = CommentForm()
        user = request.user
        profile = get_object_or_404(User,id=kwargs['pk'])
        user_profile = get_object_or_404(Profile,user=profile)
        profile_form = EditProfileForm(instance=user_profile)
        image_form = EditProfileImageForm(request.FILES,instance=user_profile)
        form = PostForm()
        posts = Post.objects.filter(user=profile)
        all_posts = Post.objects.filter(tag=user_profile.niche).exclude(user=profile)
        activities = profile.post_set.all()
        
        user_id = user.id
        friend = User.objects.get(id=kwargs['pk'])
    
        if user_id > friend.id:
            chat_room = f'chat_{user_id}-{friend.id}'
        else:
            chat_room = f'chat_{friend.id}-{user_id}'
        messages = ChatMessage.objects.filter(chatroom=chat_room)
        today_date = date.today()
        chat_date = ChatDate.objects.all()

        result = False
        query = Notify.objects.filter(subscriber=request.user,post_creator=profile)
        if query:
            result = True
        else: result = False
        
        
        context = {'status':result,'profile_stat':True,

                    'activities':activities,'my_posts':posts.order_by('-created'),
                    'form':form,'other_posts':all_posts,'user':user,
                    'profile_form':profile_form,'image_form':image_form,
                    'profile':profile,'comment_form':comment_form,
                    'messages':messages, 'today':today_date,'chat_date':chat_date
                  }
        return render(request,self.template_name,context)

    def post(self,request,*args,**kwargs):
        user = request.user
        user_profile = get_object_or_404(Profile,user=user)
        profile_form = EditProfileForm(request.POST,instance=user_profile)
        form = PostForm(request.POST)
        comment_form = CommentForm(request.POST)
        image_form = EditProfileImageForm(request.POST,request.FILES,instance=user_profile)
        profile = request.POST.get('profile')
        image = request.POST.get('img')
        comment = request.POST.get('comment')
        if profile:
            if profile_form.is_valid():
                m_form = profile_form.save(commit=False)
                m_form.user_id = request.user
                m_form.save()
                return reverse('profile',kwargs={'pk':kwargs['pk']})
        elif image:
            if image_form.is_valid():
                
                image_form.save()
                return HttpResponseRedirect(reverse('profile',kwargs={'pk':kwargs['pk']}))
            else:
                
                return HttpResponseRedirect(reverse('profile'))
        # Process Comments
        elif comment:
            pid = request.POST.get('post_id')
            post = get_object_or_404(Post,id=pid)
            
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = request.user
                instance.post_id = post
                instance.save()
                return HttpResponseRedirect(reverse('home'))
        else:
            if form.is_valid():
                post_form = form.save(commit=False)
                post_form.user = request.user
                post_form.save()
                return reverse('profile',kwargs={'pk':kwargs['pk']})
        return render(request,self.template_name)


class EditProfileView(generic.View):
    template_name = ''
    def get(self,request,*args,**kwargs):
        instance = get_object_or_404(Profile,user=request.user)
        profile_form = ProfileForm(instance=instance)
        context = {'form':profile_form}
        return None

    def post(self,request,*args,**kwargs):
        profile_form = PostForm(request.POST)
        if profile_form.is_valid():
            form = profile_form.save(commit=False)
            form.user_id = request.user
            form.save()
            return HttpResponseRedirect(reverse('home'))
        return render(request,self.template_name)

class NotificationView(generic.View):
    template_name = 'core/notifications.html'

    def get(self, request,*args,**kwargs):
        user = request.user
        my_notifications = Notification.objects.filter(subscriber=user).all().order_by('-pk')
        context = {'notifications':my_notifications}
        
        return render(request,self.template_name,context)



def subscribe_notification(request,id):
    subscriber = request.user
    creator = get_object_or_404(User,id=id)
    subscribe_user = Notify.objects.create(subscriber=subscriber,post_creator=creator)
    subscribe_user.save()
    return JsonResponse({'respons':'suscribed successfully'})


def disable_notification(request,id):
    subscriber = request.user
    creator = get_object_or_404(User,id=id)
    subscribe_user = Notify.objects.get(subscriber=subscriber,post_creator=creator)
    subscribe_user.delete()
    return JsonResponse({'response':'successfully unsuscribed'})


def message_view(request):
    messages = Message.objects.filter(receiver=request.user)
    context = {'messages':messages}
    return render(request,'core/messages.html',context)



def create_comment(request,form):
    if form.is_valid():
        form.save()
        return True
    else: return False


def view_notification(request,pk):
    try:
        notification = get_object_or_404(Notification,pk=pk)
        
        notification.is_read = True
        
        notification.save()
        
        return HttpResponseRedirect(reverse('view_notification',kwargs={'pk':pk}))
    except:
        print("request failed")


def notification_view(request,pk):
    notification = get_object_or_404(Notification,pk=pk)
    post_id = notification.post_id
    context = {'comment':False}
    try:
        post = get_object_or_404(Post,pk=post_id)
        if notification.comment_id > 0:
            comment = get_object_or_404(Comment,pk=notification.comment_id)
            context['comment'] = comment
        context['post'] = post
        return render(request,'core/notification_view.html',context)
    except:
        print('failed request')


@csrf_exempt
def change_notification(request):
    request_body = json.loads(request.body.decode('utf-8'))
    queryID = request_body['value']
    notification = get_object_or_404(Notification,pk=queryID)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status':'notification viewed'})


@csrf_exempt
def chat_user(request):
        user_id = request.user.id
        request_body = json.loads(request.body.decode('utf-8'))
        name = request_body['name']
        friend = User.objects.get(username=name)
    
        if user_id > friend.id:
            chat_room = f'chat_{user_id}-{friend.id}'
        else:
            chat_room = f'chat_{friend.id}-{user_id}'
        messages_qs = ChatMessage.objects.filter(chatroom=chat_room).order_by('-id')
        
        today_date = date.today()
        chat_date = ChatDate.objects.all()
        chat_date = serialize("json",list(chat_date))
        messages = serialize('json',list(messages_qs))
        read = read_message(request,name)
        read = json.loads(read.content)
        
        return JsonResponse({
            'messages':messages,
            'today_date':today_date,
            'friend':name,
            'id':friend.id,
            'status':read['status'],
            'chat_date':chat_date
        })



@csrf_exempt
def read_message(request,username):
    try:
        # print(username)
        friend = get_object_or_404(User,username=username)
        message_instance = Message.objects.filter(receiver=request.user,sender=friend,is_read=False)
        
        for message in message_instance:
            message.is_read = True
            message.save()
        return JsonResponse({'status':'success reading message'})
    except:
        return JsonResponse({'status':'failed'})


@csrf_exempt
def get_counts(request):
    message_query = Message.objects.filter(receiver=request.user,is_read=False)
    notification_query = Notification.objects.filter(subscriber=request.user,is_read=False)
    return JsonResponse({
        'message_count':message_query.count(),
        'notification_count':notification_query.count()
                        })


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')