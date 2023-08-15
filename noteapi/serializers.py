from rest_framework import serializers
from noteapi.models import Notes
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