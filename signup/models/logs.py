from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import UTCDateTimeAttribute

from signup import app


class Log(Model):
    class Meta:
        table_name = app.config.get('DYNAMODB_TABLE_LOGS')
        if app.config.get('DYNAMODB_URL'):
            host = app.config.get('DYNAMODB_URL')
        region = app.config.get('AWS_DEFAULT_REGION')

    log_date = UTCDateTimeAttribute(default=datetime.now, hash_key=True)
    message = UnicodeAttribute()
