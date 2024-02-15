from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
import uuid
from datetime import datetime
# Create your models here.

'''Use AbstractUser to modfy the default user model and add new fields (use AbstractBaseUser to create admin model from scracth)'''

class CustomUser(AbstractUser):
    #username=None --> Not use default username for login
    username = None
    email = models.EmailField(unique=True)
    #USERNAME_FIELD = 'email' --> email as the default field to create user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    #use the CustomUserManager for create custom user
    objects = CustomUserManager()

class OTP(models.Model):
    otp=models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default=None)
    #for 3 time attempts 
    failed_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email     
    
class Profile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)    
    id=models.UUIDField(primary_key=True)
    user_create=models.DateTimeField(default=datetime.now)
    profileimage=models.ImageField(upload_to='profilepic',default='default.png')
    name=models.CharField(max_length=50,blank=True)
    about=models.TextField(blank=True)
    current_study=models.CharField(max_length=50,blank=True)
    self_learner = models.BooleanField(default=False)
    current_teach=models.CharField(max_length=50,blank=True)
    backgroundimage=models.ImageField(upload_to='backgroundpic',default='default_cover_img.png')
    no_of_followers=models.IntegerField(default=0)
    comment_by_user=models.IntegerField(default=0)
   
    def __str__(self):  
        return self.user.email

class Post(models.Model):
    my_post=models.FileField(upload_to='allpost',)
    post_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    poster_profile=models.ForeignKey(Profile,on_delete=models.CASCADE ,null=True,default=None)
    post_time=models.DateTimeField(default=datetime.now)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    no_of_like=models.IntegerField(default=0)
    no_of_coment=models.IntegerField(default=0)
    no_of_viewer=models.IntegerField(default=0)
    caption=models.CharField(blank=True,max_length=150)
    about=models.TextField(blank=True)
    postshow= models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.my_post.name


class demo(models.Model):
    photo=models.ImageField(upload_to='profilepic',default='default.jpg')    
    def __str__(self):
        return 'chiku'
    

class Followerscount(models.Model):
    follower=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='followers')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='following')
    followtime=models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.user.email
    
class Like_post(models.Model):
    post_id=models.CharField(max_length=500)    
    like_user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    like_time=models.DateField(default=datetime.now)

    def __str__(self):
        return self.like_user.email
    
#Comment
class Comment(models.Model):
    text=models.TextField()
    comment_time=models.DateField(default=datetime.now)
    comment_by=models.ForeignKey(Profile,on_delete=models.CASCADE)
    comment_post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment_by.user
    


