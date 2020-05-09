from django.shortcuts import render
from .models import Schema
# Create your views here.

def schemaView(request):
    schemas=Schema.objects.all()
    context={'schemas':schemas}
    return render(request,'schemas/schema.html',context)

    