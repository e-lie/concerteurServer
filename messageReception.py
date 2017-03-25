#!/usr/bin/python3

""" Message reception for "le concerteur"

Usage:
  messageReception.py <sms-num> <sms-text>

Options:
  -h --help     Show this screen.

"""

from docopt import docopt
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from acapelaVaas import getAcapelaSound
from datetime import datetime
from urllib import request, parse
import os

arguments = docopt(__doc__)

params = {'num':arguments['<sms-num>'],
        'text':arguments['<sms-text>']}
url = 'http://localhost:9000/addsms'

# Encode the query string
querystring = parse.urlencode(params)

# Make a POST request and read the response
req = request.urlopen(url, querystring.encode('utf-8'))
