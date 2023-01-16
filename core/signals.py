from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post,Notification,Notify,Comment

#  user to be notified
#  User that created the post
#  Post id


@receiver(post_save,sender=Comment)
def comment_notification(sender,instance,**kwargs):
    comment_creator = instance.user
    post = instance.post_id
    post_creator = post.user
    if comment_creator != post_creator:
        notification_instance = Notification.objects.create(subscriber=post_creator,post_creator=comment_creator,
                                                post_id=post.pk,notification_type='COMMENT',comment_id=instance.pk)
        notification_instance.save()

@receiver(post_save,sender=Post)
def create_notification(sender,instance,**kwargs):
    creator = instance.user
    post_id = instance.pk
    users_list = Notify.objects.filter(post_creator=creator)
    print(users_list)
    for user in users_list:
        x = Notification.objects.create(subscriber=user.subscriber,post_creator=creator,post_id=post_id,notification_type='POST')
        x.save()
        
