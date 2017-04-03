#!/usr/bin/python3

""" Message reception for "le concerteur"

Usage:
  messageReception.py <sms-num> <sms-text>

Options:
  -h --help     Show this screen.

"""

from docopt import docopt
from urllib import request, parse

arguments = docopt(__doc__)

#get arguments for command line using docopt dict
params = {'num':arguments['<sms-num>'],
        'text':arguments['<sms-text>']}

#Local POST request to the flask app using a custom port
url = 'http://localhost:9000/add-sms'

# Encode the query string
querystring = parse.urlencode(params)

# Make a POST request and read the response
req = request.urlopen(url, querystring.encode('utf-8'))
