from django.shortcuts import render,get_object_or_404,redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Schema,Question,UserQuestions
from rest_framework import routers,serializers,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from .serializers import SchemaSerializer,UserSerializer,\
SchemaOverviewSerializer,QuestionSerializer,UserQuestionsSerializer,LoginSerializer
from rest_framework import serializers
from knox.models import AuthToken



def tokenAuthentication(user,token):
    try:
        AuthToken.objects.get(digest=token,user=user)
        return True
    except:
        return False



@api_view(['GET','POST'])
def schema_api_view(request):
    schemas=Schema.objects.all()
    serializer=SchemaSerializer(schemas,many=True)
    context={'schemas':serializer.data}
    if(request.method=='POST'):
        print(request.data)
        if tokenAuthentication(request.data['user'],request.data['token']):
            context['user']=request.data['user']
    return Response(context)


@api_view(['GET'])
def schema_overview_api_view(request,schema_id):
    schema=get_object_or_404(Schema,pk=schema_id)
    serializer=SchemaOverviewSerializer(schema)
    context={'schema':serializer.data}
    questions=Question.objects.filter(schema=schema_id)
    context['questions']=QuestionSerializer(questions,many=True).data
    return Response(context)


@api_view(['POST'])
def query_api_view(request,question_id):
    request_token=request.data["token"]
    request_pk=int(request.data["userpk"])
    context={'status':False}
    try:
        token=AuthToken.objects.get(digest=request_token)
        if token.user.pk==request_pk:
            context['status']=True
    except:
        context['status']=False
    
    if context['status']:
        question=get_object_or_404(Question,pk=question_id)
        schema_id=question.schema.pk
        schema=Schema.objects.get(pk=schema_id)
        schema_serializer=SchemaOverviewSerializer(schema)
        question_serializer=QuestionSerializer(question)
        user_question=UserQuestions.objects.get(user=request_pk,question=question_id)
        user_question_serializer=UserQuestionsSerializer(user_question)
        context['schema']=schema_serializer.data
        context['question']=question_serializer.data
        context['user_question']=user_question_serializer.data

    return Response(context)
    

@api_view(['POST'])
def login_api_view(request):
    
    username,password=request.data['username'],request.data['password']
    print(username,password)
    user=authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return Response({'status':'valid',
        'user':UserSerializer(user).data,
        "token":AuthToken.objects.create(user)[1]
        })
    else:
        return Response({'status':'invalid credentials'})


@api_view(['POST'])
def signup_api_view(request):
    username,password=request.data['username'],request.data['password']
    email=request.data['email']
    try:
            User.objects.get(username=username)
            return Response({'error':'user already exists TRY AGAIN'})
    except:
            try:
                User.objects.get(email=email)
                return Response({'error':'email already exists or invalid email TRY AGAIN'})
            except:
                user=User.objects.create_user(username,password=password,email=email)
                user.save()
                login(request,user)
                return Response({'status':'valid',
        'user':UserSerializer(user).data,
        "token":AuthToken.objects.create(user)[1]
        })