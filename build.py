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

def get_page(url):
    browser = RoboBrowser(user_agent='a python robot')
    browser.open(url)
    return PyQuery(browser.response.text)

def make_url(base, partial):
    if partial.startswith('http') or not len(base):
        return partial

    return urlparse.urljoin(base, partial)

###
# Get news
###
news_base_url = "http://www.stuff.co.nz/dominion-post"
news_base = get_page(news_base_url)

# Get main stories
stories = []
for item in news_base('section.portrait .it-article-headline a').items():
    story = get_page(make_url(news_base_url, item.attr.href))
    title = story('article.story_landing h1').text()

    stories.append(title)


###
# Get weather
###
weather_current_url = "http://api.wunderground.com/api/{0}/conditions/q/{1}.json".format(config.WUNDERLAND_API, config.WUNDERLAND_LOCATION)
r = urllib.urlopen(weather_current_url)
weather_current = json.loads(r.read())['current_observation']

weather = []
weather.append({
    'day': 'Now',
    'temperature': weather_current['temp_c'],
    'forecast': weather_current['weather'],
    'wind': weather_current['wind_string'],
    'icon': weather_current['icon']
})

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
    weather.append({
        'day': day['title'],
        'temperature': detail['low']['celsius'] if i in (2,4) else detail['high']['celsius'],
        'forecast': day['fcttext_metric'],
        'wind': str(detail['maxwind']['kph']) + 'kph ' + (detail['maxwind']['dir'] if detail['maxwind']['dir'] != 'Variable' else ''),
        'icon': day['icon']
    });


ret = {
    'news': stories,
    'weather': weather
}

print json.dumps(ret, indent=4)
