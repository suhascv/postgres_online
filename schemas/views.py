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

# Create your views here.

#all api views


#displaying all normal views
def schemaView(request):
    schemas=Schema.objects.all()
    context={'schemas':schemas}
    user = request.user
    if user is not None:
        context['user']=user.username
    else:
        context['user']=False
    print(context['user'])
    return render(request,'schemas/schema.html',context)
    

#displaying a overview and questions of the selected schema
def schemaOverview(request,schema_id):
    schema=get_object_or_404(Schema,pk=schema_id)
    context={'schema':schema}
    questions=Question.objects.filter(schema=schema_id)
    context['questions']=questions
    return render(request,'schemas/overview.html',context)

#displaying a selected question
def query(request,question_id):
    if request.user.is_authenticated:
        question=get_object_or_404(Question,pk=question_id)
        schema_id=question.schema.pk
        schema=Schema.objects.get(pk=schema_id)
        context={'schema':schema,'question':question}
        return render(request,'schemas/query.html',context)
    else:
        return redirect('signup')

#displaying a signup form
def signUp(request):
    if request.method=='POST':
        username, password = request.POST.get('username',''),request.POST.get('password','')
        email = request.POST.get('email','')
        try:
            User.objects.get(username=username)
            return render(request,'registration/signup.html',{'error':'user already exists TRY AGAIN'})
        except:
            try:
                User.objects.get(email=email)
                return render(request,'registration/signup.html',{'error':'email already exists or invalid email TRY AGAIN'})
            except:
                user=User.objects.create_user(username,password=password,email=email)
                user.save()
                login(request,user)
                insertQuestion(user)
                return redirect('schemas')        
    else:
        return render(request,'registration/signup.html',{})
        

#displaying login form
def signIn(request):
    username, password = request.POST.get('username',''),request.POST.get('password','')
    user = authenticate(username=username, password=password)    
    if user is not None:
        login(request,user)
        return redirect('schemas')
    else:
        return render(request,'registration/login.html',{})
    

def logout_view(request):
    logout(request)
    return redirect('schemas')



#once the user is registered all the questions will have default status of 'not attempted'
def insertQuestion(user):
    questions=Question.objects.all()
    for question in questions:
        userquestion=UserQuestions(user=user,question=question)
        userquestion.save()


def account(request):
    user=request.user.username
    schemas=Schema.objects.all()
    return render(request,'schemas/account.html',{'schemas':schemas,'user':user})

def status(request,schema_id):
    user=request.user
    questions=Question.objects.filter(schema=schema_id)
    data=[]
    for q in questions:
        data.append(UserQuestions.objects.get(user=user,question=q))
    schema=Schema.objects.get(pk=schema_id).name
    return render(request,'schemas/status.html',{'questions':data,'user':user.username,'schema':schema})
