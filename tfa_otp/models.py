from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# @receiver(post_save, sender=User)
# def create_user_login(sender, instance, created, **kwargs):
#     if created:
#         UserLogin.objects.create(user=instance)


# class UserLogin(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userlogin')
#     two_factor_auth = models.BooleanField(default=False)






