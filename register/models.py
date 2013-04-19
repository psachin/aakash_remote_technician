from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    serial_num = models.CharField(max_length=10)
    phone_num = models.BigIntegerField(null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
    if created == True:  
#        profile, created = UserProfile.objects.get_or_create(user=instance)
        UserProfile.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)
