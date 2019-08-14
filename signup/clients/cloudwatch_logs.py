import logging
import time

import boto3

from signup import settings

_CWLOGS_CLIENT = None


def _get_client():
    global _CWLOGS_CLIENT
    if _CWLOGS_CLIENT is None:
        _CWLOGS_CLIENT = boto3.client('logs')
    return _CWLOGS_CLIENT


def log_event(message):
    logs = _get_client()
    timestamp = int(round(time.time() * 1000))
    try:
        logs.put_log_events(
            logGroupName=settings.LOG_GROUP,
            logStreamName=settings.LOG_STREAM,
            logEvents=[
                {
                    'timestamp': timestamp,
                    'message': message,
                },
            ],
        )
    except Exception:
        logging.error('Failed to log event {}'.format(message))


def get_logs(start_time, end_time):
    logs = _get_client()
    response = logs.get_log_events(
        logGroupName=settings.LOG_GROUP,
        logStreamName=settings.LOG_STREAM,
        startTime=start_time,
        endTime=end_time,
        limit=10000,
        startFromHead=True,
    )
    return response['events']
