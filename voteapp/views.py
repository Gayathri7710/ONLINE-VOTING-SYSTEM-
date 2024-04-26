import itertools
import math
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from voteapp.send_email import sendmail
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
from django.db.models import Q
from django.http import HttpResponseRedirect
@login_required(login_url='/')
def home(request):
    voters = Voter.objects.all().count()
    candidate = Candidate.objects.all().count()
    electionarea = ElectionArea.objects.all().count()
    electiontype = ElectionType.objects.all().count()
    return render(request, "home.html", locals())

def user_home(request):
    if request.user.is_authenticated and not request.user.is_staff:
        user = Voter.objects.get(user=request.user)
        if user.emailstatus == 2:
            return redirect('view_profile')
    elif request.user.is_staff:
        return redirect('home')
    return render(request, "main.html")

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_voter(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password are not empty
        if not username or not password:
            messages.error(request, "Username and password fields should not be empty.")
            return redirect('login_voter')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('user_home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login_voter')

    return render(request, 'login.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in Successfully")
            return redirect('home')
        else:
            messages.success(request, "Invalid user")
            return redirect('admin_login')

    return render(request, 'admin_login.html')

@login_required(login_url='/')
def voting_status(request):
    areacode = request.GET.get('areacode')
    electtype = request.GET.get('electtype')
    earea = ElectionArea.objects.filter().first()
    etype = ElectionType.objects.filter().first()
    graphdata = []
    voting = Voting.objects.filter(candidate__electionarea__id=earea.id,candidate__electiontype__id=etype.id)
    data = Voter.objects.filter(status=2, electionarea__id=earea.id)
    status = VotingStatus.objects.get(electionarea__id=earea.id, electiontype__id=etype.id)
    winner = Voting.objects.filter(winner=True, candidate__electionarea__id=earea.id, candidate__electiontype__id=etype.id).first()
    if areacode and electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=electtype)
        data = Voter.objects.filter(electionarea__id=areacode)
        winner = Voting.objects.filter(winner=True, candidate__electionarea__id=areacode, candidate__electiontype__id=electtype).first()
        status = VotingStatus.objects.get(electionarea__id=areacode,  electiontype__id=electtype)
    elif areacode:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=etype.id)
        data = Voter.objects.filter(electionarea__id=areacode)
        winner = Voting.objects.filter(winner=True, candidate__electionarea__id=areacode, candidate__electiontype__id=etype.id).first()
        status = VotingStatus.objects.get(electionarea__id=areacode,  electiontype__id=etype.id)
    elif electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=earea.id, candidate__electiontype__id=electtype)
        data = Voter.objects.filter(electionarea__id=earea.id)
        winner = Voting.objects.filter(winner=True, candidate__electionarea__id=earea.id, candidate__electiontype__id=electtype).first()
        status = VotingStatus.objects.get(electionarea__id=earea.id,  electiontype__id=electtype)
    for i in voting:
        print(i.candidate.fname, i.count)
        graphdata.append({'label':i.candidate.fname, 'y':int(i.count)})
    areadata = ElectionArea.objects.all()
    typedata = ElectionType.objects.all()
    return render(request, "voting_status.html", locals())

@login_required(login_url='/')
def candidate_reports(request):
    candidate = Candidate.objects.all()
    return render(request, "candidate_report.html", locals())

@login_required(login_url='/')
def voter_reports(request):
    data = Voter.objects.all()
    return render(request, "voter_reports.html", locals())

@login_required(login_url='/')
def new_candidate(request):
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        d = request.POST['dob']
        c = request.POST['city']
        s = request.POST['state']
        z = request.POST['zipcode']
        a = request.POST['address']
        pn = request.POST['pname']
        pl = request.FILES.get('plogo')
        im = request.FILES.get('image')
        er = request.POST['earea']
        et = request.POST['etype']

        eareaobj = ElectionArea.objects.get(id=er)
        etypeobj = ElectionType.objects.get(id=et)
        candidate = Candidate.objects.create(electiontype=etypeobj, electionarea=eareaobj,  fname=f, lname=l, email=e, dob=d, city=c, state=s, zipcode=z, address=a, partyname=pn, logo=pl, image=im)
        voting = Voting.objects.create(candidate=candidate, count=0)
        messages.success(request, "Candidate added successfully")
        return redirect('candidate_reports')
    earea = ElectionArea.objects.all()
    etype = ElectionType.objects.all()
    return render(request, "new_candidate.html", locals())

@login_required(login_url='/')
def edit_candidate(request, pid):
    data = Candidate.objects.get(id=pid)
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        d = request.POST['dob']
        c = request.POST['city']
        s = request.POST['state']
        z = request.POST['zipcode']
        a = request.POST['address']
        pn = request.POST['pname']
        er = request.POST['earea']
        et = request.POST['etype']

        try:
            pl = request.FILES['plogo']
            data.logo = pl
            data.save()
        except:
            pass

        try:
            im = request.FILES['image']
            data.image = im
            data.save()
        except:
            pass
        eareaobj = ElectionArea.objects.get(id=er)
        etypeobj = ElectionType.objects.get(id=et)
        candidate = Candidate.objects.filter(id=pid).update(electiontype=et, electionarea=er, fname=f, lname=l, email=e, dob=d, city=c, state=s, zipcode=z, address=a, partyname=pn)
        messages.success(request, "Candidate updated successfully")
        return redirect('candidate_reports')
    earea = ElectionArea.objects.all()
    etype = ElectionType.objects.all()
    return render(request, "edit_candidate.html", locals())

@login_required(login_url='/')
def delete_candidate(request, pid):
    data = Candidate.objects.get(id=pid)
    data.delete()
    messages.success(request, "Candidate deleted successfully")
    return redirect('candidate_reports')

@login_required(login_url='/')
def new_electiontype(request):
    if request.method == "POST":
        n = request.POST['fname']
        desc = request.POST['desc']

        etypeobj = ElectionType.objects.create(name=n, description=desc)
        messages.success(request, "Election type added successfully")
        return redirect('electiontype_reports')
    return render(request, "add_electiontype.html", locals())

@login_required(login_url='/')
def edit_electiontype(request, pid):
    data = ElectionType.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['fname']
        desc = request.POST['desc']

        etypeobj = ElectionType.objects.filter(id=pid).update(name=n, description=desc)
        messages.success(request, "Election type updated successfully")
        return redirect('electiontype_reports')
    return render(request, "edit_electiontype.html", locals())

@login_required(login_url='/')
def delete_electiontype(request, pid):
    data = ElectionType.objects.get(id=pid)
    data.delete()
    messages.success(request, "Election type deleted successfully")
    return redirect('electiontype_reports')

@login_required(login_url='/')
def electiontype_reports(request):
    etype = ElectionType.objects.all()
    return render(request, "electiontype_reports.html", locals())

def combination_votingstatus():
    electarea = ElectionArea.objects.all()
    electtype = ElectionType.objects.all()
    list1 = [i for i in electarea]
    list2 = [i for i in electtype]
    list = [list1, list2]
    combination = [p for p in itertools.product(*list)]
    for i in combination:
        voting_status = VotingStatus.objects.get_or_create(electionarea=i[0], electiontype=i[1])

@login_required(login_url='/')
def new_electionarea(request):
    if request.method == "POST":
        n = request.POST['fname']
        t = request.POST['title']
        desc = request.POST['desc']
        etypeobj = ElectionArea.objects.create(code=n, description=desc, title=t)
        makecombination = combination_votingstatus()
        messages.success(request, "Election area added successfully")
        return redirect('electionarea_reports')
    return render(request, "new_electionarea.html", locals())

@login_required(login_url='/')
def edit_electionarea(request, pid):
    data = ElectionArea.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['fname']
        t = request.POST['title']
        desc = request.POST['desc']

        etypeobj = ElectionArea.objects.filter(id=pid).update(code=n, description=desc, title=t)
        makecombination = combination_votingstatus()
        messages.success(request, "Election area updated successfully")
        return redirect('electionarea_reports')
    return render(request, "edit_electionarea.html", locals())

@login_required(login_url='/')
def delete_electionarea(request, pid):
    data = ElectionArea.objects.get(id=pid)
    data.delete()
    messages.success(request, "Election area deleted successfully")
    return redirect('electionarea_reports')

@login_required(login_url='/')
def electionarea_reports(request):
    earea = ElectionArea.objects.all()
    return render(request, "electionarea_reports.html", locals())

@login_required(login_url='/')
def change_password(request):
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Password Changed.....")
            return redirect('logout')
        else:
            messages.success(request, "New Password and Confirm Password are not match")
    if request.user.is_staff:
        return render(request, 'change_password.html', locals())
    else:
        return render(request,'change_password.html', locals())

@login_required(login_url='/')
def Logout(request):
    logout(request)
    messages.success(request, "Logout Successfully.")
    return redirect('home')


from django.utils import timezone
from datetime import datetime, timedelta


def registration(request):
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        c = request.POST['city']
        s = request.POST['state']
        z = request.POST['zipcode']
        a = request.POST['address']
        an = request.POST['adharno']
        m = request.POST['mobile']
        ai = request.FILES['adharimage']
        im = request.FILES['image']

        # Validate first name and last name
        if not f.isalpha() or not l.isalpha():
            messages.error(request, "First name and last name should contain only characters.")
            return redirect('registration')

        # Validate date of birth
        dob = datetime.strptime(d, "%Y-%m-%d")  # Convert dob string to datetime object
        eighteen_years_ago = datetime.now() - timedelta(days=18 * 365)  # Calculate 18 years ago
        if dob > eighteen_years_ago:
            messages.error(request, "You must be at least 18 years old to register.")
            return redirect('registration')

        # Validate password length
        if len(p) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('registration')

        # Validate email format
        if not (e.endswith('@gmail.com') or e.endswith('@kluniversity.in')):
            messages.error(request, "Email must end with @gmail.com or @kluniversity.in.")
            return redirect('registration')

        # Validate mobile number length
        if len(m) != 10 or not m.isdigit():
            messages.error(request, "Mobile number must be 10 digits long.")
            return redirect('registration')

        # Validate Aadhar number length
        if len(an) != 12 or not an.isdigit():
            messages.error(request, "Aadhar number must be 12 digits long.")
            return redirect('registration')

        # Check if aadharimage and image are not the same
        if ai == im:
            messages.error(request, "Aadhar image and regular image should be different.")
            return redirect('registration')

        # Create a user and voter if validations pass
        user = User.objects.create_user(username=e, email=e, first_name=f, last_name=l, password=p)
        voter = Voter.objects.create(user=user, dob=d, city=c, state=s, zipcode=z, address=a, adharimage=ai, adharno=an,
                                     image=im, mobile=m)

        messages.success(request, "Registration successful")
        return redirect('user_home')

    return render(request, "registration.html", locals())


@login_required(login_url='/')
def edit_profile(request, pid):
    data = Voter.objects.get(id=pid)
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        d = request.POST['dob']
        c = request.POST['city']
        s = request.POST['state']
        z = request.POST['zipcode']
        a = request.POST['address']
        an = request.POST['adharno']
        m = request.POST['mobile']
        try:
            ai = request.FILES['adharimage']
            data.adharimage = ai
            data.save()
        except:
            pass
        try:
            im = request.FILES['image']
            data.image = im
            data.save()
        except:
            pass
        
        er = request.POST['earea']

        eareaobj = ElectionArea.objects.get(id=er)
        user = User.objects.filter(id=data.user.id).update(first_name=f, last_name=l, email=e, username=e)
        voter = Voter.objects.filter(id=data.id).update(dob=d, city=c, state=s, zipcode=z, address=a, adharno=an, mobile=m, electionarea=eareaobj)
        messages.success(request, "Updated successfully")
        return redirect('voter_reports')
    earea = ElectionArea.objects.all()
    etype = ElectionType.objects.all()
    return render(request, "edit_profile.html", locals())

@login_required(login_url='/')
def dashboard(request):
    user = Voter.objects.get(user=request.user)
    if user.emailstatus == 2:
        return redirect('view_profile')
    if request.method == "POST":
        otp = request.POST['otp']
        if user.otp == str(otp):
            user.voteemailstatus = 1
            user.save()
            messages.success(request, "Email Verified Successfully")
            return redirect('dashboard')
        else:
            messages.success(request, "Invalid OTP.")
            return redirect('dashboard')
    voter = Voter.objects.get(user=request.user)
    voting_status = VotingStatus.objects.filter((Q(status=1) | Q(status=3)) & Q(electionarea=voter.electionarea)).first()
    etype = None
    winner = None
    if voting_status:
        candidate = Candidate.objects.filter(electionarea=voter.electionarea, electiontype=voting_status.electiontype)
        try:
            winner = Voting.objects.get(candidate__electionarea=voter.electionarea, candidate__electiontype=voting_status.electiontype, winner=True)
        except:
            winner = None
            pass
        etype = voting_status.electiontype.name
    else:
        candidate = None
        etype = ""
    print(etype, candidate)
    return render(request, "dashboard.html", {'winner':winner, 'candidate':candidate, 'data':voter, 'pid':voter.id, 'etype':etype, 'status':voting_status})

@login_required(login_url='/')
def view_profile(request):
    voter = Voter.objects.get(user=request.user)
    return render(request, 'profile.html',{'pro':voter})

@login_required(login_url='/')
def delete_profile(request, pid):
    data = Voter.objects.get(id=pid)
    data.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('delete_profile')

@login_required(login_url='/')
def startstopvoting(request):
    areacode = request.GET.get('areacode')
    electtype = request.GET.get('electtype')
    earea = ElectionArea.objects.filter().first()
    etype = ElectionType.objects.filter().first()
    vote = VotingStatus.objects.get(electionarea__id=earea.id, electiontype__id=etype.id)
    if areacode and electtype:
        vote = VotingStatus.objects.get(electionarea__id=areacode, electiontype__id=electtype)
    elif areacode:
        vote = VotingStatus.objects.get(electionarea__id=areacode, electiontype__id=etype.id)
    elif electtype:
        vote = VotingStatus.objects.get(electionarea__id=earea.id, electiontype__id=electtype)
    if vote.status == 1:
        vote.status = 2
        messages.success(request, "Voting Stopped Successfully.")
    else:
        vote.status = 1
        messages.success(request, "Voting Started Successfully.")
    vote.save()
    if areacode and electtype:
        return HttpResponseRedirect('/voting-status?areacode='+areacode+'&electtype='+electtype)
    elif areacode:
        return HttpResponseRedirect('/voting-status?areacode='+areacode)
    elif electtype:
        return HttpResponseRedirect('/voting-status?electtype='+electtype)
    else:
        return redirect('voting_status')

@login_required(login_url='/')
def vote(request, pid):
    voter = Voter.objects.get(user=request.user)
    cand = Candidate.objects.get(id=pid)
    vote = Voting.objects.get(candidate=cand)
    vote.count = int(vote.count)+1
    voter.status = 1
    vote.save()
    voter.save()
    messages.success(request, "Voted Successfully.")
    return redirect('dashboard')
    
@login_required(login_url='/')
def generateotp(request, pid):
    user = Voter.objects.get(id=pid)
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    email_host = settings.EMAIL_HOST_USER
    print(user.user.email)
    sendmail(user.user.email, random_str, user.user.first_name+" "+user.user.last_name)
    user.otp = random_str
    user.save()
    return JsonResponse({'Success':True})

def generateotpbefore(request):
    email = request.GET.get('email')
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])
    email_host = settings.EMAIL_HOST_USER
    print(email)
    sendmail(email, random_str, email)
    request.session['otp'] = random_str
    print(request.session['otp'])
    return JsonResponse({'Success':True})

def email_verify(request, pid):
    user = Voter.objects.get(id=pid)
    if request.method == "POST":
        otp = request.POST['otp']
        if user.otp == str(otp):
            user.emailstatus = 1
            user.save()
            messages.success(request, "Email Varified Successfully")
            return redirect('view_profile')
        else:
            messages.success(request, "Invalid OTP.")
            return redirect('email_verify', pid)
    return render(request, 'verify_email.html',{'pid':pid})

def reset_voting(request):
    areacode = request.GET.get('areacode')
    electtype = request.GET.get('electtype')
    earea = ElectionArea.objects.filter().first()
    etype = ElectionType.objects.filter().first()
    voting = Voting.objects.filter(candidate__electionarea__id=earea.id, candidate__electiontype__id=etype.id).update(count=0, winner=False)
    candidate = Voter.objects.filter(electionarea__id=earea.id).update(voteemailstatus=2, status=2)
    status = VotingStatus.objects.filter(electionarea__id=earea.id, electiontype__id=etype.id).update(status=2)
    if areacode and electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=electtype).update(count=0, winner=False)
        candidate = Voter.objects.filter(electionarea__id=areacode).update(voteemailstatus=2, status=2)
        status = VotingStatus.objects.filter(electionarea__id=areacode, electiontype__id=electtype).update(status=2)
    elif areacode:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=etype.id).update(count=0, winner=False)
        candidate = Voter.objects.filter(electionarea__id=areacode).update(voteemailstatus=2, status=2)
        status = VotingStatus.objects.filter(electionarea__id=areacode, electiontype__id=etype.id).update(status=2)
    elif electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=earea.id, electiontype__id=electtype).update(count=0, winner=False)
        candidate = Voter.objects.filter(electionarea__id=earea.id).update(voteemailstatus=2, status=2)
        status = VotingStatus.objects.filter(electionarea__id=earea.id, electiontype__id=electtype).update(status=2)
    messages.success(request, "Voting Process Reset Successfully.")
    if areacode and electtype:
        return HttpResponseRedirect('/voting-status?areacode='+areacode+'&electtype='+electtype)
    elif areacode:
        return HttpResponseRedirect('/voting-status?areacode='+areacode)
    elif electtype:
        return HttpResponseRedirect('/voting-status?electtype='+electtype)
    else:
        return redirect('voting_status')

def winby(areacode, elettype):
    earea = ElectionArea.objects.get(id = areacode)
    etype = ElectionType.objects.get(id = elettype)
    voting = Voting.objects.filter(candidate__electionarea__id=earea.id, candidate__electiontype__id=etype.id).order_by('-count')
    count = 0
    first = 0
    second = 0
    for i in voting:
        count += 1
        if count == 1:
            first = i.count
        if count == 2:
            second = i.count
            break
    winby = int(first) - int(second)
    return winby

def winner_announced(request):
    areacode = request.GET.get('areacode')
    electtype = request.GET.get('electtype')
    earea = ElectionArea.objects.filter().first()
    etype = ElectionType.objects.filter().first()
    if areacode and electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=electtype).order_by('-count')
        count = 0
        first = 0
        second = 0
        for i in voting:
            if count == 0:
                first = i.count
            else:
                second = i.count
                break
            count += 1
        if first == second:
            messages.success(request, "Two or more candidate have same vote.")
            if areacode and electtype:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode + '&electtype=' + electtype)
            elif areacode:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode)
            elif electtype:
                return HttpResponseRedirect('/voting-status?electtype=' + electtype)
            else:
                return redirect('voting_status')
        status = VotingStatus.objects.filter(electionarea__id=areacode, electiontype__id=electtype).update(status=3)
        history = VotingHistory.objects.create(winner=voting.first().candidate, winby=winby(areacode, electtype), electionarea=ElectionArea.objects.get(id=areacode), electiontype=ElectionType.objects.get(id=electtype))
    elif areacode:
        voting = Voting.objects.filter(candidate__electionarea__id=areacode, candidate__electiontype__id=etype.id).order_by('-count')
        count = 0
        first = 0
        second = 0
        for i in voting:
            if count == 0:
                first = i.count
            else:
                second = i.count
                break
            count += 1
        if first == second:
            messages.success(request, "Two or more candidate have same vote.")
            if areacode and electtype:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode + '&electtype=' + electtype)
            elif areacode:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode)
            elif electtype:
                return HttpResponseRedirect('/voting-status?electtype=' + electtype)
            else:
                return redirect('voting_status')
        status = VotingStatus.objects.filter(electionarea__id=areacode, electiontype__id=etype.id).update(status=3)
        history = VotingHistory.objects.create(winner=voting.first().candidate, winby=winby(areacode, etype.id), electionarea=ElectionArea.objects.get(id=areacode), electiontype=ElectionType.objects.get(id=etype.id))
    elif electtype:
        voting = Voting.objects.filter(candidate__electionarea__id=earea.id, candidate__electiontype__id=electtype).order_by('-count')
        count = 0
        first = 0
        second = 0
        for i in voting:
            if count == 0:
                first = i.count
            else:
                second = i.count
                break
            count += 1
        if first == second:
            messages.success(request, "Two or more candidate have same vote.")
            if areacode and electtype:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode + '&electtype=' + electtype)
            elif areacode:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode)
            elif electtype:
                return HttpResponseRedirect('/voting-status?electtype=' + electtype)
            else:
                return redirect('voting_status')
        status = VotingStatus.objects.filter(electionarea__id=earea.id, electiontype__id=electtype).update(status=3)
        history = VotingHistory.objects.create(winner=voting.first().candidate, winby=winby(earea.id, electtype), electionarea=ElectionArea.objects.get(id=earea.id), electiontype=ElectionType.objects.get(id=electtype))
    else:
        voting = Voting.objects.filter(candidate__electionarea__id=earea.id, candidate__electiontype__id=etype.id).order_by('-count')
        count = 0
        first = 0
        second = 0
        for i in voting:
            if count == 0:
                first = i.count
            else:
                second = i.count
                break
            count += 1
        if first == second:
            messages.success(request, "Two or more candidate have same vote.")
            if areacode and electtype:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode + '&electtype=' + electtype)
            elif areacode:
                return HttpResponseRedirect('/voting-status?areacode=' + areacode)
            elif electtype:
                return HttpResponseRedirect('/voting-status?electtype=' + electtype)
            else:
                return redirect('voting_status')
        status = VotingStatus.objects.filter(electionarea__id=earea.id, electiontype__id=etype.id).update(status=3)
        history = VotingHistory.objects.create(winner=voting.first().candidate, winby=winby(earea.id, etype.id), electionarea=ElectionArea.objects.get(id=earea.id), electiontype=ElectionType.objects.get(id=etype.id))


    voting.first().winner = True
    voting.first().save()
    messages.success(request, "Winner is announced successfully.")
    if areacode and electtype:
        return HttpResponseRedirect('/voting-status?areacode='+areacode+'&electtype='+electtype)
    elif areacode:
        return HttpResponseRedirect('/voting-status?areacode='+areacode)
    elif electtype:
        return HttpResponseRedirect('/voting-status?electtype='+electtype)
    else:
        return redirect('voting_status')

def winnerhistory(request):
    data = VotingHistory.objects.all()
    return render(request, 'history.html', locals())

def delete_history(request, pid):
    data = VotingHistory.objects.get(id=pid)
    data.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('history')

@login_required(login_url='/')
def allcandidate(request, pid):
    data = VotingHistory.objects.get(id=pid)
    candidate = Candidate.objects.filter(electionarea=data.electionarea, electiontype=data.electiontype)
    return render(request, "history_detail.html", locals())
