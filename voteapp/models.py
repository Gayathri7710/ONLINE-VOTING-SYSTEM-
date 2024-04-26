from pyexpat import model
from statistics import mode
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.contrib.auth.models import User


class ElectionType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ElectionArea(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.code


STATUS = ((1, "Voted"), (2, "Not Voted"))
ADMINSTATUS = ((1, "Verified"), (2, "Not Verified"))
class Voter(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    adharno = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    adharimage = models.FileField(null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=2)
    voteemailstatus = models.IntegerField(choices=ADMINSTATUS, default=2)
    emailstatus = models.IntegerField(choices=ADMINSTATUS, default=2)
    electionarea = models.ForeignKey(ElectionArea, on_delete=models.CASCADE, null=True, blank=True)
    adminstatus = models.IntegerField(choices=ADMINSTATUS, null=True, blank=True, default=1)

    def __str__(self) -> str:
        return self.user.username


class Candidate(models.Model):
    fname = models.CharField(max_length=100, null=True, blank=True)
    lname = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    partyname = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zipcode = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    logo = models.FileField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    electionarea = models.ForeignKey(ElectionArea, on_delete=models.CASCADE, null=True, blank=True)
    electiontype = models.ForeignKey(ElectionType, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return self.fname + " " + self.lname


class Homepage(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    logo = models.FileField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title



class Voting(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    winner = models.BooleanField(null=True, blank=True, default=False)
    count = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.candidate.fname + " " + self.count


VOTESTATUS = ((1, "Start"), (2, "Not Start"), (3, "Winner Announced"))
class VotingStatus(models.Model):
    status = models.IntegerField(choices=VOTESTATUS, null=True, blank=True, default=2)
    electiontype = models.ForeignKey(ElectionType, on_delete=models.CASCADE, null=True, blank=True)
    electionarea = models.ForeignKey(ElectionArea, on_delete=models.CASCADE, null=True, blank=True)


class VotingHistory(models.Model):
    winner = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    electionarea = models.ForeignKey(ElectionArea, on_delete=models.CASCADE, null=True, blank=True)
    electiontype = models.ForeignKey(ElectionType, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    winby = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.winner.fname + " " + self.winby