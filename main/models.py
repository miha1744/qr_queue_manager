from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Doctor(models.Model):
    # relationships
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # basic information
    name = models.CharField(max_length=50, help_text="Name of a doctor")

    profession = models.CharField(max_length=50, help_text="Profession of a doctor")

    image = models.ImageField(default= "NoneImage.jpg",null=True, blank=True)

    def __str__(self):
        return f"{self.pk}. {self.name}"

class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50, help_text="Name of a user")

    def __str__(self):
        return f"{self.name}"
