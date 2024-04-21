from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class BlogPost(BaseModel):
    title= models.CharField(max_length=100)
    description=models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')


class BlogComment(BaseModel):
    comment = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

