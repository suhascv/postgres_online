from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)


class Schema(models.Model):
    image=models.ImageField(upload_to='images/')
    name=models.CharField(max_length=100)
    description=models.TextField(default='')
    overview=models.ImageField(upload_to='images/',blank=True)

    def __str__(self):
        return self.name
    


class Question(models.Model):
    statement=models.TextField(blank=True)
    schema=models.ForeignKey(Schema,on_delete=models.CASCADE)

    def __str__(self):
        return self.schema.name +' : '+ self.statement