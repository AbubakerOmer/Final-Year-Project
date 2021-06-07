
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from chat.models import Message


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',blank=True)
    # email = models.EmailField(max_length=40,blank=True)
    mobile = models.CharField(max_length=20,blank=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name +self.user.email
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to = 'pics', blank=True)
    description=models.CharField(max_length=100,blank=True)

    tag = models.CharField(max_length=100)
    address = models.TextField()
    def __str__(self):
        return self.name

class Bank(models.Model):
    name = models.CharField(max_length =100)
    branch = models.CharField(max_length = 100)
    services = models.TextField()
    address = models.TextField()
    def __str__(self):
        return self.name

class Assylum(models.Model):
    org_type=models.CharField(max_length=100,blank=True)
    org_name=models.CharField(max_length=200,blank=True)
    category = models.CharField(max_length=100,blank=True)
    email=models.EmailField(max_length=80,blank=True)
    phone= models.PositiveIntegerField(blank=True)
    working_day=models.CharField(max_length=900,blank=True)
    website=models.URLField(blank=True)
    address = models.TextField(blank=True)
class Refuse(models.Model):
    org_name=models.CharField(max_length=200,blank=True)
    email=models.EmailField(max_length=80,blank=True)
    phone= models.PositiveIntegerField(blank=True)
    working_day=models.CharField(max_length=900,blank=True)
    website=models.URLField(blank=True)
    address = models.TextField(blank=True)
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
class WelcomeNotes(models.Model):
    title =models.CharField(max_length=100)
    note=  models.CharField(max_length=300)
    def __str__(self):
        return self.name
class Gp(models.Model):
    name = models.CharField(max_length =100)
    address = models.TextField()
    phone= models.PositiveIntegerField()
    def __str__(self):
        return self.name





CATEGEORY_CHOICES  = (
    ("Emergency_Support", "Emergency_Support"),
    ("Fix_Meeting", "Fix_Meeting"),
    ("Others", "Others"),
    ("Direct_Meeting", "Direct_Meeting"),
)
STATUS_CHOICES = (

    ("PENDING", "PENDING"),
    ("APPROVED", "APPROVED"),
    ("REJECTED", "REJECTED"),)


class Query(models.Model):
    sno = models.AutoField(primary_key=True,blank=True)
    currenstatus = models.BooleanField(default=True)
    category_type = models.CharField(max_length=50,choices=CATEGEORY_CHOICES,default='PENDING',blank=True)
    details = models.TextField(default=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default="PENDING",max_length=50)
    assign = models.CharField(max_length=50)



    def __str__(self):
        return self.details



class Querystatus(models.Model):
    is_approved = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES,max_length=30,  default="PENDING")
    query_status = models.ForeignKey(Query,on_delete=models.CASCADE)


    def __str__(self):
        return self.status


class Save_value(models.Model):
     consellor = models.CharField(max_length=35)



class Messages_Assigned(models.Model):
    Id=models.AutoField(primary_key=True)
    Message_Id=models.ForeignKey(Message,on_delete=models.CASCADE)
    Assigned=models.BooleanField()
    Assigned_To=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Assigned_To")
    Assigned_By=models.ForeignKey(User,on_delete=models.CASCADE,related_name="Assigned_By")
    Assigned_Date=models.DateTimeField(auto_now=True)
