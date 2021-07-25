from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F
from .models import UserProfile, Question, Option, User
from .serializers.user_serializers import UserSerializer
from .serializers.question_serializers import QuestionSerializer

@api_view(['GET'])
def UserList(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def QuestionList(request):
    questions = Question.objects.all()
    serializer = QuestionSerializer(questions, many=True, context={'request': request})
    return Response(serializer.data)
