from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
import datetime
from django.contrib.auth.models import UserManager as DefaultUserManager, User
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from django.db.models.signals import post_save
from django.dispatch import receiver


# class newUser(AbstractBaseUser):
#     name = models.CharField(max_length=50, verbose_name="이름", default = "user27")
#     password = models.CharField(max_length=50, default='123')
#     score = models.IntegerField(default=0)
#     USERNAME_FIELD = 'name'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class UserManager(DefaultUserManager):
    def get_or_create_google_user(self, user_pk, extra_data):
        user = newUser.objects.get(pk=user_pk)
        user.username = extra_data['name']
        user.save()
        return user


class Game(models.Model):
    creator = models.ForeignKey(User, related_name="Host", on_delete=models.DO_NOTHING) # 방
    opponent = models.ForeignKey(User, related_name="Participant", null=True, blank=True, on_delete=models.DO_NOTHING)#참가자
    winner = models.ForeignKey(User, related_name='Win', null=True, blank=True, on_delete=models.DO_NOTHING) # 우승자
    loser = models.ForeignKey(User, related_name="Lose", null=True, blank=True, on_delete=models.DO_NOTHING)
    current_turn = models.ForeignKey(User, related_name='Turn', on_delete=models.DO_NOTHING) # 현재

    creator_card = models.IntegerField(verbose_name = "creator_card", null=True, blank=True)
    opponent_card = models.IntegerField(verbose_name="opponent_card", null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True) # 방 생성
    draw = models.BooleanField(default=False)
    greater = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)
