from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

class Student(models.Model):
  name = models.CharField(max_length=50)
  age= models.CharField( max_length=2)
  roll_num =models.CharField( max_length=20)
  phone_num=models.BigIntegerField()
  email=models.EmailField()
  address =models.TextField()

  def __str__(self):
      return self.name
  
class City(models.Model):
   name=models.CharField(max_length=20)

   def __str__(self):
      return self.name
   
 
   class Meta:
    verbose_name_plural = 'cities'

class profile(models.Model):
   name=models.CharField(max_length=50)
   phone_number=PhoneNumberField()
   email=models.EmailField()
   instgram=models.CharField(max_length=50)
   pic=models.ImageField(upload_to="profile_pictures",null=True,blank=True)

   def __str__(self):
       return self.name
   

  
