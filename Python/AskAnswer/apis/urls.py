from django.urls import path
from .views import UserList, QuestionList

urlpatterns = [
    path('user-list/', UserList, name='user-list'),
    path('question-list/', QuestionList, name='question-list')
]