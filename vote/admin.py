from django.contrib import admin

from .models import ClassName, Candidate, User

admin.site.register(ClassName)
admin.site.register(Candidate)
admin.site.register(User)