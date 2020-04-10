from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from github import Github
from profanity_check import predict, predict_prob
from datetime import datetime
from pytz import timezone
import pytz


import os

project_desc="""
### Wait Time Now
Wait Time Now is not responsible for the accuracy of this crowdsourced data and assumes no responsibility for any errors or omissions. The User assumes the entire risk associated with the use of this crowdsourced data.   
"""

repository='aiformankind/wait-time'
page='wait_time.md'
reply_message='Thank you for sharing the infos.'

app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Wait Time Now"



@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Process incoming msg"""
    body = request.values.get('Body', None)
    json_output = body

    now = datetime.now(tz=pytz.utc)

    date = now.astimezone(timezone('US/Pacific'))

    dt_string = date.strftime("%Y/%m/%d %H:%M:%S %Z")

    json_output += " submitted at "+dt_string


    #TODOS
    #zipcode to parse zipcode eg. wholefood 20 mins 91456, 94577 wholefood  10 mins call google map api, robust parsing/handling
    #geocoding api or yelp api

    g = Github(os.getenv('GIT_TOKEN'))

    repo = g.get_repo(repository)

    contents = repo.get_contents(page, ref="master")

    original_contents = contents.decoded_content.decode("utf-8")

    original_contents = original_contents.split("\n")[3:]
    original_contents = '\n'.join([str(elem) for elem in original_contents])

    updated_content = project_desc + "\n\n\n" + "#### "+json_output + "\n\n" + original_contents

    #print("Updated {}".format(updated_content))
    ### update web page
    repo.update_file(contents.path, "add latest items", updated_content, contents.sha, branch="master")

    # Start our TwiML response
    resp = MessagingResponse()
    resp.message(reply_message)
    return str(resp)
