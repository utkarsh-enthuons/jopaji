from django import forms
from .models import contact_us, franchise, address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm, password_validation
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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


# user registration
class CustomerRegistration(UserCreationForm):
    first_name = forms.CharField(label='First Name', required=True,
                            widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}),
                            validators=[
                                RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    last_name = forms.CharField(label='Last Name', required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}),
                                 validators=[
                                     RegexValidator(regex=name_pattern, message="Please enter a valid last name.")])
    email = forms.CharField(label='Email Address', required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'}),
                            validators=[
                                RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password', 'class': 'form-control'}), validators=[
        RegexValidator(regex=password_pattern,
                       message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    password2 = forms.CharField(label='Confirm Password', required=True, widget=forms.PasswordInput(
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
        user = super(CustomerRegistration, self).save(commit=False)
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])  # Set hashed password
        user.is_active = True

        if commit:
            user.save()

        return user


class CustomerLogin(AuthenticationForm):
    username = forms.CharField(label='Email Address', required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control', "autofocus": True}),
                            validators=[
                                RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Your Password', 'class': 'form-control', "autocomplete": "current-password"}), validators=[
        RegexValidator(regex=password_pattern,
                       message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
        elif not user.is_staff:
            raise ValidationError("You must need to verify your email to log in.")


class UserPasswordReset(PasswordResetForm):
    email = forms.EmailField(label=_('Email Address'), max_length=255, required=True,
         widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}),
         validators=[RegexValidator(regex=email_pattern, message="Please enter a valid email address.")])


class UserSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": _("The confirm password doesn't match with new password."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
    )


class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control', 'autofocus': 'True'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html(), validators=[
        RegexValidator(regex=password_pattern, message="Password must contain at least 8 characters, including at least one digit, one lowercase letter, one uppercase letter, and one special character.")])
    new_password2 = forms.CharField(label=_('Password'), strip=False, required=True, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))

    def clean_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("Passwords do not match")
        return new_password2


class UserAddress(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAddress, self).__init__(*args, **kwargs)
        required_fields = ['name', 'phone', 'email', 'h_no', 'locality', 'city_or_village', 'zipcode', 'state', ]
        for field in required_fields:
            self.fields[field].required = True

    class Meta:
        model = address
        fields = ['name', 'phone', 'email', 'h_no', 'locality', 'city_or_village', 'zipcode', 'state']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Your Name'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'h_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hounse No.'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality'}),
            'city_or_village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Khurja'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '123456'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }