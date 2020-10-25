from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime
from django.urls import reverse 
from mptt.models import MPTTModel , TreeForeignKey
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#from user_profile.models import User
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
import datetime
from django.urls import reverse 
from mptt.models import MPTTModel , TreeForeignKey
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#from user_profile.models import User
from django.contrib.postgres.fields import ArrayField

from django.dispatch import receiver
from django.conf import settings 
from django.db.models.signals import post_save, pre_save
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from randompinfield import RandomPinField                          
from django.contrib import messages
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from rest_framework_simplejwt.tokens import RefreshToken
from User_details.decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.conf import settings



# host_prefix = "http://"
# host_name = host_prefix+settings.ALLOWED_HOSTS[0]+":8080"

host_prefix = "https://"
host_name = host_prefix+settings.ALLOWED_HOSTS[0]

#------------------------------------- User_details--------------------------------

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/<username>/<filename>
    return 'users/{0}/{1}'.format(instance.user.username, filename)


class UserManager(BaseUserManager):
    

    def create_user(self, email, password=None):
        # if username is None:
        #     raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

    def create_supelier(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(email, password)
        user.is_suplier = True
        user.save()
        return user

 

 

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True,null=True,blank=True)
    email = models.EmailField(max_length=255,unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_suplier  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length= 64,default="",blank=True)
    role = models.CharField(max_length= 64,default="",blank=True)
    pwd = models.CharField(max_length= 568,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# class GuestUser(models.Model):
  
#   ip = models.CharField(max_length=220)
#   date = models.DateTimeField(auto_now=True)

# def guest_ip_address(request):

#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# @receiver(post_save, sender=GuestUser)
# def create_user_profile(sender, instance, created, *args, **kwargs):
#     if created:
#         Profile.objects.create(guestuser=instance)


class Profile(models.Model):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    OTHER = 'o'

    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (OTHER,'Other'),
    )

    name = models.CharField(max_length = 264, null = True, blank = True,default="")
    email = models.CharField(max_length = 64, null= True, blank = True,default="")
    profile_picture = models.ImageField(null=True, blank=True)
    profile_picture_url = models.CharField(max_length=255,blank=True,null=True,default="")
    phone_number = models.CharField(max_length=100 ,  null=True,blank=True,default="")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True,default="")
    # city = models.CharField(max_length=100, blank= True, null= True)
    # district = models.CharField(max_length=100, blank= True, null= True)
    # road_number = models.CharField(max_length = 264,blank=True, null=True)
    # building_number = models.CharField(max_length = 264,blank=True, null=True)
    # apartment_number = models.CharField(max_length = 264,blank=True, null=True)
    # user_id = models.IntegerField(blank = True, null = True,default=-1)
    address = models.TextField(blank = True, default="")
    area = models.CharField(max_length=255,blank=True,null=True,default="")
    location = models.CharField(max_length=255,blank=True,null=True,default="")
    user_id = models.IntegerField (blank = True, null = True,default=-1)



    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
      
        #print(self.product_image)
        if self.profile_picture:
            return "{0}{1}".format(host_name,self.profile_picture.url)
        else:
            return " "
        
    
    def save(self, *args, **kwargs):
          self.profile_picture_url = self.image
          super(Profile, self).save(*args, **kwargs)


class user_relation (models.Model):
    verified_user_id = models.IntegerField (blank = True, null = True,default=-1)
    non_verified_user_id = models.IntegerField (blank = True, null = True,default=-1)


class user_supervisor_relation (models.Model):
    supervisor_id = models.IntegerField (blank = True, null = True,default=0)
    user_id = models.IntegerField (blank = True, null = True)

class ActivityLog(models.Model):
    user_id = models.IntegerField (blank = True, null = True)
    activity_name = models.CharField(max_length=255,blank=True,null=True,default="")
    time = models.DateTimeField (auto_now_add=True)
    activity_id = models.IntegerField (blank = True, null = True)


# class DeactivateUser(TimeStampedModel):
#     user = models.OneToOneField(User, related_name='deactivate', on_delete=models.CASCADE)
#     deactive = models.BooleanField(default=True)

class user_balance(models.Model):
    wallet = models.FloatField(blank = False, null = True, default=0)
    point = models.FloatField(blank = False, null = True, default = 0)
    dates = models.DateTimeField (auto_now_add=True)
    user_id = models.IntegerField(blank=False, null=True,default=-1)
    ip_id = models.IntegerField(blank=False, null=True,default=-1)

class Guest_user(models.Model):
    ip_address = models.CharField(max_length = 64, blank = False, null = True,default="")
    Date = models.DateField (auto_now_add=True)
    non_verified_user_id = models.IntegerField(blank=False, null=True,default=-1)

    @property
    def sub(self):


        if self.id: 

            non_id = self.id


        else:

            non_id = 0 

        return non_id

            


    def save(self, *args, **kwargs):

        self.non_verified_user_id = self.sub
        super(Guest_user, self).save(*args, **kwargs)



# ------------------------- Advertisement ---------------------

class Advertisement(models.Model):

    image = models.ImageField(upload_to='Advertisement',null = True)
    ad_link = models.CharField(max_length=255,blank=True,null = True,default="")
    content = models.CharField(max_length=255,blank=True,null = True,default="")
    click_count = models.IntegerField(default =0)
    view_count = models.IntegerField(default=0)
    total_click_count = models.IntegerField(default =0)
    total_view_count = models.IntegerField(default=0)
    priority = models.IntegerField(default=-1)
    is_active = models.BooleanField(blank = True, default = True)
    
    def __str__(self):
        return str(self.content)

# ----------------------------- Impression ----------------------------

class ProductImpression (models.Model):

    users = ArrayField(models.IntegerField(), blank=True, null=True,default=list)
    product_id = models.IntegerField (null = False,default=-1)
    view_count = models.IntegerField (blank = True, null = True, default = 0)
    click_count = models.IntegerField (blank = True, null = True,default = 0)
    cart_count = models.IntegerField (blank = True, null = True,default = 0)
    sales_count = models.IntegerField (blank = True, null = True,default = 0)
    non_verified_user = ArrayField(models.IntegerField(), blank=True, null=True,default=list)
    dates = models.DateTimeField(auto_now_add=True)

#-------------------------------Site Settings---------------------------------

class CompanyInfo(models.Model):
    '''
    This is Compnay Info model class.
    '''
    # company_id = models.AutoField(primary_key = True, auto_created = True, unique=True)
    name = models.CharField(max_length=500 , blank=True, null=True,default="")
    logo = models.ImageField(upload_to='Logo', null = True,blank = True,default="")
    address = models.TextField(max_length=1500,blank=True, null=True,default="" )
    icon = models.ImageField(upload_to='Icon', null = True,blank=True,default="")
    Facebook = models.CharField(max_length=264 , blank=True, null=True,default="")
    twitter = models.CharField(max_length=264 , blank=True, null=True,default="")
    linkedin = models.CharField(max_length=264 , blank=True, null=True,default="")
    youtube = models.CharField(max_length=264 , blank=True, null=True,default="")
    email = models.CharField(max_length=264 , blank=True, null=True,default="")
    phone = models.CharField(max_length=264 , blank=True, null=True,default="")
    help_center = models.CharField(max_length=264 , blank=True, null=True,default="")
    About = models.CharField(max_length=5000 , blank=True, null=True,default="")
    policy = ArrayField(models.CharField(max_length=100000), blank=True, null=True,default=list)
    terms_condition= ArrayField(models.CharField(max_length=100000), blank=True, null=True,default=list)
    slogan = models.CharField(max_length=264 , blank=True, null=True,default="")
    cookies = models.CharField(max_length=10000 , blank=True, null=True,default="")
    


class Banner(models.Model):

    count = models.IntegerField( blank=False,default=0)
    set_time = models.IntegerField(blank = False,default=0)
    is_active = models.BooleanField(blank = True, default = True)


class Banner_Image(models.Model):
    # this call is for uploading banner images
    Banner_id = models.IntegerField(blank=True, null=True,default=-1)
    image = models.ImageField(upload_to='Banner', null = True)
    is_active = models.BooleanField(blank = True, default = True)
    link = models.CharField(max_length=500, blank=True, null=True,default="")
    content = models.CharField(max_length=264 , blank=True, null=True,default="")

class RolesPermissions(models.Model):

    roleType = models.CharField(max_length=264 , blank=True, null=True,default="")
    roleDetails = models.CharField(max_length=264 , blank=True, null=True,default="")

    def __str__(self):
        return self.roleType

class Currency (models.Model):
    ''' This model class is for currency conversion '''
    currency_type = models.CharField (max_length=100, blank = True, null = True, default= "Taka") 
    value = models.FloatField (blank = True, null = True, default= 1.00)
    dates = models.DateTimeField (auto_now_add=True)
    role_id = models.IntegerField (blank= True, null = True,default=-1)

class ContactUs (models.Model):
    sender_name = models.CharField (max_length = 100, blank = True, null = True,default="")
    sender_email = models.EmailField(blank = True, null = True,default="")
    subject = models.CharField(max_length = 264, blank = True, null = True,default="")
    message = models.CharField (max_length = 10000, blank = True, null = True,default="")
    is_attended = models.BooleanField(blank = True, null = True, default = False)

#---------------------------------------------------------------------------------------------------------

class Settings(models.Model):
    ''' This model class is for settings '''
    tax = models.FloatField(blank = True, null = True,default=0.00)
    vat = models.FloatField(blank = True, null = True,default=0.00)
    role_id = models.IntegerField (blank= True, null = True,default=-1)
    point_value = models.FloatField(blank = True, null = True, default = 1.00)
    point_converted_value = models.FloatField(blank = True, null = True, default = 0.00)
    #dates = models.DateTimeField (auto_now_add=True)
    theme_id = models.IntegerField (blank= True, null = True,default=-1)


class Theme(models.Model):
    ''' This model class is for Theme details'''
    name = models.CharField(max_length=264, blank=True, null= True,default="")
    details = models.CharField (max_length=100000, blank= True, null= True,default="")

class APIs(models.Model):
    ''' This model class is for APIs '''
    name = models.CharField(max_length=264, blank= True, null= True,default="")
    details = models.CharField (max_length=100000, blank = True, null = True,default="")



#-------------------------------------Support---------------------------------

# Create your models here.
status = (
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
    
)


#sender_id is the user who makes the complain 
#receiver_id is the one from the support team who receives the comments
class Ticket(models.Model):
    
    title = models.CharField(max_length=255, null = True, blank = True,default="")
    sender_id = models.IntegerField(blank = True, null = True,default=-1)
    receiver_id = models.IntegerField(blank = True, null = True,default=-1)
    department = models.CharField(max_length=255, blank=True,default="")
    complain = models.TextField(blank = True,default="")
    #replies = ArrayField(models.TextField(blank = True))
    status = models.CharField(choices=status, max_length=155, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_attended = models.BooleanField(default=False)

    


    def __str__(self):
        return str(self.title)
        

    class Meta:
        ordering = ["-created"]


#For one user there will be one reply
#User_id refers to the user who makes the comment(customer,support)
class TicketReplies(models.Model):

    ticket_id = models.IntegerField(blank = False,default=-1)
    reply = models.TextField(blank=True,default="")
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(blank = True, null = True,default=-1)
    name = models.CharField(max_length=255,null=True)
    is_staff = models.BooleanField(default=False)


    def _str_(self):
        return str(self.reply)

#------------------------------ Email_Configuration---------------

class EmailConfig(models.Model):
    email_backend = models.CharField (max_length=64, default = "django.core.mail.backends.smtp.EmailBackend")
    email_host = models.CharField (max_length = 64, default = "smtp.gmail.com")
    email_port = models.IntegerField(default = 587)
    Tls_value = models.BooleanField(default = True)
    email_host_user = models.EmailField()
    email_host_password= models.CharField(max_length = 264)
    Ssl_value = models.BooleanField(default = False)
   
#---------------------------------Cart----------------------------------

# Create your models here.
# class Product(models.Model):
#     title = models.CharField(max_length=255, blank=True)
#     quantity = models.IntegerField(default = 10)
    

#     def __str__(self):
#         return str(self.id)






class ProductPrice(models.Model):
    product_id = models.IntegerField(default=-1)
    price = models.FloatField(default=0.00)
    purchase_price = models.FloatField(blank = True, null = True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    currency_id = models.IntegerField(default=-1)


    def __str__(self):
        return str(self.product_id)
    

class Order(models.Model):
    order =(
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid"),
    ("Cancelled", "Cancelled"),
    ("Not Ordered", "Not Ordered"),
    )
    order_status =  models.CharField(choices=order, max_length=155, default="Unpaid",blank=True,null=True)
    delivery = (
    ("To pay", "To pay"),
    ("To ship", "To ship"),
    ("Received", "Received"),
    ("Not Ordered", "Not Ordered"),
    ("Cancelled", "Cancelled"),
    )
    delivery_status = models.CharField(choices=delivery, max_length=155, default="To ship",blank=True,null=True)
    admin = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    admin_status = models.CharField(choices=admin, max_length=155, default="Processing",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    user_id = models.IntegerField(blank=True,null=True,default=-1)
    ip_address = models.CharField(max_length = 255,blank=True,null=True,default="")
    checkout_status = models.BooleanField(default=False,blank=True,null=True)
    ordered_date = models.DateField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True,default=-1)
    coupon = models.BooleanField(default=False,blank=True,null=True)
    coupon_code = models.CharField(max_length = 255,blank=True,null=True,default="")


    def __str__(self):
        return str(self.id)



class OrderDetails(models.Model):
    order_id = models.IntegerField(blank=True,null=True,default=-1)
    product_id = models.IntegerField(blank=True,null=True,default=-1)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_removed = models.BooleanField(default = False)
    total_quantity = models.IntegerField(default=0,blank=True,null=True)
    unit_price = models.FloatField(default=0.00,blank=True,null=True)
    total_price = models.FloatField(default=0.00,blank=True,null=True)
    unit_point = models.FloatField(default=0.00,blank=True,null=True)
    total_point = models.FloatField(default=0.00,blank=True,null=True)
    product_name = models.CharField(max_length=255,blank=True,null=True,default="")
    product_color = models.CharField(max_length = 255,blank=True,null=True,default="")
    product_size = models.CharField(max_length = 255,blank=True,null=True,default="")
    product_unit = models.CharField(max_length = 255,blank=True,null=True,default="")
    product_images = ArrayField(models.CharField(max_length=100000), blank=True, null=True,default=list)
    remaining = models.IntegerField(default=0,blank=True,null=True)
    admin =(
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Cancelled", "Cancelled"),
    )
    admin_status = models.CharField(choices=admin, max_length=155, default="Pending",blank=True,null=True)



    def __str__(self):
        return f'{self.order_id} X {self.product_id}'


class ProductPoint(models.Model):
    point = models.FloatField(blank=True,null=True,default=0.00)
    product_id = models.IntegerField(default=-1)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(blank=True,null=True)

    def __str__(self):
        return f'{self.id} X {self.product_id}'

class Userz(models.Model):
    address = models.TextField()
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return str(self.id)

class BillingAddress(models.Model):
    user_id = models.IntegerField(blank=True,null=True,default=-1)
    #address = models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_updated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True,default=-1)
    ip_address = models.CharField(max_length = 255,blank=True,default="")
    phone_number = models.CharField(max_length=100 ,blank=True,default="")
    name = models.CharField(max_length = 255,blank=True,default="")
    #gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    # city = models.CharField(max_length=100, blank= True, null= True,default="")
    # district = models.CharField(max_length=100, blank= True, null= True,default="")
    # road_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    # building_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    # apartment_number = models.CharField(max_length = 264,blank=True, null=True,default="")
    address = models.TextField(blank = True, default="")
    area = models.CharField(max_length=255,blank=True,default="")
    location = models.CharField(max_length=255,blank=True,default="")

    def __str__(self):
        return str(self.id)








    #--------------------------- Product --------------------------------

def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)

class ProductImage(models.Model):
    
    product_id = models.IntegerField(default= -1)
    #image= models.ImageField(upload_to='Products/', blank=True,null=True)
    product_image= models.ImageField(blank=True,null=True)
    image_url = models.CharField(max_length=255,blank=True,null=True,default="")
    content = models.CharField(max_length = 1500, blank = True, null = True,default="")


    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
      
        
        if self.product_image:
            return "{0}{1}".format(host_name,self.product_image.url)
        else:
            return " "
        
    
    def save(self, *args, **kwargs):
          self.image_url = self.image
          super(ProductImage, self).save(*args, **kwargs)


    
class Product(models.Model):
    admin_approval = (
    ("Processing", "Processing"),
    ("Confirmed", "Confirmed"),
    ("Cancelled", "Cancelled"),
    )
    seller = models.IntegerField(default=-1,blank=True)
    product_admin_status = models.CharField(choices=admin_approval, max_length=155, default="Processing",blank=True,null=True)

    category_id = models.IntegerField( blank=True , null=True,default=-1)
    sub_category_id = models.IntegerField( blank=True , null=True,default=-1)
    sub_sub_category_id = models.IntegerField( blank=True , null=True,default=-1)
    title = models.CharField(max_length=250 ,blank=True,default="")
    brand = models.CharField(max_length=120 , blank=True,default="" )
    date=models.DateTimeField(auto_now_add=True)
    #image = ArrayField(models.ImageField(upload_to=product_image_path, blank=True),null=True , blank=True)
    description = models.TextField(null=True, blank=True,default="")
    key_features=ArrayField(models.TextField(null=True , blank=True), null=True ,blank=True,default=list)
    is_deleted = models.BooleanField(default=False)
    properties= models.BooleanField(default=True)
    is_group = models.BooleanField(default=False)
    unit = models.CharField(max_length=200, null = True, blank=True,default="")
    warranty = models.CharField(max_length=200, null = True, blank=True,default="")
    origin = models.CharField(max_length=200, null = True, blank=True,default="")
    shipping_country = models.CharField(max_length=200, null = True, blank=True,default="")



class Variation(models.Model):
    product_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="")
    sale_price = models.FloatField(null=True, blank=True,default=0.00)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) #refer none == unlimited amount

    def __unicode__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    # def get_html_price(self):
    #   if self.sale_price is not None:
    #       html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
    #   else:
    #       html_text = "<span class='price'>%s</span>" %(self.price)
    #   return mark_safe(html_text)

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def add_to_cart(self):
        return "%s?item=%s&qty=1" %(reverse("cart"), self.id)

    def remove_from_cart(self):
        return "%s?item=%s&qty=1&delete=True" %(reverse("cart"), self.id)

    def get_title(self):
        return "%s - %s" %(self.product.title, self.title)



def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    # variations = product.variation_set.all()
    # if variations.count() == 0:
    #   new_var = Variation()
    #   new_var.product = product
    #   new_var.title = "Default"
    #   new_var.price = product.price
    #   new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)



class Category(models.Model):
    #product_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120, unique=True,null=True,blank=True)
    category_id = models.IntegerField(default=-1)
    active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    level = models.CharField(max_length=120, default="First")
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @property
    def sub(self):


        if self.id: 

            category_id = self.id


        else:

            category_id = 0 

        return category_id 

            


    def save(self, *args, **kwargs):

        self.category_id = self.sub
        super(Category, self).save(*args, **kwargs)




class Sub_Category(models.Model):
    category_id = models.IntegerField(default=-1)
    sub_category_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="None",null=True,blank=True)
    active = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    level = models.CharField(max_length=120,default="Second")
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    children = ArrayField(models.CharField(max_length=120,null=True , blank=True), null=True ,blank=True,default=list)


    @property
    def sub(self):


        if self.id: 

            sub_cat = self.id


        else:

            sub_cat = 0 

        return sub_cat

            


    def save(self, *args, **kwargs):

        self.sub_category_id = self.sub
        super(Sub_Category, self).save(*args, **kwargs)

    # @property
    # def sub(self):


    #     if self.id is not None: 

    #         print("entering here")



    #         subsub = []

    #         try:

    #             sub_sub = Sub_Sub_Category.objects.filter(sub_category_id=self.id)


    #         except:

    #             sub_sub = None 

    #         if sub_sub:
    #             print(here)

    #             subsub = list(existing.values_list('title',flat=True))

    #         else:

    #             subsub



    #     def save(self, *args, **kwargs):
    #       self.sub_sub_categories = self.sub
    #       super(Sub_category, self).save(*args, **kwargs)













class Sub_Sub_Category(models.Model):
    sub_category_id = models.IntegerField(default=-1)
    title = models.CharField(max_length=120,default="None",null=True,blank=True)
    active = models.BooleanField(default=False)
    level = models.CharField(max_length=120,default="Third")
    #slug = models.SlugField(unique=True)
    #active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    sub_sub_category_id = models.IntegerField(default=-1)
    is_active = models.BooleanField(default=False)

    @property
    def sub(self):


        if self.id: 

            sub_sub = self.id


        else:

            sub_sub = 0 

        return sub_sub 

            


    def save(self, *args, **kwargs):

        self.sub_sub_category_id = self.sub
        super(Sub_Sub_Category, self).save(*args, **kwargs)


class GroupProduct(models.Model):
    products_ids = ArrayField(models.IntegerField( null=True , blank=True),null=True , blank=True,default=list)
    title = models.CharField(max_length=120, blank = True, null = True,default="")
    #slug = models.SlugField(unique=True , blank=True)
    startdate=models.DateField(auto_now_add=True,null=True , blank=True)
    enddate=models.DateField(null=True , blank=True)
    flashsellname = models.CharField(max_length=120, blank = True , null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    product_id = models.IntegerField(null = True, blank = True)

    def __unicode__(self):
        return self.title

#------------------------------------- Product_Comments--------------------------------
class Comment(models.Model):
    comment = models.TextField(blank = True)
    date_created = models.DateField(auto_now_add=True)
    product_id = models.IntegerField(default=0)

    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.comment

    class Meta:
        ordering = ["-date_created"]


class CommentReply(models.Model):
    comment_id = models.IntegerField(blank = True,null=True)
    reply = models.TextField(blank = True)
    date_created = models.DateField(auto_now_add=True)
    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.reply

    class Meta:
        ordering = ["-date_created"]

#------------------------------------- Product_Reviews--------------------------------
class Reviews(models.Model):
    product_id = models.IntegerField(default=0)
    
    user_id = models.IntegerField(blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)
    content = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'product_reviews' ,null=True, blank = True)
    num_stars = (
        (1 , "Worst"),
        (2 , "Bad"),
        (3 , "Not Bad"),
        (4 , "Good"),
        (5 , "Excellent"),
        )
    rating = models.IntegerField(choices=num_stars,blank=True,null=True)
    date_created = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date_created"]

# -------------------------- Product Code ------------------------------------

class ProductCode (models.Model):
    Barcode_img = models.CharField(max_length = 264,null = True, blank = False)
    date = models.DateField(auto_now_add=True)
    product_id = models.IntegerField(blank = False, null = True)
    Barcode = models.CharField(max_length = 264,null = True, blank = False)
    SKU = models.CharField(max_length = 264,null = True, blank = False)
    SKU_img = models.CharField(max_length = 264,null = True, blank = False)

#------------------------- Product Discount ---------------------------------

class discount_product(models.Model):
    Sales_type = (

        ('FLAT', 'Flat'),
        ('FLASH', 'Flash'),
        ('WHOLESALE', 'Wholesale'),
    )
    discount_type = models.CharField(max_length=264, blank=True, null= True,choices=Sales_type)
    amount = models.FloatField (blank = False, null = True, default =0.00)
    start_date = models.DateField (auto_now_add=True,blank=True,null=True)
    end_date = models.DateField (blank = False, null = True)
    max_amount = models.FloatField (blank = False, null = True, default =0)
    group_product_id = models.IntegerField(blank=False, null=True)
    product_id = models.IntegerField(blank=False, null=True)


# ---------------------- Product Cupon -------------------------------------------

class Cupons(models.Model):
    cupon_code = models.CharField(max_length= 264, blank = True, null = True)
    amount = models.FloatField (blank = True, null = True)
    start_from = models.DateField(blank = True, null = True)
    valid_to = models.DateField(blank = True, null = True)
    is_active = models.BooleanField()

# ---------------------------------- FAQ-----------------------------------------

class FAQ (models.Model):
    question = models.CharField(max_length = 264, blank = True, null = True)
    ans = models.CharField (max_length = 3000, blank = True, null = True)
    date = models.DateField(auto_now_add=True)


# ----------------------------------- Product Inventory ---------------------------
class ProductSpecification(models.Model):
    product_id = models.IntegerField(default=-1)
    size = models.CharField(max_length=200, null = True, blank=True,default="")
    #unit = models.CharField(max_length=200, null = True, blank=True,default="")
    weight = models.CharField(max_length = 255,blank=True,null=True,default="")
    #color = ArrayField(models.CharField(max_length=200,default="abc"),default=list,blank=True)
    color = models.CharField(max_length=200,null= True, blank=True,default="")
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return str(self.id)


    @property
    def total(self):


        try:

            warehouses = WarehouseInfo.objects.filter(specification_id=self.id)


        except:

            warehouses = None 


        if warehouses:

            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)


        else:

            w_quantity = 0



        try:

            shops = ShopInfo.objects.filter(specification_id=self.id)


        except:

            shops = None 


        if shops:

            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)


        else:

            s_quantity = 0



        total_quantity = w_quantity + s_quantity

        return total_quantity


    def save(self, *args, **kwargs):

        self.quantity = self.total
        # print("save er moddhe")
        # print(self.quantity)
        super(ProductSpecification, self).save(*args, **kwargs)
        # print("save er pore")
        # print(self.quantity)












    # @property
    # def quantity(self):
    #     total = self.warehouse_quantity + self.shop_quantity
    #     float_total = format(total, '0.2f')
    #     return float_total

    # @property
    # def total(self):

    #     #link ='/media/'+'Product/'+str(self.product_image)
      
    #     # print(self.product_image)
    

    #     print("id ase")

    #     try:
    #         warehouses = Warehouse.objects.filter(specification_id=self.id)

    #     except:

    #         warehouses = None

    #     print(warehouses)

    #     if warehouses:

    #         w_quantity_list = list(warehouses.values_list('product_quantity',flat = True))
    #         w_quantity = sum(w_quantity_list)
    #         print(w_quantity)

    #     else:
    #         w_quantity = 0



    #     try:
    #         shops = Shop.objects.filter(specification_id=self.id)

    #     except:

    #         shops = None

    #     if shops:

    #         s_quantity_list = list(shops.values_list('product_quantity',flat = True))
    #         s_quantity = sum(s_quantity_list)
    #         print(s_quantity)

    #     else:
    #         s_quantity = 0


    #     total_quantity = w_quantity + s_quantity

       


    #     return total_quantity








        
    
    # def save(self, *args, **kwargs):

    #     self.quantity = self.total
    #     print("save er moddhe")
    #     print(self.quantity)
    #     super(ProductSpecification, self).save(*args, **kwargs)
    #     print("save er pore")
    #     print(self.quantity)




# class Warehouse(models.Model):
#     warehouse_name = models.CharField(max_length=264, blank=True, null= True)
#     warehouse_location = models.CharField(max_length=2048, blank=True, null= True)
#     product_quantity = models.IntegerField(blank=False, null=True,default=0)
#     specification_id = models.IntegerField(blank=False, null=True,default=-1)
#     date = models.DateField (auto_now_add=True,blank=True,null=True)
#     shop_quantity = models.IntegerField(blank=False, null=True,default=0)
#     warehouse_quantity = models.IntegerField(blank=False, null=True,default=0)



#     @property
#     def shop(self):

#         try:
#             spec = Shop.objects.filter(specification_id=self.specification_id)

#         except:
#             spec = None


#         if spec:

#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)


#         else:

#             s_quantity = 0




#         return s_quantity



#     @property
#     def warehouse(self):

#         try:
#             spec = Warehouse.objects.filter(specification_id=self.specification_id)

#         except:
#             spec = None


#         if spec:

#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)


#         else:

#             s_quantity = 0




#         return s_quantity






#     def save(self, *args, **kwargs):

#         self.shop_quantity = self.shop
#         self.warehouse_quantity = self.warehouse
#         super(Warehouse, self).save(*args, **kwargs)
#         # print(self.shop_quantity)
#         # print(self.warehouse_quantity)
#         try:
#             ware = Warehouse.objects.get(id = self.id)
#             print(ware)

#         except:
#             ware = None

#         if ware:

#             warehouse_quantity = ware.warehouse_quantity
#             shop_quantity = ware.shop_quantity
#             print(warehouse_quantity)
#             print(shop_quantity)
#             total_quantity = warehouse_quantity + shop_quantity


#             try:

#                 prod_spec = ProductSpecification.objects.get(id=self.specification_id)

#             except:

#                 prod_spec = None

#             if prod_spec:
#                 prod_spec.quantity = total_quantity
#                 prod_spec.save()








# class Shop(models.Model):
#     shop_name = models.CharField(max_length=264, blank=True, null= True)
#     shop_location = models.CharField(max_length=2048, blank=True, null= True)
#     product_quantity = models.IntegerField(blank=False, null=True)
#     specification_id = models.IntegerField(blank=False, null=True)
#     date = models.DateField (auto_now_add=True,blank=True,null=True)
#     shop_quantity = models.IntegerField(blank=False, null=True,default=0)
#     warehouse_quantity = models.IntegerField(blank=False, null=True,default=0)


#     # @property
#     # def save_specification(self):


#     #     spec = ProductSpecification()

#     #     # spec_id = spec.id
#     #     spec.save()
#     #     # print("after save")
#     #     # print(spec.total_quantity)


#     #     return 1





#     # def save(self, *args, **kwargs):

#     #     self.specification_id = self.save_specification
#     #     super(Shop, self).save(*args, **kwargs)


#     @property
#     def shop(self):

#         try:
#             spec = Shop.objects.filter(specification_id=self.specification_id)

#         except:
#             spec = None


#         if spec:

#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)


#         else:

#             s_quantity = 0




#         return s_quantity



#     @property
#     def warehouse(self):

#         try:
#             spec = Warehouse.objects.filter(specification_id=self.specification_id)

#         except:
#             spec = None


#         if spec:

#             s_list = list(spec.values_list('product_quantity',flat = True))
#             s_quantity = sum(s_list)


#         else:

#             s_quantity = 0




#         return s_quantity






#     def save(self, *args, **kwargs):

#         self.shop_quantity = self.shop
#         self.warehouse_quantity = self.warehouse
#         super(Shop, self).save(*args, **kwargs)
#         # print(self.shop_quantity)
#         # print(self.warehouse_quantity)
#         try:
#             ware = Shop.objects.get(id = self.id)
#             print(ware)

#         except:
#             ware = None

#         if ware:

#             warehouse_quantity = ware.warehouse_quantity
#             shop_quantity = ware.shop_quantity
#             print(warehouse_quantity)
#             print(shop_quantity)
#             total_quantity = warehouse_quantity + shop_quantity

#             try:

#                 prod_spec = ProductSpecification.objects.get(id=self.specification_id)

#             except:

#                 prod_spec = None

#             if prod_spec:
#                 prod_spec.quantity = total_quantity
#                 prod_spec.save()
      



class Inventory_Price(models.Model):

    product_id = models.IntegerField( blank=True , null=True,default=-1)
    specification_id = models.IntegerField( blank=True , null=True,default=-1)
    quantity = models.IntegerField( blank=True ,default=0)
    date = models.DateField(blank=True,default="")
    price = models.IntegerField(blank=True,default=0)

 

    def __str__(self):
        return f'{self.product_id} X {self.specification_id}'



# class OrderInfo(models.Model):

#     order_id = models.IntegerField( blank=True , null=True,default=-1)



class Warehouse(models.Model):

    warehouse_name = models.CharField(max_length=264, blank=True, null= True)
    warehouse_location = models.CharField(max_length=264, blank=True, null= True)



class Shop(models.Model):


    shop_name = models.CharField(max_length=264, blank=True, null= True)
    shop_location = models.CharField(max_length=264, blank=True, null= True)


class WarehouseInfo(models.Model):

    warehouse_id = models.IntegerField(blank=True,default=-1)
    specification_id = models.IntegerField(blank=True,default=-1)
    product_id = models.IntegerField(blank=True,default=-1)
    quantity = models.IntegerField(blank=True,default=0)




    def save(self, *args, **kwargs):


        #self.shop_quantity = self.shop
        # self.warehouse_quantity = self.warehouse
        super(WarehouseInfo, self).save(*args, **kwargs)
        # print(self.shop_quantity)
        # print(self.warehouse_quantity)
        try:

            warehouses = WarehouseInfo.objects.filter(specification_id=self.specification_id)


        except:

            warehouses = None 


        if warehouses:

            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)


        else:

            w_quantity = 0



        try:

            shops = ShopInfo.objects.filter(specification_id=self.specification_id)


        except:

            shops = None 


        if shops:

            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)


        else:

            s_quantity = 0



        total_quantity = w_quantity + s_quantity

        
        



        try:
            

            prod_spec = ProductSpecification.objects.get(id=self.specification_id)

            


        except:

            

            prod_spec = None

           

        if prod_spec:
            prod_spec.quantity = total_quantity
            prod_spec.save()

           

    





class ShopInfo(models.Model):

    shop_id = models.IntegerField(blank=True,default=-1)
    specification_id = models.IntegerField(blank=True,default=-1)
    quantity = models.IntegerField(blank=True,default=0)
    product_id = models.IntegerField(blank=True,default=-1)


    def save(self, *args, **kwargs):

        

        #self.shop_quantity = self.shop
        # self.warehouse_quantity = self.warehouse
        super(ShopInfo, self).save(*args, **kwargs)
        # print(self.shop_quantity)
        # print(self.warehouse_quantity)
        try:

            warehouses = WarehouseInfo.objects.filter(specification_id=self.specification_id)


        except:

            warehouses = None 


        if warehouses:

            w_quantity_list = list(warehouses.values_list('quantity',flat = True))
            w_quantity = sum(w_quantity_list)


        else:

            w_quantity = 0



        try:

            shops = ShopInfo.objects.filter(specification_id=self.specification_id)


        except:

            shops = None 


        if shops:

            s_quantity_list = list(shops.values_list('quantity',flat = True))
            s_quantity = sum(s_quantity_list)


        else:

            s_quantity = 0



        total_quantity = w_quantity + s_quantity

        
        



        try:
            

            prod_spec = ProductSpecification.objects.get(id=self.specification_id)

            


        except:

            

            prod_spec = None

           

        if prod_spec:
            prod_spec.quantity = total_quantity
            prod_spec.save()



class inventory_report(models.Model):

    product_id = models.IntegerField(blank=False, null=False)
    debit = models.IntegerField(blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    warehouse_id = models.IntegerField(blank=True, null=True)
    shop_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True,null=True , blank=True)
    selling_price = models.FloatField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)



class OrderInfo(models.Model):


    order_id = models.IntegerField(blank=True,default=-1)
    billing_address_id = models.IntegerField(blank=True,default=-1)
    area_id = models.IntegerField(blank=True,default=-1)
    company_id = models.IntegerField(blank=True,default=-1)
    company_name = models.CharField(max_length=264,blank=False,default= "")
    company_details = models.TextField(blank = True,default="")
    delivery_type_id = models.IntegerField(blank=True,default=-1)
    delivery_date = models.DateField(blank=True,default="")
    days = models.IntegerField(blank=True,default=0)
    host_site = models.CharField(max_length=264,blank=True,default= "")
    location_id = models.IntegerField(blank=True,default=-1)
    location_details = models.TextField(blank = True,default="")
    payment_type = models.CharField(max_length=264,blank=True,default= "")
    total_amount = models.FloatField(blank=True,default=0.00)



class Invoice(models.Model):
    order_id = models.IntegerField(blank=False,default=-1)
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

class ProductBrand (models.Model):
    Brand_name = models.CharField(max_length=264,blank=True,default= "")
    Brand_owner = models.CharField(max_length=264,blank=True,default= "")
    Brand_country = models.CharField(max_length=264,blank=True,default= "")
    created_date = models.DateField (auto_now_add=True,blank=True,null=True)
    

