from rest_framework import serializers
from noteapi.models import Notes,Useractivation,User_subscription_details
from django.contrib.auth.models import User


class NotesSerializer(serializers.ModelSerializer):

     class Meta:
        model = Notes
        fields = ('id','note','notedesc')

class UserSerializer(serializers.ModelSerializer):

   class Meta:
      model = User
      fields = ('username','email','password')
      extra_kwargs = {'password': {'write_only': True}}

class UserValidation(serializers.ModelSerializer):

   class Meta:
      model = Useractivation
      fields = ('__all__')

class VerifyUser(serializers.ModelSerializer):
   class Meta:
      model = Useractivation,User
      fields = ('email','otp')

class Subscription_details(serializers.ModelSerializer):
   class Meta:
      model = User_subscription_details
      fields = ('subcription_date','sub','user_id')
