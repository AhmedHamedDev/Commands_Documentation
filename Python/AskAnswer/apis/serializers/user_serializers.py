from django.contrib.auth import models
from ..models import Question, UserProfile, User, Option, OptionType
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    avatarURL = serializers.SerializerMethodField()

    def get_avatarURL(self, user):
        profile = UserProfile.objects.get(user=user)
        return profile.avatarURL

    def get_questions(self, user):
        questions = Question.objects.filter(author=user)
        lis_of_obj = QuestionSerializer(questions,many=True,context={'request': self.context['request']}).data
        return [d['id'] for d in lis_of_obj]

    def get_answers(self, user):
        answers = Option.objects.filter(voters__id__exact=user.id)
        lis_of_obj = OptionSerializer(answers,many=True,context={'request': self.context['request']}).data
        data = dict()
        for obj in lis_of_obj:
            data[obj['question_id']] = obj['name']
        return data

    class Meta:
        model = User
        fields = ['id','username', 'avatarURL', 'questions','answers']


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['avatarURL', 'user_id', 'user']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id']


class OptionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionType
        fields = ['name']


class OptionSerializer(serializers.ModelSerializer):
  name = serializers.SerializerMethodField()

  def get_name(self, option):
        optionType = OptionType.objects.get(id=option.optionType.id)
        return optionType.name

  class Meta:
        model = Option
        fields = ['name','question_id']