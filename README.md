# Alfred

Alfred is a simple weather / calendar dashboard, perfect for running on a spare PC / Raspberry Pi hooked
up to a screen.

The code is simple... just static files and a cron job. Set it up behind a webserver and then just open
in a browser.

Code is very basic, thrown-together and haphazard. But does the trick!

![Screenshot of Alfred in action](https://raw.githubusercontent.com/srynot4sale/alfred/master/screenshot.png)


## Dependency

- Python 2.x (w/ virtualenv and pip)
- Static webserver
- Browser (can be on seperate machine)


## Installation

    cd srcdir

    # Install pip requirements
    virtualenv env
    env/bin/pip install -r requirements.txt

    # Setup cron job
    cp alfred.cron /etc/cron.d/alfred
    vim /etc/cron.d/alfred # Fix user and paths


## Setup

You'll need to setup Google Calendar credentials

    cd srcdir
    env/bin/python build.py
