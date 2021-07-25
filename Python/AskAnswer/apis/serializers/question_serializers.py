from rest_framework.utils.serializer_helpers import ReturnDict
from ..models import Question, UserProfile, User, Option, OptionType
from rest_framework import serializers

class DictSerializer(serializers.ListSerializer):

    dict_key = 'id'

    @property
    def data(self):
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class OptionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionType
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):

  class Meta:
        model = Option
        fields = '__all__'

# class QuestionSerializer(serializers.ModelSerializer):
#     author = serializers.SerializerMethodField()
#     optionOne = serializers.SerializerMethodField()
#     optionTwo = serializers.SerializerMethodField()
    
#     def get_author(self, question):
#         return question.author.username

#     def get_optionOne(self, question):
#         option = question.question_options.get(optionType__id = 1)
#         return {'text': option.text, 'votes': [v['username'] for v in option.voters.values()]}

#     def get_optionTwo(self, question):
#         option = question.question_options.get(optionType__id = 2)
#         return {'text': option.text, 'votes': [v['username'] for v in option.voters.values()]}


#     class Meta:
#         model = Question
#         fields = ['id', 'timestamp', 'author', 'optionOne', 'optionTwo']
#         depth = 2
#         list_serializer_class = DictSerializer


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    optionOne = serializers.SerializerMethodField()
    
    def get_author(self, question):
        return question.author.username

    def get_optionOne(self, question):
        option = question.question_options.values()
        return option

    class Meta:
        model = Question
        fields = ['id', 'timestamp', 'author', 'question_options', 'optionOne']
        depth = 2
        list_serializer_class = DictSerializer





