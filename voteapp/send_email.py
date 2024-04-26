from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

SENDEREMAIL = "bhuwanbhaskar761@gmail.com"

def sendmail(myemail, random_str, username):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Verification Code"
    html_content = "<html><body><h4>Your Email Verification code is : </h4><h3>"+str(random_str)+"</h3></body></html>"
    sender = {"name":"Voting System","email":SENDEREMAIL}
    to = [{"email":str(myemail),"name":username}]
    reply_to = {"email":SENDEREMAIL,"name":"Voting System"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    params = {"parameter":"My param value","subject":"Voting System"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)