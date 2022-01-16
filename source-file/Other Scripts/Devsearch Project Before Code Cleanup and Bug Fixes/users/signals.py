from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance  # instance related to User (auth admin)
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
    # print('Profile Saved')
    # print('Instance:', instance)
    # print('CREATED:', created)
        
        subject = 'Welcome to DevSearch'
        message = 'We are glad you are here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # sender
            [profile.email],  # list of recipients (multiple emails)
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance  # instance related to Profile (setiap perubahan pada Profile, maka akan merubah User pada auth admin juga)
    user = profile.user

    # if created == False:
    if created is False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteProfile(sender, instance, **kwargs):
    user = instance.user  # instance.user related to Profile.user
    print(instance)
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteProfile, sender=Profile)


'''
# post_delete user in User
def userDelete(sender, instance, **kwargs):
    user = instance
    print(user)
    deleteUser = User.objects.all()
    print(deleteUser)


post_delete.connect(userDelete, sender=User)
'''
