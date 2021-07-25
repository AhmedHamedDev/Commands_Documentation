from django.contrib.auth import models
from .models import Blog
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        #fields = '__all__'


class BlogSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True, many=False)
    author_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Blog
        fields = ['title', 'content', 'slug', 'date', 'author_id', 'author']