from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('FARMER', 'Farmer'),
        ('BUYER', 'Buyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER')

    def is_farmer(self):
        return self.role == 'FARMER'
    
    def is_buyer(self):
        return self.role == 'BUYER'
    
    def is_admin_role(self):
        return self.role == 'ADMIN' or self.is_superuser
