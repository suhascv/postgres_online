from django.contrib import admin
from .models import Schema,Question,UserQuestions
# Register your models here.

admin.site.register(UserQuestions)
admin.site.register(Schema)
admin.site.register(Question)
