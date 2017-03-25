import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from app import app, db


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

server = Server(host="0.0.0.0", port=9000)

manager.add_command("runserver", server)


if __name__ == '__main__':
    manager.run()

