from __future__ import print_function
import datetime
import json
import os.path
import pickle
import pytz
import re
import subprocess

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as gRequest
import requests

from config import CALENDARS, TIMEZONE, EVENT_REGEX


# If modifying these scopes, delete your previously saved credentials
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CLIENT_SECRET_FILE = 'token.pickle'


def get_credentials():
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CLIENT_SECRET_FILE):
        with open(CLIENT_SECRET_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(gRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(CLIENT_SECRET_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


###
# Get Google Calender entries
###
credentials = get_credentials()
service = build('calendar', 'v3', credentials=credentials)

# Call the Calendar API
tz = pytz.timezone(TIMEZONE)
midnight = tz.localize(datetime.datetime.combine(datetime.datetime.now(tz), datetime.time(0, 0)))
startTimeObj = midnight.astimezone(pytz.utc)
startTime = startTimeObj.isoformat()
endTimeObj = startTimeObj + datetime.timedelta(4)
endTime = endTimeObj.isoformat()

#for c in service.calendarList().list().execute().get('items'):
#    print(c)


events = []
for title, calendar in CALENDARS.iteritems():
    events_result = service.events().list(calendarId=calendar, timeMin=startTime, timeMax=endTime, maxResults=40, singleEvents=True, orderBy='startTime', timeZone=TIMEZONE).execute()
    eventsResult = events_result.get('items', [])

    for event in eventsResult:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end   = event['start'].get('dateTime', event['end'].get('date'))

        etitle = title
        for regex, newtitle in EVENT_REGEX:
            if re.match(regex, event['summary']) is not None:
                etitle = newtitle

        events.append((start, end, event['summary'], etitle, event['id']))


# Resort the list of events by starttime now we have retreived from all calendars
events = sorted(events, cmp=lambda x,y: cmp(x[0],y[0]))


###
# Get sweet photo
###
reddit_photos_url = "https://www.reddit.com/r/EarthPorn/top/.json?sort=top&t=day"
r = requests.get(reddit_photos_url, headers={'User-Agent': 'https://github.com/srynot4sale/alfred'})
photo_listings = r.json()
for photo in photo_listings.get('data', {}).get('children', []):
    if photo['data']['domain'] not in ('i.imgur.com', 'i.redd.it'):
        continue

    if photo['data']['over_18']:
        continue

    photo_url = photo['data']['url']
    break


ret = {
    'cachebust': get_git_revision_hash(),
    'events': events,
    'background': photo_url
}

print(json.dumps(ret, indent=4))
