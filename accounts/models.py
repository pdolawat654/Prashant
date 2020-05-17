from PIL import Image
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg',upload_to='profile_pics')
    phone=models.CharField(max_length=10)
    dob=models.CharField(max_length=20)
    workat=models.CharField(max_length=50)
    branch=models.CharField(max_length=20)
    passout=models.CharField(max_length=10)
    otp=models.CharField(max_length=6)
    verify=models.CharField(max_length=1,default=0)
    def __str__(self):
        return f'{self.user.first_name} Profile'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size=(400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)