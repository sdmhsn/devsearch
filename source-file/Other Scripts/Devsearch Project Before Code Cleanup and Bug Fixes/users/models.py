from django.db import models
from django.contrib.auth.models import User  # related to User in admin
import uuid
from django.db.models.deletion import CASCADE
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver  # decorator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)


class Skill(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)  # models.SET_NULL: So if I send a message to someone and ideally my account, I want the recipient to still see that message. I don't want that to go away. They should have a record of it
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')  # related_name='messages': And we need to do something a little bit different for the recipient, because in this case, the recipient connection to the profile is going to interfere with our sender.  So when we go to the profile. To access the profiles messages instead of doing something like profile message, Underscore said, we're just going to be able to type in messages. So this is how that profile model is going to connect to this. So we need to add this to one of these, at least, because if we don't, then it will not allow us to have a connection to the profile model twice so we won't know how to actually connect to it. So we need to add in a related name.
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta: 
        ordering = ['is_read', '-created']  # message sorted in inbox and django admin by is_read and created (minus)

'''
# @receiver(post_save, sender=Profile)
def createProfile(sender, instance, created, **kwargs):
    print('Profile Saved')
    print('Instance:', instance)
    print('CREATED:', created)  # true when we created new data (profile)


# @receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    print('Deleting User...')


post_save.connect(createProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
'''
