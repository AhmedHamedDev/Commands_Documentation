from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import  get_object_or_404
from rest_framework import serializers

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer
from .models import Blog

@api_view(['GET'])
def blogList(request):
    blogs = Blog.objects.select_related('author').all()
    serializer = BlogSerializer(blogs, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def blogDetail(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    serializer = BlogSerializer(blog_obj, many=False, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
def blogCreate(request):
    serializer = BlogSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

@api_view(['POST'])
def blogUpdate(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    serializer = BlogSerializer(instance=blog_obj, data=request.data)

    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

@api_view(['DELETE'])
def blogDelete(request, slug):
    blog_obj = get_object_or_404(Blog, slug=slug)
    blog_obj.delete()
    
    return Response("deleted successfully")
