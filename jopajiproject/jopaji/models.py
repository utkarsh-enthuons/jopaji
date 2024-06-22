from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import RegexValidator
from tinymce.models import HTMLField
from django.utils.text import slugify
from django.contrib.auth.models import User
import json

# create regex pattern
name_pattern = r'^[a-zA-Z]+(?: [a-zA-Z]+)*$'
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+?1?\d{9,15}$'
page_choice = (('default', 'select Field'), ('homepage', 'Homepage'), ('about_us', 'About Us'), ('menu', 'Our Menu'),
               ('franchise', 'Franchise'),
               ('contact_us', 'Contact Us'), ('book_order', 'Book an Order'))
state_choice = (('default', 'Select State'), ('andaman_and_nicobar_islands', 'Andaman and Nicobar Islands'),
                ('andhra_pradesh', 'Andhra Pradesh'), ('arunachal_pradesh', 'Arunachal Pradesh'), ('assam', 'Assam'),
                ('bihar', 'Bihar'), ('chandigarh', 'Chandigarh'), ('chhattisgarh', 'Chhattisgarh'),
                ('dadra_and_nagar_haveli', 'Dadra and Nagar Haveli'), ('daman_and_diu', 'Daman and Diu'),
                ('delhi', 'Delhi'), ('goa', 'Goa'), ('gujarat', 'Gujarat'), ('haryana', 'Haryana'),
                ('himachal_pradesh', 'Himachal Pradesh'), ('jammu_and_kashmir', 'Jammu and Kashmir'),
                ('jharkhand', 'Jharkhand'), ('karnataka', 'Karnataka'), ('kerala', 'Kerala'), ('ladakh', 'Ladakh'),
                ('lakshadweep', 'Lakshadweep'), ('madhya_pradesh', 'Madhya Pradesh'), ('maharashtra', 'Maharashtra'),
                ('manipur', 'Manipur'), ('meghalaya', 'Meghalaya'), ('mizoram', 'Mizoram'), ('nagaland', 'Nagaland'),
                ('odisha', 'Odisha'), ('puducherry', 'Puducherry'), ('punjab', 'Punjab'), ('rajasthan', 'Rajasthan'),
                ('sikkim', 'Sikkim'), ('tamil_nadu', 'Tamil Nadu'), ('telangana', 'Telangana'), ('tripura', 'Tripura'),
                ('uttar_pradesh', 'Uttar Pradesh'), ('uttarakhand', 'Uttarakhand'), ('west_bengal', 'West Bengal'))


# Create your models here.
class Banner(models.Model):
    page_name = models.CharField(choices=page_choice, default='default', max_length=50)
    desk_image = models.ImageField(upload_to='images/sub-banner/desktop/', blank=False, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], default="")
    mob_image = models.ImageField(upload_to='images/sub-banner/mobile/', blank=False, validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])], default="")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    alt_text = models.CharField(max_length=100, blank=False, default='Banner', validators=[
        RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])

    def __str__(self):
        return self.page_name


class user_client(models.Model):
    title = models.CharField(max_length=100, blank=False, validators=[
        RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    image = models.ImageField(upload_to='images/', blank=False,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    client_desc = HTMLField()

    def __str__(self):
        return self.title


class category_master(models.Model):
    cat_name = models.CharField(max_length=100, blank=False, validators=[
        RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    status = models.BooleanField(default=True, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    priority = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='images/cat_image/', blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    desk_image = models.ImageField(upload_to='images/cat_image/', blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    mob_image = models.ImageField(upload_to='images/cat_image/', blank=True,
                                  validators=[
                                      FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    cat_descr = HTMLField(blank=True, default='')
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.cat_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cat_name


class contact_us(models.Model):
    name = models.CharField(max_length=64, blank=False,
                            validators=[RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    email = models.EmailField(max_length=64, blank=False, validators=[
        RegexValidator(regex=email_pattern, message="Please enter a valid Email ID.")])
    subject = models.CharField(max_length=300, blank=False, default="")
    message = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.name


class franchise(models.Model):
    name = models.CharField(max_length=64, blank=False,
                            validators=[RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    email = models.EmailField(max_length=64, blank=False, validators=[
        RegexValidator(regex=email_pattern, message="Please enter a valid Email ID.")])
    phone = models.CharField(max_length=10, blank=False, default="", validators=[
        RegexValidator(regex=phone_pattern, message="Please enter a valid Phone number.")])
    address = models.CharField(max_length=300, blank=False, default="")
    address2 = models.CharField(max_length=300, blank=True)
    message = models.TextField(max_length=2000, blank=True)

    def __str__(self):
        return self.name


class tbl_product(models.Model):
    productname = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(category_master, on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255, blank=True)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='images/product/', blank=False, default=True,
                               validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    recipe = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.productname)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.productname


class address(models.Model):
    admin_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=64, blank=False,
                            validators=[RegexValidator(regex=name_pattern, message="Please enter a valid first name.")])
    phone = models.CharField(max_length=10, blank=False, default="", validators=[
        RegexValidator(regex=phone_pattern, message="Please enter a valid Phone number.")])
    email = models.EmailField(max_length=64, blank=False, validators=[
        RegexValidator(regex=email_pattern, message="Please enter a valid Email ID.")])
    h_no = models.IntegerField(max_length=3, blank=True)
    city_or_village = models.CharField(max_length=100, blank=False)
    zipcode = models.IntegerField(max_length=6, blank=False)
    address = models.CharField(max_length=300, blank=False, default="")
    state = models.CharField(choices=page_choice, default='default', max_length=50)

    def __str__(self):
        return self.name
