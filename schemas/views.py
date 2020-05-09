from django.shortcuts import render,get_object_or_404
from .models import Schema,Question
# Create your views here.

def schemaView(request):
    schemas=Schema.objects.all()
    context={'schemas':schemas}
    return render(request,'schemas/schema.html',context)

def schemaOverview(request,schema_id):
    schema=get_object_or_404(Schema,pk=schema_id)
    context={'schema':schema}
    questions=Question.objects.filter(schema=schema_id)
    context['questions']=questions
    return render(request,'schemas/overview.html',context)

def query(request,question_id):
    print('here')
    question=get_object_or_404(Question,pk=question_id)
    schema_id=question.schema.pk
    schema=Schema.objects.get(pk=schema_id)
    context={'schema':schema,'question':question}
    return render(request,'schemas/query.html',context)

