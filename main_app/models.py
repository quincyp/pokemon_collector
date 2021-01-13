from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    
    level = models.IntegerField(default=1,  validators = [MaxValueValidator(100, message="Max level 100")])
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    