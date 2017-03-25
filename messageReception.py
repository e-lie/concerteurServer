from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from acapelaVaas import getAcapelaSound
from datetime import datetime
from urllib import request, parse
import os

smsNum = 33637105067
smsText = "Ceci est un message de test"

params = {'num':smsNum,
        'text':smsText}
url = 'http://localhost:9000/addsms'

# Encode the query string
querystring = parse.urlencode(params)

# Make a POST request and read the response
u = request.urlopen(url, querystring.encode('utf-8'))
mp3Response = u.read()
print(mp3Response)
