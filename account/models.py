from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,UserManager
import datetime
from .utilis import upload_image
# Create your models here.

# --------------------------------------------------------------------------------------------------------------------------------------
class CustomerManager(BaseUserManager):
    def create_user(self,mobile_number,email='',name='',family='',gender=None,active_code=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل اجباری میباشد')
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            gender=gender,
            active_code=active_code
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
# -----------------------------------------------------------------------

    def create_superuser(self,mobile_number,email,name,family,gender=None,active_code=None,password=None):
        user=self.create_user(
            mobile_number=mobile_number, 
            email=email,
            name=name,
            family=family,
            gender=gender,
            active_code=active_code,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


# --------------------------------------------------------------------------------------------------------------------------------------
class CustomerUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,unique=True,verbose_name="شماره موبایل")
    email=models.CharField(max_length=200,blank=True)
    name=models.CharField(max_length=50,blank=True)
    family=models.CharField(max_length=50,blank=True)
    Gender_choice=(('m','male'),('f','female'))
    gender=models.CharField(max_length=50,blank=True,null=True,choices=Gender_choice,default='m')
    regester_date=models.DateField(default=datetime.datetime.now)
    is_active=models.BooleanField(default=False)
    active_code=models.CharField(max_length=50,blank=True,null=True)
    is_admin=models.BooleanField(default=False)
    
    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS = ['email','name','family']
    
    objects=CustomerManager()
# -----------------------------------------------------------------------
    def __str__(self) :
        return f'{self.name}\t{self.family}'
    
# -----------------------------------------------------------------------
    @property         
    def is_staff(self):
        return self.is_admin
    
# --------------------------------------------------------------------------------------------------------------------------------------
class Customer(models.Model):
    user=models.OneToOneField(CustomerUser,on_delete=models.CASCADE,primary_key=True)
    phone=models.CharField(max_length=11,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    upload_image=upload_image('images','customer')
    image_name=models.ImageField(upload_to=upload_image.upload_to,verbose_name='تصویر پروفایل')
    
    def __str__(self) :
        return f'{self.user}'
    
    


      

    
    