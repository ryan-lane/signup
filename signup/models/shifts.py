from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import UTCDateTimeAttribute

from signup import app


class Shift(Model):
    class Meta:
        table_name = app.config.get('DYNAMODB_TABLE')
        if app.config.get('DYNAMODB_URL'):
            host = app.config.get('DYNAMODB_URL')
        region = app.config.get('AWS_DEFAULT_REGION')

    shift_id = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()
    name = UnicodeAttribute()
    modified_date = UTCDateTimeAttribute(default=datetime.now)
