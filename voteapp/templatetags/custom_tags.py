from itertools import product
from django import template
from voteapp.models import *
import datetime
register = template.Library()

@register.filter(name="checkvoting")
def checkvoting(pid=None):
    earea = ElectionArea.objects.filter().first()
    vote = VotingStatus.objects.filter(electionarea__id=earea.id)
    print("My vote=", vote)
    if pid:
        vote.filter(electionarea__id=pid)
    if vote.first().status == 1:
        return True
    else:
        return False

@register.filter(name="checkstatus")
def checkstatus(pid=None):
    earea = ElectionArea.objects.filter().first()
    vote = VotingStatus.objects.filter(electionarea__id=earea.id)
    if pid:
        vote.filter(electionarea__id=pid)
    if vote.first().status == 3:
        return True
    else:
        return False
        
@register.filter(name="checkvarifyemail")
def checkvarifyemail(pid):
    vote = Voter.objects.get(user=pid)
    if vote.voteemailstatus == 2:
        return True
    else:
        return False

@register.filter(name="changestr")
def changestr(pid):
    return str(pid)