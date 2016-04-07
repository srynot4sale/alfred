from __future__ import print_function
import httplib2
import os
import re

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime
from pyquery import PyQuery
from robobrowser import RoboBrowser
import bleach
import json
import logging
import os.path
import requests
import urllib
import urlparse

import config

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Alfred'

def get_credentials():
    """Gets valid Google credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_page(url):
    browser = RoboBrowser(user_agent='a python robot')
    browser.open(url)
    return PyQuery(browser.response.text)

def make_url(base, partial):
    if partial.startswith('http') or not len(base):
        return partial

    return urlparse.urljoin(base, partial)

def get_git_revision_hash():
    import subprocess
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()


###
# Get Google Calender entries
###
credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
eventsResult = service.events().list(
    calendarId='primary', timeMin=now, maxResults=20, singleEvents=True,
    orderBy='startTime').execute()
eventsResult = eventsResult.get('items', [])

events = []
for event in eventsResult:
    start = event['start'].get('dateTime', event['start'].get('date'))
    events.append((start, event['summary']))


###
# Get weather
###
weather_current_url = "http://api.wunderground.com/api/{0}/conditions/q/{1}.json".format(config.WUNDERLAND_API, config.WUNDERLAND_LOCATION)
r = urllib.urlopen(weather_current_url)
weather_current = json.loads(r.read())['current_observation']

weather = [
    {
        'day': 'Now'
    },
    {
        'day': 'Today'
    },
    {
        'day': 'Tonight'
    },
    {
        'day': 'Tomorrow'
    },
    {
        'day': 'Tomorrow night'
    }
]

weather[0] = {
    'day': 'Now',
    'temperature': weather_current['temp_c'],
    'forecast': weather_current['weather'],
    'wind': str(weather_current['wind_kph']) + ' km/h ' + (weather_current['wind_dir'] if weather_current['wind_dir'] != 'Variable' else ''),
    'icon': weather_current['icon']
}

weather_future_url = "http://api.wunderground.com/api/{0}/forecast/q/{1}.json".format(config.WUNDERLAND_API, config.WUNDERLAND_LOCATION)
r = urllib.urlopen(weather_future_url)
weather_future_json = json.loads(r.read())
weather_future_simple = weather_future_json['forecast']['txt_forecast']['forecastday']
weather_future_detail = weather_future_json['forecast']['simpleforecast']['forecastday']

i = 0
for day in weather_future_simple:
    i += 1
    if i > 4:
        break

    detail = weather_future_detail[0 if i in (1,2) else 1]
    icon = day['icon']
    forecast = day['fcttext_metric']

    # Remove temp
    forecast = re.sub(r'(Low|High) [0-9]+C\.(\s+)?', '', forecast)
    wind = re.compile(r'Winds ([^\s]+) at ([^\.]+ km\/h)\.').search(forecast)
    if wind:
        forecast = re.sub(r'Winds [^\s]+ at [^\.]+ km\/h\.(\s+)?', '', forecast)
        wind = '{0} {1}'.format(wind.group(2), wind.group(1)).replace(' to ', '-')
    else:
        wind = str(detail['maxwind']['kph']) + ' km/h ' + (detail['maxwind']['dir'] if detail['maxwind']['dir'] != 'Variable' else '')

    temperature = detail['low']['celsius'] if i in (2,4) else detail['high']['celsius']

    weather[i]['temperature'] = temperature
    weather[i]['forecast'] = forecast.strip()
    weather[i]['wind'] = wind.strip()
    weather[i]['icon'] = icon


ret = {
    'cachebust': get_git_revision_hash(),
    'weather': weather,
    'events': events
}

print(json.dumps(ret, indent=4))
