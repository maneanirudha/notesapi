from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    note = models.CharField(max_length=50,blank=False,default='')
    notedesc = models.CharField(max_length=5000,blank=False,default='')


    def __str__(self):
        return self.note

    class Meta:
        ordering = ('id',)

class Useractivation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    otp = models.CharField(max_length=4,blank=False,default='')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.otp

    class Meta:
        ordering = ('id',)

class Subscriptionplans(models.Model):
    plan_name = models.CharField(max_length=25,blank=False)
    plan_validity = models.IntegerField(blank=False)
    note_limit = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.plan_name

    class Meta:
        ordering = ('id',)

class User_subscription_details(models.Model):
    sub = models.ForeignKey(Subscriptionplans,on_delete=models.CASCADE,blank=False,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    subcription_date = models.DateField(blank=False)

    # def __str__(self):
    #     return self.sub

    class Meta:
        ordering = ('id',)

    