from django import forms
from .models import contact_us, franchise
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+?1?\d{9,15}$'
password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['subject'].required = True

    class Meta:
        model = contact_us
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write message', 'class': 'form-control'}),
        }


class FranchiseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FranchiseForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['address'].required = True

    class Meta:
        model = franchise
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address 1', 'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'placeholder': 'Address 2 (Optional)', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write message', 'class': 'form-control'}),
        }


class RegUser(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
                             validators=[
                                 RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                                 validators=[
                                     RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                validators=[
                                    RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password', 'class': 'form-control'}), validators=[
        RegexValidator(regex=password_pattern,
                       message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Retype Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already taken.")
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super(RegUser, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])  # Set hashed password
        user.is_staff = True
        user.is_active = True
        if commit:
            user.save()
            # Assign user to a group (You can replace 'my_group_name' with your desired group name)
            group = Group.objects.get(name='user_person')
            user.groups.add(group)
        else:
            print("User not created.")
        print(user)
        return user


class UserLogin(forms.Form):
    username = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
                             validators=[
                                 RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password', 'class': 'form-control'}), validators=[
        RegexValidator(regex=password_pattern,
                       message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
