# 1- Serializer: transform normal python object to json, should create all the fields ourself

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def no_more_than_2_chars(value):
        if len(value) > 2:
            raise serializers.ValidationError('First name can not be more than 2 char')
        return value

    class PersonSerializer(serializers.serializer):
        first_name = serializers.CharField(max_length=200, validators = [no_more_than_2_chars])
        last_name = serializers.CharField(max_length=200)

        def validate_first_name(self, value):
            if len(value) > 5:
                raise serializers.ValidationError('first name can not be more than 5 char')
            return value

        def validate(self, data):
            if data.get('first_name').startswith('#') or data.get('last_name').startswith('#'):
                raise serializers.ValidationError('error')
            return data

p1 = Person(data={first_name= 'ahmed', last_name='#hamed'})
p1.is_valid() # false
p1.errors

###############################################################################################

# 2- ModelSerializer: transform model query set to json and vice versa,
# fields are generated automatically based on the model fields, crud oprations on model

class BlogModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    title = models.CharField(max_length=200)
    content = models.TextField(default='')

    def __str__(self):
        return self.title

class BlogSerializer(serializers.ModelSerializer):
    day_a_go = serializers.SerializerMethodField(method_name='get_days_ago')

    class Meta:
        model = BlogModel
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        # title = validated_data.get('title')
        # content = validated_data.get('content')
        return BlogModel.objects.create(**validated_data)

    def update(self, instance, validate_data):
        instance.title = validate_data.get('title', instance.title)
        instance.content = validate_data.get('content', instance.content)
        instance.save()
        return instance

    def get_days_ago(self, ser_obj):
        return '10 days ago'

###############################################################################################

# 3- HyperLinkedSerializer: uses hyperlinks to represent relationships, 
# rather than primary keys, include a url field instead of a primary key field

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('url', 'id', 'account_name', 'users', 'created')

#####################################################################################

# 4 - ListSerializer: serializing and validating multiple objects at once,
# won't typically need to use it directly, customize the create or update
# behavior of multiple bulk objects

class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [Book(**item) for item in validated_data]
        return Book.objects.bulk_create(books)

class BookSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = BookListSerializer


###########################################################################

# 5 - BaseSerializer: is useful if you want to implement new generic serializer classes
# similar to Serializer class, change serialization and deserialization styles,
# customize serialization or deserialization behavior (.to_representaion(), .to_internal_value()),
# adding new behavior for new serializer base classes

#BaseSerializer class that can be used to easily support alternative serialization and deserialization styles.

#This class implements the same basic API as the Serializer class:

#.data - Returns the outgoing primitive representation.
#.is_valid() - Deserializes and validates incoming data.
#.validated_data - Returns the validated incoming data.
#.errors - Returns any errors during validation.
#.save() - Persists the validated data into an object instance.
#There are four methods that can be overridden, depending on what functionality you want the serializer class to support:

#.to_representation() - Override this to support serialization, for read operations.
#.to_internal_value() - Override this to support deserialization, for write operations.
#.create() and .update() - Override either or both of these to support saving instances.

class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()

#It's simple to create a read-only serializer for converting HighScore instances into primitive data types.

class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }

#We can now use this class to serialize single HighScore instances:

@api_view(['GET'])
def high_score(request, pk):
    instance = HighScore.objects.get(pk=pk)
    serializer = HighScoreSerializer(instance)
    return Response(serializer.data)
    
#Or use it to serialize multiple instances:

@api_view(['GET'])
def all_high_scores(request):
    queryset = HighScore.objects.order_by('-score')
    serializer = HighScoreSerializer(queryset, many=True)
    return Response(serializer.data)
    


