from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """
    extended user profile
    """
    user = models.OneToOneField(User)
    serial_num = models.CharField(max_length=10)
    phone_num = models.BigIntegerField(null=True)

    def __unicode__(self):
        return "%s" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
    if created == True:  
        UserProfile.objects.get_or_create(user=instance)

'''
class GroupProfile(models.Model):
    """
    create group profile

    ref:
    https://github.com/zhaoyujiang/userprofile/blob/master/userprofile/models.py
    """
    group = models.OneToOneField(Group)
    owner = models.ForeignKey(User, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return "%s" %(self.group)

    
def create_group_profile(sender, instance, created, **kwargs):  
    if created == True:  
        GroupProfile.objects.get_or_create(group=instance)
'''
post_save.connect(create_user_profile, sender=User)
#post_save.connect(create_group_profile, sender=Group)
