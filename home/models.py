from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title= models.CharField(max_length=100)
    description=models.TextField()
    date_posted=models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')

    def __str__(self):
        return self.title
        