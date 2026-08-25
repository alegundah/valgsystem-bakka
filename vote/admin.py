from django.contrib import admin

from .models import Candidate, User

admin.site.register(Candidate)
admin.site.register(User)