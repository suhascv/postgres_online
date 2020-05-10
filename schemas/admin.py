from django.contrib import admin
from .models import Schema,Question,Customer
# Register your models here.

admin.site.register(Customer)
admin.site.register(Schema)
admin.site.register(Question)
