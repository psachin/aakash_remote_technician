from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import ModelForm, widgets
from models import Profile, DeviceUser, Technician, Complaint

from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin import widgets 

from datetime import datetime, date

class RegisterDeviceUser(UserCreationForm):
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
        Clean and validate serial number from `models.DeviceUser`
        class
        
        ref:
        http://stackoverflow.com/questions/13036708/
        how-to-get-user-object-by-profile-field-value

        tests:
        
        >>> user = User.objects.all()
        >>> sachin = user.get(username='sachin')
        >>> sachin.profile.deviceuser_set.get(serial_num='1088301283')
        <DeviceUser: sachin>
        """

        # print self.cleaned_data['serial_num']
        try:
            DeviceUser.objects.get(serial_num=self.cleaned_data['serial_num'])
        except DeviceUser.DoesNotExist:
            return self.cleaned_data["serial_num"]
        raise forms.ValidationError(("Serial number already exist"))

    def clean_phone_num(self):
        """
        Clean and validate phone number from `models.DeviceUser` class
        """
        # print self.cleaned_data['phone_num']
        try:
            DeviceUser.objects.get(phone_num=self.cleaned_data['phone_num'])
            print "register user in try"
        except DeviceUser.DoesNotExist:
            return self.cleaned_data["phone_num"]
        raise forms.ValidationError(("Phone number already exist"))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")

        user = super(UserCreationForm, self).save(commit=True)
        # print self.cleaned_data["username"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        user.is_active = True # mark as active
        user.is_staff = True  # mark as staff

        if commit:
            try:
                user.save()
            except:
                raise forms.ValidationError("user profile saving failed")
        else:
            raise NotImplementedError("Can't create User and UserProfile without database save")
            

        '''
        >>> from django.contrib.auth.models import User
        >>> from register.models import Profile, DeviceUser
        >>> amit = User.objects.create(username='amit')
        >>> amit = User.objects.get(username='amit')
        >>> amit_profile = Profile.object.get(user=amit)
        >>> deviceuser = DeviceUser.objects.get(user=amit_profile)
        >>> deviceuser.phone_num
        u'992048445'

        '''
        
        username = User.objects.get(username=self.cleaned_data["username"])
        username_profile = Profile.objects.get(user=username)
        deviceuser = DeviceUser.objects.create(user=username_profile)
        # 
        deviceuser.serial_num = self.cleaned_data['serial_num']
        # print deviceuser.serial_num
        deviceuser.phone_num = self.cleaned_data['phone_num']
        # print deviceuser.phone_num

        '''
        profile = user.get_profile()
        profile.serial_num = self.cleaned_data['serial_num']
        profile.phone_num = self.cleaned_data['phone_num']
        '''

        if Group.objects.exists():
            try:
                Group.objects.get(name='aakash_user')
                # add user to group
                aakash_user = Group.objects.get(name='aakash_user')
                username = User.objects.get(username=user.username)
                username.groups.add(aakash_user)
            except:
                print "Group other than aakash_user"
                # create group
                Group.objects.create(name='aakash_user')
                # add user to group
                aakash_user = Group.objects.get(name='aakash_user')
                username = User.objects.get(username=user.username)
                username.groups.add(aakash_user)
        else:
            print "no group exists"
            print "creating Group: aakash_user"
            # create group
            Group.objects.create(name='aakash_user')
            # add user to group
            aakash_user = Group.objects.get(name='aakash_user')
            username = User.objects.get(username=user.username)
            username.groups.add(aakash_user)

                    
        if commit:
            try:                # save user and profile
                deviceuser.save()
            except:
                raise forms.ValidationError("Saving of DeviceUser failed")
        return user, deviceuser

class RegisterTechnician(UserCreationForm):
    """
    registration form for technician
    """
    email = forms.CharField(max_length=75, required=True)
    phone_num = forms.IntegerField(max_value=9999999999, required=True)
    agree = forms.BooleanField(
        error_messages={'required': 'You must accept the agreement inorder to register'},
        widget=forms.CheckboxInput(),
        label="I agree the rules",
        )

    # error_messages = {
    #     'duplicate_sr_num': _("Serial number already exists."),
    #     'password_mismatch': _("The two password fields didn't match."),
    # }

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','phone_num','password1','password2',)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already taken"))
        return self.cleaned_data['email']

    def clean_phone_num(self):
        """
        Clean and validate phone number from `models.DeviceUser` class
        """
        print self.cleaned_data['phone_num']
        try:
            Technician.objects.get(phone_num=self.cleaned_data['phone_num'])
        except Technician.DoesNotExist:
            print "doesNotExist"
            return self.cleaned_data["phone_num"]
        raise forms.ValidationError(("Phone number already exist"))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")

        user = super(UserCreationForm, self).save(commit=True)
        # print self.cleaned_data["username"]
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        user.is_active = True # mark as active
        user.is_staff = True  # mark as staff

        if commit:
            try:
                user.save()
            except:
                raise forms.ValidationError("user profile saving failed")
        else:
            raise NotImplementedError("Can't create User and UserProfile without database save")
            

        '''
        >>> from django.contrib.auth.models import User
        >>> from register.models import Profile, DeviceUser
        >>> amit = User.objects.create(username='amit')
        >>> amit = User.objects.get(username='amit')
        >>> amit_profile = Profile.object.get(user=amit)
        >>> deviceuser = DeviceUser.objects.get(user=amit_profile)
        >>> deviceuser.phone_num
        u'992048445'

        '''
        
        username = User.objects.get(username=self.cleaned_data["username"])
        username_profile = Profile.objects.get(user=username)
        technician = Technician.objects.create(user=username_profile)
        # 
        technician.phone_num = self.cleaned_data['phone_num']
        # print deviceuser.phone_num

        '''
        profile = user.get_profile()
        profile.serial_num = self.cleaned_data['serial_num']
        profile.phone_num = self.cleaned_data['phone_num']
        '''

        if Group.objects.exists():
            try:
                Group.objects.get(name='technician')
                # add user to group
                technician_g = Group.objects.get(name='technician')
                username = User.objects.get(username=user.username)
                username.groups.add(technician_g)
            except:
                '''
                aakash_user = Group(name="aakash_user")
                aakash_user.save()
                username = User.objects.get(username=user.username)
                username.groups.add(aakash_user)
                '''
                # create group
                Group.objects.create(name='technician')
                technician_g = Group.objects.get(name='technician')
                # add user to group
                username = User.objects.get(username=user.username)
                username.groups.add(technician_g)
        else:
            print "no Group exists"
            print "creating Group: technician"
            # create group
            Group.objects.create(name='technician')
            # add user to group
            technician_g = Group.objects.get(name='technician')
            username = User.objects.get(username=user.username)
            username.groups.add(technician_g)
                    
        if commit:
            try:                # save user and profile
                technician.save()
            except:
                raise forms.ValidationError("Saving of technician failed")
        return user, technician


class LogComplaint(ModelForm):
    """
    log complaint agains the device
    """
    when = forms.DateField(label="When(mm/dd/YYYY)")
    #when = widgets.AdminDateWidget()
    start = forms.TimeInput()
    end = forms.TimeInput()
    # end = forms.DateTimeField(widget=widgets.AdminSplitDateTime)
    complaint = forms.TextInput()


    class Meta:
        model = Complaint
        fields = ('when','start','end','complaint',)
        exclude = {'username',}

    def clean_when(self):
        """
        clean the date field
        """
        # print "WHEN: %s" % (self.cleaned_data["when"])
        # print type(self.cleaned_data["when"])
        # nn = datetime.strptime(self.cleaned_data["when"],"%Y-%d-%m")
        n = date.today()
        if self.cleaned_data["when"] < n:
            raise forms.ValidationError("Date can't be lower than today's date: %s" % (datetime.strftime(n,"%m/%d/%Y")))
        else:
            return self.cleaned_data["when"]
    
    def clean_start(self):
        """
        validate start time
        """
        try:
            self.cleaned_data["start"]
            try:
                self.when_start = datetime.combine(self.clean_when(), self.cleaned_data["start"])
                # print self.when_start
            except:
                raise forms.ValidationError("this field is required.")
        except:
            raise forms.ValidationError("this field is required.")
        return self.cleaned_data["start"]

    def clean_end(self):
        """
        validate end time
        """
        try:
            self.cleaned_data["end"]
            try:
                self.when_end = datetime.combine(self.clean_when(), self.cleaned_data["end"])
            except:
                raise forms.ValidationError("this field is required.")
        except:
            raise forms.ValidationError("this field is required.")
        return self.cleaned_data["end"]
                             
    def clean_complaint(self):
        """
        clean and validate complaints
        """
        return self.cleaned_data['complaint']
    
    def save(self, username, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")

        username = User.objects.get(username=username)
        user_profile = Profile.objects.get(user=username)
        deviceuser = DeviceUser.objects.get(user=user_profile)
        complaint = Complaint.objects.create(user=deviceuser)
        complaint.complaint = self.cleaned_data["complaint"]
        
        complaint.when = self.cleaned_data["when"]
        complaint.start = self.cleaned_data["start"]
        complaint.end = self.cleaned_data["end"]
        print self.when_end - self.when_start
        # print "Difference in time: %s" % (complaint.end - complaint.start)
        
        if commit:
            complaint.save()
        return complaint
        

    '''
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

'''
sac = User.objects.get(username='sachin')
sac.userprofile.user.groups.values_list()

'''
