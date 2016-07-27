import time

from pynamodb.exceptions import TableError

from signup import app
from shifts import Shift

# Only used when using dynamodb local
if app.config.get('DYNAMODB_CREATE_TABLE'):
    i = 0
    # This loop is absurd, but there's race conditions with dynamodb local
    while i < 5:
        try:
            if not Shift.exists():
                Shift.create_table(
                    read_capacity_units=10,
                    write_capacity_units=10,
                    wait=True
                )
            break
        except TableError:
            i = i + 1
            time.sleep(2)
