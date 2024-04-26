"""Voting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from voteapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-home', home, name="home"),
    path('', user_home, name="user_home"),
    path('login-voter', login_voter, name="login_voter"),
    path('admin-login', admin_login, name="admin_login"),
    path('voting-status', voting_status, name="voting_status"),
    path('candidate-reports', candidate_reports, name="candidate_reports"),
    path('voter-reports', voter_reports, name="voter_reports"),
    path('new-candidate', new_candidate, name="new_candidate"),
    path('edit-candidate/<int:pid>', edit_candidate, name="edit_candidate"),
    path('delete-candidate/<int:pid>', delete_candidate, name="delete_candidate"),

    path('electiontype-reports', electiontype_reports, name="electiontype_reports"),
    path('new-electiontype', new_electiontype, name="new_electiontype"),
    path('edit-electiontype/<int:pid>', edit_electiontype, name="edit_electiontype"),
    path('delete-electiontype/<int:pid>', delete_electiontype, name="delete_electiontype"),

    path('electionarea-reports', electionarea_reports, name="electionarea_reports"),
    path('new-electionarea', new_electionarea, name="new_electionarea"),
    path('edit-electionarea/<int:pid>', edit_electionarea, name="edit_electionarea"),
    path('delete-electionarea/<int:pid>', delete_electionarea, name="delete_electionarea"),

    path('change-password', change_password, name="change_password"),
    path('logout', Logout, name="logout"),
    path('logout/', Logout, name="logout"),
    path('registration/', registration, name="registration"),
    path('dashboard', dashboard, name="dashboard"),
    path('dashboard/', dashboard, name="dashboard"),
    path('view-profile/', view_profile, name="view_profile"),
    path('edit-profile/<int:pid>', edit_profile, name="edit_profile"),
    path('delete-profile/<int:pid>', delete_profile, name="delete_profile"),


    path('startstopvoting', startstopvoting, name="startstopvoting"),
    path('vote/<int:pid>', vote, name="vote"),
    path('generateotp/<int:pid>', generateotp, name="generateotp"),
    path('generateotpbefore/', generateotpbefore, name="generateotpbefore"),
    path('email-verify/<int:pid>', email_verify, name="email_verify"),
    path('reset-voting', reset_voting, name="reset_voting"),
    path('winner-announced', winner_announced, name="winner_announced"),
    path('winnerhistory', winnerhistory, name="history"),
    path('delete-history/<int:pid>', delete_history, name="delete_history"),
    path('allcandidate/<int:pid>', allcandidate, name="allcandidate"),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
