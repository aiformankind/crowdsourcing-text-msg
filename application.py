import os
from datetime import datetime

import pytz
from flask import Flask, request
from github import Github
from pytz import timezone
from twilio.twiml.messaging_response import MessagingResponse

import pyap
from src.sqlite_helper import execute_query
from geopy.geocoders import Nominatim
import folium


PROJECT_DESC = """
### Wait Time Now
Wait Time Now is not responsible for the accuracy of this crowdsourced data and assumes no responsibility for any errors or omissions. The User assumes the entire risk associated with the use of this crowdsourced data.   
"""
REPOSITORY_NAME = 'aiformankind/messaging_dev_test'
READEME_PAGE = 'wait_time.md'
REPLY_MESSAGE = 'Thank you for sharing the infos.'

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to Wait Time Now"

@app.route("/map", methods=['GET', 'POST'])
def map():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    return folium_map._repr_html_()

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Process incoming msg"""
    body = request.values.get('Body', None)
    json_output_original = body

    now = datetime.now(tz=pytz.utc)

    date = now.astimezone(timezone('US/Pacific'))

    dt_string = date.strftime("%Y/%m/%d %H:%M:%S %Z")

    json_output = json_output_original + " submitted at " + dt_string

    # TODOS
    # zipcode to parse zipcode eg. wholefood 20 mins 91456, 94577 wholefood  10 mins call google map api, robust parsing/handling
    # geocoding api or yelp api

    g = Github(os.getenv('GIT_TOKEN'))

    repo = g.get_repo(REPOSITORY_NAME)

    contents = repo.get_contents(READEME_PAGE, ref="master")

    original_contents = contents.decoded_content.decode("utf-8")

    original_contents = original_contents.split("\n")[3:]
    original_contents = '\n'.join([str(elem) for elem in original_contents])


    sql_cmd = "INSERT INTO message VALUES ('{}')".format(json_output)
    execute_query(sql_cmd)

    #print(json_output_original.upper())
    addresses = pyap.parse(json_output_original.upper(), country='US')

    #print(len(addresses))

    if(len(addresses) > 0):
        parsed_address = addresses[0].as_dict()['full_address']
        #print(parsed_address)
        geolocator = Nominatim(user_agent="crowdsourcing")
        location = geolocator.geocode(parsed_address)
        if location is not None:
            #insert into DB processed table
            sql_insert_cmd = "INSERT INTO processed(address, latitude, longitude, message) VALUES('{}','{}','{}','{}')".format(parsed_address,
                                                                                                                       location.latitude,
                                                                                                                       location.longitude,
                                                                                                                       json_output)

            execute_query(sql_insert_cmd)


    updated_content = PROJECT_DESC + "\n\n\n" + "#### " + json_output + "\n\n" + original_contents

    # print("Updated {}".format(updated_content))
    ### update web page
    repo.update_file(contents.path, "add latest items", updated_content, contents.sha, branch="master")

    # Start our TwiML response
    resp = MessagingResponse()
    resp.message(REPLY_MESSAGE)
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
