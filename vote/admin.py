from django.contrib import admin

from .models import Candidate, User, Vote

admin.site.register(Candidate)
admin.site.register(User)
admin.site.register(Vote)