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
    username = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(max_length=255,unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_suplier  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length= 64)

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

    name = models.CharField(max_length = 264, null = True, blank = True)
    email = models.CharField(max_length = 64, null= True, blank = True)
    profile_picture = models.ImageField(upload_to='Profile_Img', blank=True)
    phone_number = models.CharField(max_length=100 ,  null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    city = models.CharField(max_length=100, blank= True, null= True)
    district = models.CharField(max_length=100, blank= True, null= True)
    road_number = models.CharField(max_length = 264,blank=True, null=True)
    building_number = models.CharField(max_length = 264,blank=True, null=True)
    apartment_number = models.CharField(max_length = 264,blank=True, null=True)
    user_id = models.IntegerField(blank = True, null = True)


class user_relation (models.Model):
    verified_user_id = models.IntegerField (blank = True, null = True)
    non_verified_user_id = models.IntegerField (blank = True, null = True)

# class DeactivateUser(TimeStampedModel):
#     user = models.OneToOneField(User, related_name='deactivate', on_delete=models.CASCADE)
#     deactive = models.BooleanField(default=True)

class user_balance(models.Model):
    wallet = models.FloatField(blank = False, null = True, default=0)
    point = models.FloatField(blank = False, null = True, default = 0)
    dates = models.DateTimeField (auto_now_add=True)
    user_id = models.IntegerField(blank=False, null=True)
    ip_id = models.IntegerField(blank=False, null=True)

class Guest_user(models.Model):
    ip_address = models.CharField(max_length = 64, blank = False, null = True)
    Date = models.DateField (blank = False, null = True)
# ------------------------- Advertisement ---------------------

class Advertisement(models.Model):

    image = models.ImageField(upload_to='Advertisement',null = True)
    ad_link = models.CharField(max_length=255,blank=True,null = True)
    content = models.CharField(max_length=255,blank=True,null = True)
    click_count = models.IntegerField(default =0)
    view_count = models.IntegerField(default=0)
    total_click_count = models.IntegerField(default =0)
    total_view_count = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.content)

# ----------------------------- Impression ----------------------------

class ProductImpression (models.Model):

    Users = ArrayField(models.IntegerField(), blank=True, null=True,default=list)
    product_id = models.IntegerField (null = False)
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
    name = models.CharField(max_length=500 , blank=True, null=True)
    logo = models.ImageField(upload_to='Logo', null = True)
    address = models.TextField(max_length=1500,blank=True, null=True )
    icon = models.ImageField(upload_to='Icon', null = True)
    Facebook = models.CharField(max_length=264 , blank=True, null=True)
    twitter = models.CharField(max_length=264 , blank=True, null=True)
    linkedin = models.CharField(max_length=264 , blank=True, null=True)
    youtube = models.CharField(max_length=264 , blank=True, null=True)
    email = models.CharField(max_length=264 , blank=True, null=True)
    phone = models.CharField(max_length=264 , blank=True, null=True)
    help_center = models.CharField(max_length=264 , blank=True, null=True)
    About = models.CharField(max_length=5000 , blank=True, null=True)
    policy = ArrayField(models.CharField(max_length=100000), blank=True, null=True,default=list)
    terms_condition= ArrayField(models.CharField(max_length=100000), blank=True, null=True,default=list)
    slogan = models.CharField(max_length=264 , blank=True, null=True)
    cookies = models.CharField(max_length=10000 , blank=True, null=True)
    


class Banner(models.Model):

    count = models.IntegerField( blank=False, null=False )
    set_time = models.IntegerField(null = True)


class Banner_Image(models.Model):
    # this call is for uploading banner images
    Banner_id = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='Banner', null = True)
    link = models.CharField(max_length=500, blank=True, null=True)
    content = models.CharField(max_length=264 , blank=True, null=True)

class RolesPermissions(models.Model):

    roleType = models.CharField(max_length=264 , blank=True, null=True)
    roleDetails = models.CharField(max_length=264 , blank=True, null=True)

    def __str__(self):
        return self.roleType

class Currency (models.Model):
    ''' This model class is for currency conversion '''
    currency_type = models.CharField (max_length=100, blank = True, null = True, default= "Taka") 
    value = models.FloatField (blank = True, null = True, default= 1.00)
    dates = models.DateTimeField (auto_now_add=True)
    role_id = models.IntegerField (blank= True, null = True)

class ContactUs (models.Model):
    sender_name = models.CharField (max_length = 100, blank = True, null = True)
    sender_email = models.EmailField(blank = True, null = True)
    subject = models.CharField(max_length = 264, blank = True, null = True)
    message = models.CharField (max_length = 10000, blank = True, null = True)
    is_attended = models.BooleanField(blank = True, null = True, default = False)

#---------------------------------------------------------------------------------------------------------

class Settings(models.Model):
    ''' This model class is for settings '''
    tax = models.FloatField(blank = True, null = True)
    vat = models.FloatField(blank = True, null = True)
    role_id = models.IntegerField (blank= True, null = True)
    point_value = models.FloatField(blank = True, null = True, default = 1.00)
    point_converted_value = models.FloatField(blank = True, null = True, default = 0.00)
    #dates = models.DateTimeField (auto_now_add=True)
    theme_id = models.IntegerField (blank= True, null = True)


class Theme(models.Model):
    ''' This model class is for Theme details'''
    name = models.CharField(max_length=264, blank=True, null= True)
    details = models.CharField (max_length=100000, blank= True, null= True)

class APIs(models.Model):
    ''' This model class is for APIs '''
    name = models.CharField(max_length=264, blank= True, null= True)
    details = models.CharField (max_length=100000, blank = True, null = True)



#-------------------------------------Support---------------------------------

# Create your models here.
status = (
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
    
)


#sender_id is the user who makes the complain 
#receiver_id is the one from the support team who receives the comments
class Ticket(models.Model):
    
    title = models.CharField(max_length=255, null = True, blank = True)
    sender_id = models.IntegerField(blank = True, null = True)
    receiver_id = models.IntegerField(blank = True, null = True)
    department = models.CharField(max_length=255, blank=True)
    complain = models.TextField(blank = True)
    #replies = ArrayField(models.TextField(blank = True))
    status = models.CharField(choices=status, max_length=155, default="pending")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    


    def __str__(self):
        return str(self.title)
        

    class Meta:
        ordering = ["-created"]


#For one user there will be one reply
#User_id refers to the user who makes the comment(customer,support)
class TicketReplies(models.Model):

    ticket_id = models.IntegerField(blank = False)
    reply = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(blank = True, null = True)

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
    product_id = models.IntegerField(default=1)
    price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    currency_id = models.IntegerField(default=1)


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
    delivery_status = models.CharField(choices=delivery, max_length=155, default="To pay",blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    user_id = models.IntegerField(blank=True,null=True)
    ip_address = models.CharField(max_length = 255,blank=True,null=True)
    checkout_status = models.BooleanField(default=False,blank=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)


    def __str__(self):
        return str(self.id)



class OrderDetails(models.Model):
    order_id = models.IntegerField(blank=True,null=True)
    product_id = models.IntegerField(blank=True,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_removed = models.BooleanField(default = False)
    total_quantity = models.IntegerField(default=0,blank=True,null=True)
    unit_price = models.IntegerField(default=0,blank=True,null=True)
    total_price = models.IntegerField(default=0,blank=True,null=True)
    unit_point = models.IntegerField(default=0,blank=True,null=True)
    total_point = models.IntegerField(default=0,blank=True,null=True)
    product_name = models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return f'{self.order_id} X {self.product_id}'


class ProductPoint(models.Model):
    point = models.FloatField(blank=True,null=True)
    product_id = models.IntegerField(default=1)
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
    user_id = models.IntegerField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    date_updated = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    non_verified_user_id = models.IntegerField(blank=True,null=True)
    ip_address = models.CharField(max_length = 255,blank=True,null=True)

    def __str__(self):
        return str(self.id)


class ProductSpecification(models.Model):
    product_id = models.IntegerField(default=1)
    size = ArrayField(models.CharField(max_length=200), blank=True)
    unit = ArrayField(models.CharField(max_length=200), blank=True)
    weight = models.CharField(max_length = 255,blank=True,null=True)
    #color = ArrayField(models.CharField(max_length=200,default="abc"),default=list,blank=True)
    color = ArrayField(models.CharField(max_length=200),null= True, blank=True)

    def __str__(self):
        return str(self.product_id)




    #--------------------------- Product --------------------------------

def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)

class ProductImage(models.Model):
    
    product_id = models.IntegerField(default= 0)
    #image= models.ImageField(upload_to='Products/', blank=True,null=True)
    product_image= models.ImageField(blank=True,null=True)

    
    
    image_url = models.CharField(max_length=255,blank=True,null=True)


    @property
    def image(self):

        #link ='/media/'+'Product/'+str(self.product_image)
    
        return "{0}{1}".format(host_name,self.product_image.url)
        
       


    def save(self, *args, **kwargs):
          #self.unique_id = self.get_unique_id()
          #print(self.image_url())
        
          # print(host_name)
          # print(self.image)
          # print(self.image.url)

          # print(self.image_url)
          print(self.product_image.url)
          print(self.image)
          self.image_url = self.image
          #print(self.image_urls)
          super(ProductImage, self).save(*args, **kwargs)



    
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    category_id = models.IntegerField( blank=True , null=True)
    title = models.CharField(max_length=250 ,blank=True)
    brand = models.CharField(max_length=120 , blank=True )
    date=models.DateTimeField(auto_now_add=True)
    #image = ArrayField(models.ImageField(upload_to=product_image_path, blank=True),null=True , blank=True)
    description = models.TextField(null=True, blank=True)
    key_features=ArrayField(models.TextField(null=True , blank=True), null=True ,blank=True)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    properties= models.BooleanField(default=True)





class Variation(models.Model):
	product_id = models.IntegerField()
	title = models.CharField(max_length=120)
	sale_price = models.FloatField(null=True, blank=True)
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
	# 	if self.sale_price is not None:
	# 		html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
	# 	else:
	# 		html_text = "<span class='price'>%s</span>" %(self.price)
	# 	return mark_safe(html_text)

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
	# 	new_var = Variation()
	# 	new_var.product = product
	# 	new_var.title = "Default"
	# 	new_var.price = product.price
	# 	new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)



class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	#slug = models.SlugField(unique=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __unicode__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug })


class GroupProduct(models.Model):
	products_ids = ArrayField(models.IntegerField( null=True , blank=True),null=True , blank=True)
	title = models.CharField(max_length=120, unique=True)
	#slug = models.SlugField(unique=True , blank=True)
	startdate=models.DateTimeField(null=True , blank=True)
	enddate=models.DateTimeField(null=True , blank=True)
	flashsellname=models.name = models.CharField(max_length=120, blank = True , null=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	product_id = models.IntegerField(null = True, blank = True)

	def __unicode__(self):
		return self.title

#------------------------------------- Product_Comments--------------------------------
class Comment(models.Model):
    comment = models.TextField(blank = True)
    date_created = models.DateTimeField(auto_now_add=True)
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
    date_created = models.DateTimeField(auto_now_add=True)
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
    image = models.ImageField(upload_to = 'product_reviews' , blank = True)
    num_stars = (
        (1 , "Worst"),
        (2 , "Bad"),
        (3 , "Not Bad"),
        (4 , "Good"),
        (5 , "Excellent"),
        )
    rating = models.IntegerField(choices=num_stars,blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)


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

#------------------------- Product Discount ---------------------------------

class discount_product(models.Model):
    Sales_type = (

        ('FLAT', 'Flat'),
        ('FLASH', 'Flash'),
        ('WHOLESALE', 'Wholesale'),
    )
    discount_type = models.CharField(max_length=264, blank=True, null= True,choices=Sales_type)
    amount = models.FloatField (blank = False, null = True, default =0)
    start_date = models.DateField (blank = False, null = True)
    end_date = models.DateField (blank = False, null = True)
    max_amount = models.FloatField (blank = False, null = True, default =0)
    group_product_id = models.IntegerField(blank=False, null=True)
    product_id = models.IntegerField(blank=False, null=True)


# ---------------------- Product Cupon -------------------------------------------

class Cupons(models.Model):
    cupon_code = models.CharField(max_length= 264, blank = True, null = True)
    amount = models.FloatField (blank = True, null = True)
    start_from = models.DateField( auto_now_add = True)
    valid_to = models.DateField(blank = True, null = True)
    is_active = models.BooleanField()

# ---------------------------------- FAQ-----------------------------------------

class FAQ (models.Model):
    question = models.CharField(max_length = 264, blank = True, null = True)
    ans = models.CharField (max_length = 3000, blank = True, null = True)
    date = models.DateField(auto_now_add=True)
