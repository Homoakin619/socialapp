from django.db import models

class ChatDate(models.Model):
    timestamp = models.DateField()

    def __str__(self):
        return '%s' % self.timestamp

class ChatMessage(models.Model):
    date = models.ForeignKey(ChatDate,on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    chatroom = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return f'{self.chatroom} -- {self.sender}: {self.message}'