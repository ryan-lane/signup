import boto3
from flask.ext.script import Command

from signup import settings


class CreateLogs(Command):

    def run(self):
        logs = boto3.client('logs')
        logs.create_log_group(logGroupName=settings.LOG_GROUP)
        logs.create_log_stream(
            logGroupName=settings.LOG_GROUP,
            logStreamName=settings.LOG_STREAM,
        )
