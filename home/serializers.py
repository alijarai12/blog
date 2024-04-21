from rest_framework import serializers
from .models import BlogPost, BlogComment

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= BlogPost
        fields= '__all__'

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= BlogComment
        fields= '__all__'
