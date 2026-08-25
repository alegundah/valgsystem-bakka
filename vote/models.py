from django.db import models
from django.utils.crypto import get_random_string

class ClassName(models.Model):
    name = models.CharField(max_length=4)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=60)
    date_of_birth = models.DateField(null=True, blank=True)

    picture_happy = models.ImageField(null=True, blank=True)
    picture_neutral = models.ImageField(null=True, blank=True)
    picture_sad = models.ImageField(null=True, blank=True)

    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE) # TODO: change 
    party_code = models.CharField(max_length=5, null=True, blank=True)
    party = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)

    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.forename} {self.surname} : {self.party}"

class User(models.Model):
    code = models.CharField(
        max_length=10,
        default=get_random_string(length=10),
        primary_key=True
    )
    used = models.BooleanField(default=False)
    ClassName = models.ForeignKey(ClassName, on_delete=models.CASCADE, default=None)

    def __str__(self):
        hidden_code = "".join(self.code[0:3] + "*" * 7)
        return hidden_code