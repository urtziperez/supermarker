from django.db import models
from couchdbkit.ext.django.schema import *
# Create your models here.

class User(Document):
    name = StringProperty()
    password = StringProperty()