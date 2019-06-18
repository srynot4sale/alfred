# Alfred

Alfred is a simple weather / calendar dashboard, perfect for running on a spare PC / Raspberry Pi hooked
up to a screen.

The code is simple... a simple Next.js server and a cron job. Set it up on a linux host running docker and
then just open in a browser.

Code is very basic, thrown-together and haphazard. But does the trick!

![Screenshot of Alfred in action](https://raw.githubusercontent.com/srynot4sale/alfred/master/screenshot.png)


# How it works

The ``build.py`` Python script is called by the cron job and builds the ``feed.json`` file. This is regularly
loaded by the webpage and used to refresh the data on the screen. The webpage will also detect if you have
pulled some new code and refresh the page.

``build.py`` uses uses the Google Calendar API for the calendar which means it supports Family calendars, and
https://reddit.com/r/earthporn for the background.


## Dependencies

- Python 3.x (w/ virtualenv and pip)
- Docker
- Browser (can be on seperate machine)


## Installation

    cd srcdir

    # Install pip requirements
    virtualenv -p /usr/bin/python3 env
    env/bin/pip install -r requirements.txt

    # Update config
    cp config.py.example config.py
    vim config.py # Update details

    # Build
    make


## Setup & run

You'll need to setup Google Calendar credentials

    cd srcdir
    env/bin/python build.py

    # Setup cron job
    cp alfred.cron /etc/cron.d/alfred
    vim /etc/cron.d/alfred # Fix user and paths

    # Wait for first cron run

    # Run frontend
    docker-compose up -d

    # Open http://localhost:3000 in your browser!
