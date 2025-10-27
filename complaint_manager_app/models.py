from django.db import models
from django.contrib.auth.models import User
    
# Create your models here.
class Complaint(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('in_progress','In progress'),
        ('resolved','Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status= models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 


    def __str__(self):
        return self.name