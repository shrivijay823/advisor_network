from django.db import models
from django.contrib.auth.models import User

class Advisor(models.Model):
    name=models.CharField(max_length=30)
    dp=models.ImageField(null=True,blank=True,upload_to='images/',default='default.png')
    

class booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    advisor=models.ForeignKey(Advisor,on_delete=models.CASCADE)
    bktime=models.DateTimeField(null=True,blank=False)
