from django.db import models

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
        return " ".join([self.forename, self.surname, ":", self.party])
