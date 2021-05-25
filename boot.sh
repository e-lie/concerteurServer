#!/bin/bash
set -e
uwsgi --http 0.0.0.0:9090 --wsgi-file /concerteur_server/wsgi.py --callable application --stats 0.0.0.0:9191
