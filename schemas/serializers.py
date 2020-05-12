from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Schema,Question,UserQuestions

class SchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Schema
        fields=['pk','name','image']
        

class SchemaOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Schema
        fields=['name','image','description','overview']



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=['pk','statement']

class UserQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserQuestions
        fields=['user','question','status','latest']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']

