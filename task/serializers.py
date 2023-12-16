from rest_framework import serializers
from .models import User,task_table
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta:
        model=User
        fields=['id','first_name','last_name','username','password']
        
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=task_table
        fields=['username','id','task','deadline']