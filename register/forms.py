from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm
from models import UserProfile

from django.utils.translation import ugettext, ugettext_lazy as _


class Register(UserCreationForm):
    """
    form for user
    """
    email = forms.CharField(max_length=75, required=True)
    serial_num = forms.CharField(max_length=10, required=True)
    phone_num = forms.IntegerField(max_value=9999999999, required=True)
    agree = forms.BooleanField(
        error_messages={'required': 'You must accept in order allow root access to your device'},
        widget=forms.CheckboxInput(),
        label="I agree to allow root access",
        )

    # error_messages = {
    #     'duplicate_sr_num': _("Serial number already exists."),
    #     'password_mismatch': _("The two password fields didn't match."),
    # }

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','serial_num','phone_num','password1','password2',)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already taken"))
        return self.cleaned_data['email']

    def clean_serial_num(self):
        """
        Clean and validate serial number from `models.UserProfile`
        class
        
        ref:
        http://stackoverflow.com/questions/13036708/
        how-to-get-user-object-by-profile-field-value
        """
        print self.cleaned_data['serial_num']
        try:
            UserProfile.objects.get(serial_num=self.cleaned_data['serial_num'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data["serial_num"]
        raise forms.ValidationError(("Serial number already exist"))

    def clean_phone_num(self):
        """
        Clean and validate phone number from `models.UserProfile` class
        """
        print self.cleaned_data['phone_num']
        try:
            UserProfile.objects.get(phone_num=self.cleaned_data['phone_num'])
        except UserProfile.DoesNotExist:
            return self.cleaned_data["phone_num"]
        raise forms.ValidationError(("Phone number already exist"))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")

        user = super(UserCreationForm, self).save(commit=True)
        print self.cleaned_data["username"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        user.is_active = True # mark as active
        user.is_staff = True  # mark as staff

        profile = user.get_profile()
        profile.serial_num = self.cleaned_data['serial_num']
        profile.phone_num = self.cleaned_data['phone_num']

        if commit:
            try:                # save user and profile
                profile.save()
                user.save()
            except:
                raise forms.ValidationError("Saving failed")
        return user, profile

    def group_save(self):
        user = super(UserCreationForm, self).save(commit=True)
        print "Username: %s" % (user.username)
        try:
            aakash_user = Group.objects.get(name='aakash_user')
            username = User.objects.get(username=user.username)
            username.groups.add(aakash_user)
        except:
            aakash_user = Group(name="aakash_user")
            aakash_user.save()
            username = User.objects.get(username=user.username)
            username.groups.add(aakash_user)


class RegisterForm():
    class Meta:
        form = Register
    

'''
sac = User.objects.get(username='sachin')
sac.userprofile.user.groups.values_list()


class TechnicianRegister(UserCreationForm):
    """
    form for technician
    """
    phone_num = forms.IntegerField(max_value=9999999999, required=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone_num','password1','password2')

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create technician and TechnicianProfile without database save")

        technician = super(UserCreationForm, self).save(commit=True)
        technician.username = self.cleaned_data["username"]
        technician.first_name = self.cleaned_data["first_name"]
        technician.last_name = self.cleaned_data["last_name"]
        technician.email = self.cleaned_data["email"]
        technician.set_password(self.cleaned_data["password1"])
        technician.is_active = True
        technician.is_staff = True
        profile = technician.get_profile()
        profile.phone_num = self.cleaned_data['phone_num']

        if commit:
            try:
                profile.save()
                technician.save()
            except:
                raise forms.ValidationError("serial number already exists")

        return technician, profile


'''
