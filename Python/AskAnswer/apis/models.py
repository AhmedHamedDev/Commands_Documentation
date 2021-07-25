from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    avatarURL = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 

################################################################################

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_questions')
    timestamp = models.DateTimeField(auto_now_add=True)

################################################################################

class OptionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

################################################################################

class Option(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_options')
    optionType = models.ForeignKey(OptionType, on_delete=models.CASCADE, related_name='type_options')
    voters = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.text