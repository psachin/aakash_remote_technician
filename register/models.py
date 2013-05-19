from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

from datetime import datetime
#from taggit.managers import TaggableManager

class Profile(models.Model):
    """
    extended auth user profile
    """
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "%s" % self.user

class DeviceUser(models.Model):
    """
    extended user profile for aakash users
    """
    user = models.ForeignKey(Profile)
    serial_num = models.CharField(max_length=15)
    phone_num = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s" % (self.user)

class Technician(models.Model):
    """
    extended technician profile
    """
    user = models.ForeignKey(Profile)
    phone_num = models.CharField(max_length=15)
    
    def __unicode__(self):
        return "%s" % (self.user)

class Complaint(models.Model):
    """
    users complaints
    """
    user = models.ForeignKey(DeviceUser)
    when = models.DateField(null=True, blank=True)
    start = models.TimeField(null=True, blank=True)
    end = models.TimeField(null=True, blank=True)
    complaint = models.TextField()
    technician = models.ForeignKey(Profile, null=True) 
    
    def __unicode__(self):
        return "%s : %s" % (self.user, self.complaint)

def create_profile(sender, instance, created, **kwargs):  
    if created == True:  
        Profile.objects.get_or_create(user=instance)

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
post_save.connect(create_profile, sender=User)
#post_save.connect(create_group_profile, sender=Group)
