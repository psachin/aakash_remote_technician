from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from models import UserProfile

class Register(UserCreationForm):
    """my form"""
    serial_num = forms.CharField(max_length=10, required=True)
    phone_num = forms.IntegerField(max_value=9999999999, required=True)
    agree = forms.BooleanField(
        error_messages={'required': 'You must accept in order allow root access to your device'},
        widget=forms.CheckboxInput(),
        label="I agree to allow root access",
        )
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','serial_num','phone_num','password1','password2')

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
        user.is_staff = True
        profile = user.get_profile()
        profile.serial_num = self.cleaned_data['serial_num']
        # for x in range(1,User.objects.count()):
        #     if User.objects.all().get(id=x).get_profile(serial_num=profile.serial_num).exists():
        #         raise forms.ValidationError("serial number already exists")
        profile.phone_num = self.cleaned_data['phone_num']

        if commit:
            try:
                profile.save()
                user.save()
            except:
                raise forms.ValidationError("serial number already exists")
        
        return user, profile


