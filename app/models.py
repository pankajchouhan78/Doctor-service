from django.db import models

# Create your models here.
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
class Docutor(models.Model):
    name = models.CharField(max_length=250)
    photo = models.ImageField(upload_to= "UploadDocutor/")
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=12)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=50)
    degree =  models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    specialzation = models.CharField(max_length=100)
    appoiment = models.DateField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    docutor = models.ForeignKey(Docutor, on_delete=models.CASCADE, blank=True, null=True)
    Name = models.CharField(max_length=250)
    password = models.CharField(max_length=100, blank=True)
    Photo = models.ImageField(upload_to= "UploadPatient/")
    phone = models.CharField(max_length=12)
    gender = models.CharField(choices=GENDER_CHOICES,  max_length=50)
    age = models.IntegerField()
    disease = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name



