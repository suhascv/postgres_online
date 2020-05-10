from django.shortcuts import render,get_object_or_404,redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Schema,Question,Customer

# Create your views here.

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

def schemaOverview(request,schema_id):
    schema=get_object_or_404(Schema,pk=schema_id)
    context={'schema':schema}
    questions=Question.objects.filter(schema=schema_id)
    context['questions']=questions
    return render(request,'schemas/overview.html',context)

def query(request,question_id):
    if request.user.is_authenticated:
        question=get_object_or_404(Question,pk=question_id)
        schema_id=question.schema.pk
        schema=Schema.objects.get(pk=schema_id)
        context={'schema':schema,'question':question}
        return render(request,'schemas/query.html',context)
    else:
        return redirect('signup')

def signUp(request):
    if request.method=='POST':
        username, password = request.POST.get('username',''),request.POST.get('password','')
        email = request.POST.get('email','')
        try:
            User.objects.get(username=username)
            return render(request,'schemas/signup.html',{'error':'user already exists TRY AGAIN'})
        except:
            try:
                User.objects.get(email=email)
                return render(request,'schemas/signup.html',{'error':'email already exists or invalid email TRY AGAIN'})
            except:
                user=User.objects.create_user(username,password=password,email=email)
                user.save()
                login(request,user)
                return redirect('schemas')        
    else:
        return render(request,'schemas/signup.html',{})
        

def signIn(request):
    username, password = request.POST.get('username',''),request.POST.get('password','')
    user = authenticate(username=username, password=password)    
    if user is not None:
        login(request,user)
        return redirect('schemas')
    else:
        return render(request,'schemas/login.html',{})
    

def logout_view(request):
    logout(request)
    return redirect('schemas')