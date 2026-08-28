from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings 
from django.db import models
from django.utils.crypto import get_random_string

class VoteManager(models.Model):
    started = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)

class Candidate(models.Model):
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=60)
    picture = models.CharField(null=True, blank=True)
    class_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    party_code = models.CharField(max_length=5, null=True, blank=True)
    party = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.forename} {self.surname} : {self.party}"
    

class User(AbstractUser):
    class_name = models.ForeignKey(
        Group, 
        null=True,
        on_delete=models.CASCADE, 
        related_name="users"
    )

class Vote(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="vote"
    )
    global_vote = models.ForeignKey(
        Candidate, 
        on_delete=models.CASCADE, 
        related_name="global_vote",
        null=True
    )
    class_vote = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE, 
        related_name="class_vote",
        null=True
    )

    def used(self):
        return self.global_vote and self.class_vote

def delete_users():
    User.objects.filter(is_superuser=False).delete()

def create_user(class_name):
    u = User.objects.create(username=get_random_string(length=10), class_name=class_name)
    v = Vote.objects.create(user=u)