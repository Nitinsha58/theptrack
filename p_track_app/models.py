
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, null=True)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    sent_email = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Note_category(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.category}'

class Note(models.Model):
    category = models.ForeignKey(Note_category, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'Note title is: {self.title}'