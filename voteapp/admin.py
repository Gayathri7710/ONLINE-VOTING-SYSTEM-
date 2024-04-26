from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Voter)
admin.site.register(Candidate)
admin.site.register(Homepage)
admin.site.register(Voting)
admin.site.register(ElectionArea)
admin.site.register(ElectionType)
admin.site.register(VotingStatus)
