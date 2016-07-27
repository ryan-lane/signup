#!/usr/bin/env python

from flask.ext.script import Manager

from signup import app
from signup.scripts.utils import DumpCSV

manager = Manager(app)

manager.add_command("dumpcsv", DumpCSV)

if __name__ == "__main__":
    manager.run()
