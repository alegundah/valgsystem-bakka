from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings 
from django.db import models

class Candidate(models.Model):
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=60)
    picture = models.ImageField(null=True, blank=True)
    class_name = models.ForeignKey(Group, on_delete=models.CASCADE)
    party_code = models.CharField(max_length=5, null=True, blank=True)
    party = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.forename} {self.surname} : {self.party}"
    

class User(AbstractUser):
    school_class = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="school_class"
    )

class Vote(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    global_vote = models.ForeignKey(
        Candidate, 
        on_delete=models.PROTECT, 
        related_name="global_vote"
    )
    class_vote = models.ForeignKey(
        Candidate, 
        on_delete=models.PROTECT, 
        related_name="class_vote"
    )