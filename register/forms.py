from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from models import UserProfile

from random import choice
from string import letters

class Register(UserCreationForm):
    """my form"""
    serial_num = forms.CharField(max_length=10)
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','serial_num','password1','password2',)

        
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")

        user = super(UserCreationForm, self).save(commit=True)
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            profile = user.get_profile()
            profile.serial_num = self.cleaned_data['serial_num']
            # profile.serial_num = ''.join([choice(letters) for i in xrange(12)])
            #user_profile = UserProfile(user=user, serial_num=self.cleaned_data['serial_num'])
            profile.save()
            user.save()
        return user, profile
