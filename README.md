#Le concerteur 


### Installation

`virtualenv3 venv` or pyenv...
edit .env to configure database login (tested with mysql)
source .env
pip3 install -r requirements.txt
python manage.py db init
python manager.py db migrate
python manager.py db upgrade
apt-get install python3-docopt
