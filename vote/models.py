from django.db import models


class ClassName(models.Model):
    name = models.CharField(max_length=4)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    forename = models.CharField(max_length=20)
    surname = models.CharField(max_length=60, null=True)
    date_of_birth = models.DateField(null=True)

    picture_happy = models.ImageField()
    picture_happy = models.ImageField()
    picture_sad = models.ImageField()

    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE) # TODO: change 
    party_code = models.CharField(max_length=5, null=True)
    party = models.CharField(max_length=40)
    description = models.TextField(null=True)
