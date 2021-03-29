from django.db import models

# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to = 'pics')
    tag = models.CharField(max_length=100)
    address = models.TextField()

class Bank(models.Model):
    name = models.CharField(max_length =100)
    branch = models.CharField(max_length = 100)
    services = models.TextField()
    address = models.TextField()

    
class AssylumHelp(models.Model):
    category = models.CharField(max_length = 100)
    link = models.TextField()

