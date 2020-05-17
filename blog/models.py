from PIL import Image
from django.db import models
from django.utils import timezone
from accounts.models import Profile

class Blog(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    content=models.TextField()
    image=models.ImageField(default='default.jpg',upload_to='blogs/')
    date=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.profile.user.first_name} blog'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.image.path)
        if img.height > 600 or img.width > 600:
            output_size=(600,600)
            img.thumbnail(output_size)
            img.save(self.image.path)


