# Alfred

Alfred is a simple weather / calendar dashboard, perfect for running on a spare PC / Raspberry Pi hooked
up to a screen.

The code is simple... just static files and a cron job. Set it up behind a webserver and then just open
in a browser.

Code is very basic, thrown-together and haphazard. But does the trick!

![Screenshot of Alfred in action](https://raw.githubusercontent.com/srynot4sale/alfred/master/screenshot.png)


# How it works

The ``build.py`` Python script is called by the cron job and builds the ``feed.json`` file. This is regularly
loaded by the webpage and used to refresh the data on the screen. The webpage will also detect if you have
pulled some new code and refresh the page.

``build.py`` uses http://weather.com as a datasource for the weather, Google Calendar for the calendar, and
https://reddit.com/r/earthporn for the background.


## Dependencies

- Python 2.x (w/ virtualenv and pip)
- Static webserver
- Browser (can be on seperate machine)


## Installation

    cd srcdir

    # Install required packages
    sudo apt install libxml2-dev libxslt1-dev python-dev

    # Install pip requirements
    virtualenv env
    env/bin/pip install -r requirements.txt

    # Update config
    cp config.py.example config.py
    vim config.py # Update weather details

    # Setup cron job
    cp alfred.cron /etc/cron.d/alfred
    vim /etc/cron.d/alfred # Fix user and paths

    # Build
    cd alfred-fe
    npm install

    npm start


## Setup

You'll need to setup Google Calendar credentials

    cd srcdir
    env/bin/python build.py
