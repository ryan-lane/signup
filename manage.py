#!/usr/bin/env python

from flask.ext.script import Manager

from signup import app
from signup.scripts.utils import CreateLogs

manager = Manager(app)

manager.add_command("create-logs", CreateLogs)

if __name__ == "__main__":
    manager.run()
