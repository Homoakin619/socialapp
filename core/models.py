from django.db import models
from django.conf import settings
from django.urls import reverse

NICHE_CHOICES = (
    ('ADAB','ADAB'),
)

STATUS_CHOICES = (
    ('USER','USER'),
    ('USTAZ','USTAZ')
)

TAGS_CHOICES = (
    ('ADAB','ADAB'),
    ('HADITH','HADITH'),
    ('FALSAFA','FALSAFA')
)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=8,choices=TAGS_CHOICES)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent_id = models.IntegerField(blank=True,null=True)

    def __repr__(self) -> str:
        return self.user.username

NOTIFIACTIONS = (
    ('COMMENT','COMMENT'),
    ('POST','POST')
)

class Notification(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='notified_user')
    post_creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='post_creator')
    post_id = models.IntegerField()
    is_read = models.BooleanField(default=False)
    comment_id = models.IntegerField(default=-1)
    notification_type = models.CharField(choices=NOTIFIACTIONS,max_length=7)

    def __str__(self):
        return self.subscriber.username

class Notify(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='subscribers')
    post_creator = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='subscribed_to',on_delete=models.CASCADE)
    

# class Reply(models.Model):
#     parent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    

