from django.contrib import admin
from .models import *


models = [UserProfile,Task,Category]
# Register your models here.
admin.site.register(models)