from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class task_table(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.CharField(max_length=100, null=False)
    deadline=models.DateField(null=False)