from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

NICHE_CHOICES = (
    ('ADAB','ADAB'),
    ('HADITH','HADITH'),
    ('FALSAFA','FALSAFA')
)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(null=True,blank=True)
    about = models.CharField(max_length=150,blank=True,null=True)
    is_ustaz = models.BooleanField(default=False)
    niche = models.CharField(choices=NICHE_CHOICES,max_length=7,default='ADAB')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile',kwargs={'pk':self.pk})