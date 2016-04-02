from pyquery import PyQuery
from robobrowser import RoboBrowser
import bleach
import json
import logging
import os.path
import requests
import urllib
import urlparse
#import PIL.Image
#import unicodecsv

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
r = urllib.urlopen('http://www.metservice.com/publicData/localForecastWellington')
data = json.loads(r.read())

weather = []
days = {'Today': 0, 'Tomorrow': 1}
dates = days.keys()
dates.sort()
for day in dates:
    d = data['days'][days[day]]

    daydata = {'day': day}
    for i in ('dow', 'date', 'min', 'max', 'forecast', 'forecastWord'):
        daydata[i] = d[i]

    weather.append(daydata)


ret = {
    'news': stories,
    'weather': weather
}

print json.dumps(ret, indent=4)
