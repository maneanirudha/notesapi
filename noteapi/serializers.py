from rest_framework import serializers
from noteapi.models import Notes


class NotesSerializer(serializers.ModelSerializer):

     class Meta:
        model = Notes
        fields = ('id','note','notedesc')