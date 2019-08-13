import json
from os import getenv


def bool_env(var_name, default=False):
    """
    Get an environment variable coerced to a boolean value.
    Example:
        Bash:
            $ export SOME_VAL=True
        settings.py:
            SOME_VAL = bool_env('SOME_VAL', False)
    Arguments:
        var_name: The name of the environment variable.
        default: The default to use if `var_name` is not specified in the
                 environment.
    Returns: `var_name` or `default` coerced to a boolean using the following
        rules:
            "False", "false" or "" => False
            Any other non-empty string => True
    """
    test_val = getenv(var_name, default)
    # Explicitly check for 'False', 'false', and '0' since all non-empty
    # string are normally coerced to True.
    if test_val in ('False', 'false', '0'):
        return False
    return bool(test_val)


def float_env(var_name, default=0.0):
    """
    Get an environment variable coerced to a float value.
    This has the same arguments as bool_env. If a value cannot be coerced to a
    float, a ValueError will be raised.
    """
    return float(getenv(var_name, default))


def int_env(var_name, default=0):
    """
    Get an environment variable coerced to an integer value.
    This has the same arguments as bool_env. If a value cannot be coerced to an
    integer, a ValueError will be raised.
    """
    return int(getenv(var_name, default))


def str_env(var_name, default=''):
    """
    Get an environment variable as a string.
    This has the same arguments as bool_env.
    """
    return getenv(var_name, default)

DEBUG = bool_env('DEBUG', False)
PORT = int_env('PORT', 80)
STATIC_FOLDER = str_env('STATIC_FOLDER', 'public')

# SSL redirection and HSTS
SSLIFY = bool_env('SSLIFY', False)

# Dynamo storage

# The DynamoDB URL
# Example: http://localhost:8000
DYNAMODB_URL = str_env('DYNAMODB_URL')
# The DynamoDB table to use for storage.
# Example: mydynamodbtable
DYNAMODB_TABLE = str_env('DYNAMODB_TABLE')
# Whether or not to allow signup to generate its own DynamoDB table via
# PynamoDB.
DYNAMODB_CREATE_TABLE = bool_env('DYNAMODB_CREATE_TABLE', False)
# Must be set to the region the server is running.
AWS_DEFAULT_REGION = str_env('AWS_DEFAULT_REGION', 'us-east-1')

# Mail
MAILGUN_URL = str_env('MAILGUN_URL')
MAILGUN_API_KEY = str_env('CREDENTIALS_MAILGUN_API_KEY')
MAILGUN_FROM_ADDRESS = str_env('MAILGUN_FROM_ADDRESS')
CHANGELOG_ADDRESS = str_env('CHANGELOG_ADDRESS')
CHANGELOG_SUBJECT = str_env('CHANGELOG_SUBJECT')
CHANGELOG_BODY = str_env('CHANGELOG_BODY')
CHANGELOG_BODY_REMOVED = str_env('CHANGELOG_BODY_REMOVED')

# Tickets
TICKETS_EMAIL_SUBJECT = str_env('TICKETS_EMAIL_SUBJECT')
TICKETS_EMAIL_BODY = str_env('TICKETS_EMAIL_BODY')
TICKETS_CODE = json.loads(str_env('TICKETS_CODE', '{}'))
TICKETS_EMAIL_SUBJECT_TAKEN = str_env('TICKETS_EMAIL_SUBJECT_TAKEN')
TICKETS_EMAIL_BODY_TAKEN = str_env('TICKETS_EMAIL_BODY_TAKEN')
TICKETS_EMAIL_SUBJECT_REMOVED = str_env('TICKETS_EMAIL_SUBJECT_REMOVED')
TICKETS_EMAIL_BODY_REMOVED = str_env('TICKETS_EMAIL_BODY_REMOVED')

# Shifts
SHIFTS = [
    {'name': 'Friday Afternoon and Night Site Coordinator *',
     'shifts': [
        {'shift_id': 'frisc1', 'position': 'Site Coordinator', 'day': 'Friday', 'time': '12:00pm - 3:00pm', 'code': 'sc'},
        {'shift_id': 'friasc1', 'position': 'Assistant Site Coordinator', 'day': 'Friday', 'time': '12:00pm - 3:00pm', 'code': 'sc'},
        {'shift_id': 'frisc2', 'position': 'Site Coordinator', 'day': 'Friday', 'time': '3:00pm - 6:00pm', 'code': 'sc'},
        {'shift_id': 'friasc2', 'position': 'Assistant Site Coordinator', 'day': 'Friday', 'time': '3:00pm - 6:00pm', 'code': 'sc'},
        {'shift_id': 'frisc3', 'position': 'Site Coordinator', 'day': 'Friday', 'time': '6:00pm - 9:00pm', 'code': 'sc'},
        {'shift_id': 'friasc3', 'position': 'Assistant Site Coordinator', 'day': 'Friday', 'time': '6:00pm - 9:00pm', 'code': 'sc'},
        {'shift_id': 'frisc4', 'position': 'Site Coordinator', 'day': 'Friday', 'time': '9:00pm - 12:00am', 'code': 'sc'},
        {'shift_id': 'friasc4', 'position': 'Assistant Site Coordinator', 'day': 'Friday', 'time': '9:00pm - 12:00am', 'code': 'sc'},
        {'shift_id': 'frisc5', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '12:00am - 3:00am', 'code': 'sc'},
        {'shift_id': 'friasc5', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '12:00am - 3:00am', 'code': 'sc'},
        {'shift_id': 'frisc6', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '3:00am - 6:00am', 'code': 'sc'},
        {'shift_id': 'friasc6', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '3:00am - 6:00am', 'code': 'sc'},
        {'shift_id': 'frisc7', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '6:00am - 9:00am', 'code': 'sc'},
        {'shift_id': 'friasc7', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '6:00am - 9:00am', 'code': 'sc'},
    ]},
    {'name': 'Friday Gate and Parking',
     'shifts': [
        {'shift_id': 'frigate1', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '12:00pm - 1:30pm'},
        {'shift_id': 'frigate2', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '12:00pm - 1:30pm'},
        {'shift_id': 'frigate3', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '1:20pm - 3:00pm'},
        {'shift_id': 'frigate4', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '1:20pm - 3:00pm'},
        {'shift_id': 'frigate5', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'frigate6', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'frigate7', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'frigate8', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'frigate9', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'frigate10', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'frigate11', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'frigate12', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'frigate13', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'frigate14', 'position': 'Gate and Parking 4', 'day': 'Friday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'frigate15', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'frigate16', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'frigate17', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'frigate18', 'position': 'Gate and Parking 4', 'day': 'Friday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'frigate19', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'frigate20', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'frigate21', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'frigate22', 'position': 'Gate and Parking 4', 'day': 'Friday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'frigate23', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'frigate24', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'frigate25', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'frigate26', 'position': 'Gate and Parking 4', 'day': 'Friday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'frigate27', 'position': 'Gate and Parking 1', 'day': 'Friday', 'time': '11:50pm - 1:30am'},
        {'shift_id': 'frigate28', 'position': 'Gate and Parking 2', 'day': 'Friday', 'time': '11:50pm - 1:30am'},
        {'shift_id': 'frigate29', 'position': 'Gate and Parking 3', 'day': 'Friday', 'time': '11:50pm - 1:30am'},
        {'shift_id': 'frigate30', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '1:20am - 3:00am'},
        {'shift_id': 'frigate31', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '1:20am - 3:00am'},
    ]},
    {'name': 'Saturday Morning through Sunday Morning Site Coordinator *',
     'shifts': [
        {'shift_id': 'satsc1', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '9:00am - 12:00pm', 'code': 'sc'},
        {'shift_id': 'satasc1', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '9:00am - 12:00pm', 'code': 'sc'},
        {'shift_id': 'satsc2', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '12:00pm - 3:00pm', 'code': 'sc'},
        {'shift_id': 'satasc2', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '12:00pm - 3:00pm', 'code': 'sc'},
        {'shift_id': 'satsc3', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '3:00pm - 6:00pm', 'code': 'sc'},
        {'shift_id': 'satasc3', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '3:00pm - 6:00pm', 'code': 'sc'},
        {'shift_id': 'satsc4', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '6:00pm - 9:00pm', 'code': 'sc'},
        {'shift_id': 'satasc4', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '6:00pm - 9:00pm', 'code': 'sc'},
        {'shift_id': 'satsc5', 'position': 'Site Coordinator', 'day': 'Saturday', 'time': '9:00pm - 12:00am', 'code': 'sc'},
        {'shift_id': 'satasc5', 'position': 'Assistant Site Coordinator', 'day': 'Saturday', 'time': '9:00pm - 12:00am', 'code': 'sc'},
        {'shift_id': 'satsc6', 'position': 'Site Coordinator', 'day': 'Sunday', 'time': '12:00am - 3:00am', 'code': 'sc'},
        {'shift_id': 'satasc6', 'position': 'Assistant Site Coordinator', 'day': 'Sunday', 'time': '12:00am - 3:00am', 'code': 'sc'},
        {'shift_id': 'satsc7', 'position': 'Site Coordinator', 'day': 'Sunday', 'time': '3:00am - 6:00am', 'code': 'sc'},
        {'shift_id': 'satasc7', 'position': 'Assistant Site Coordinator', 'day': 'Sunday', 'time': '3:00am - 6:00am', 'code': 'sc'},
        {'shift_id': 'satsc8', 'position': 'Site Coordinator', 'day': 'Sunday', 'time': '6:00am - 9:00am', 'code': 'sc'},
        {'shift_id': 'satasc8', 'position': 'Assistant Site Coordinator', 'day': 'Sunday', 'time': '6:00am - 9:00am', 'code': 'sc'},
        {'shift_id': 'satsc9', 'position': 'Site Coordinator', 'day': 'Sunday', 'time': '9:00am - 12:00pm', 'code': 'sc'},
        {'shift_id': 'satasc9', 'position': 'Assistant Site Coordinator', 'day': 'Sunday', 'time': '9:00am - 12:00pm', 'code': 'sc'},
    ]},
    {'name': 'Saturday Gate and Parking',
     'shifts': [
        {'shift_id': 'satgate1', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '9:00am - 10:30am'},
        {'shift_id': 'satgate2', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '9:00am - 10:30am'},
        {'shift_id': 'satgate3', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '10:20am - 12:00pm'},
        {'shift_id': 'satgate4', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '10:20am - 12:00pm'},
        {'shift_id': 'satgate5', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '11:50am - 1:30pm'},
        {'shift_id': 'satgate6', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '11:50am - 1:30pm'},
        {'shift_id': 'satgate7', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '11:50am - 1:30pm'},
        {'shift_id': 'satgate8', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '1:20pm - 3:00pm'},
        {'shift_id': 'satgate9', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '1:20pm - 3:00pm'},
        {'shift_id': 'satgate10', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '1:20pm - 3:00pm'},
        {'shift_id': 'satgate11', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'satgate12', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'satgate13', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '2:50pm - 4:30pm'},
        {'shift_id': 'satgate14', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'satgate15', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'satgate16', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '4:20pm - 6:00pm'},
        {'shift_id': 'satgate17', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'satgate18', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'satgate19', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '5:50pm - 7:30pm'},
        {'shift_id': 'satgate20', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'satgate21', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'satgate22', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '7:20pm - 9:00pm'},
        {'shift_id': 'satgate23', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'satgate24', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'satgate25', 'position': 'Gate and Parking 3', 'day': 'Saturday', 'time': '8:50pm - 10:30pm'},
        {'shift_id': 'satgate26', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'satgate27', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '10:20pm - 12:00am'},
        {'shift_id': 'satgate28', 'position': 'Gate and Parking 1', 'day': 'Saturday', 'time': '11:50pm - 1:30am'},
        {'shift_id': 'satgate29', 'position': 'Gate and Parking 2', 'day': 'Saturday', 'time': '11:50pm - 1:30am'},
        {'shift_id': 'satgate30', 'position': 'Gate and Parking 1', 'day': 'Sunday', 'time': '1:20am - 3:00am'},
        {'shift_id': 'satgate31', 'position': 'Gate and Parking 2', 'day': 'Sunday', 'time': '1:20am - 3:00am'},
    ]},
    {'name': 'Friday Food',
     'shifts': [
        {'shift_id': 'friprep1', 'position': 'Prep 1', 'day': 'Friday', 'time': '3:00pm - 5:00pm'},
        {'shift_id': 'friprep2', 'position': 'Prep 2', 'day': 'Friday', 'time': '3:00pm - 5:00pm'},
        {'shift_id': 'friprep3', 'position': 'Prep 1', 'day': 'Friday', 'time': '4:30pm - 6:30pm'},
        {'shift_id': 'friprep4', 'position': 'Prep 2', 'day': 'Friday', 'time': '4:30pm - 6:30pm'},
        {'shift_id': 'friprep5', 'position': 'Prep 3', 'day': 'Friday', 'time': '4:30pm - 6:30pm'},
        {'shift_id': 'friprep6', 'position': 'Prep 4', 'day': 'Friday', 'time': '4:30pm - 6:30pm'},
        {'shift_id': 'friprep7', 'position': 'Prep 1', 'day': 'Friday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'friprep8', 'position': 'Prep 2', 'day': 'Friday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'friprep9', 'position': 'Prep 3', 'day': 'Friday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'friprep10', 'position': 'Prep 4', 'day': 'Friday', 'time': '6:00pm - 8:00pm'},
    ]},
    {'name': 'Saturday Brunch Prep and Serve',
     'shifts': [
        {'shift_id': 'satbrunchprep1', 'position': 'Prep 1', 'day': 'Saturday', 'time': '8:00am - 10:00am'},
        {'shift_id': 'satbrunchprep2', 'position': 'Prep 2', 'day': 'Saturday', 'time': '8:00am - 10:00am'},
        {'shift_id': 'satbrunchprep3', 'position': 'Prep 1', 'day': 'Saturday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'satbrunchprep4', 'position': 'Prep 2', 'day': 'Saturday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'satbrunchprep5', 'position': 'Serve 1', 'day': 'Saturday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'satbrunchprep6', 'position': 'Serve 2', 'day': 'Saturday', 'time': '10:00am - 12:00pm'}
    ]},
    {'name': 'Saturday Brunch Clean',
     'shifts': [
        {'shift_id': 'satbrunchclean1', 'position': 'Clean 1', 'day': 'Saturday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'satbrunchclean2', 'position': 'Clean 2', 'day': 'Saturday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'satbrunchclean3', 'position': 'Clean 3', 'day': 'Saturday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'satbrunchclean4', 'position': 'Clean 4', 'day': 'Saturday', 'time': '12:00pm - 1:00pm'}
    ]},
    {'name': 'Saturday Dinner Prep',
     'shifts': [
        {'shift_id': 'satdinprep1', 'position': 'Prep 1', 'day': 'Saturday', 'time': '4:00pm - 6:00pm'},
        {'shift_id': 'satdinprep2', 'position': 'Prep 2', 'day': 'Saturday', 'time': '4:00pm - 6:00pm'},
        {'shift_id': 'satdinprep3', 'position': 'Prep 3', 'day': 'Saturday', 'time': '4:00pm - 6:00pm'},
        {'shift_id': 'satdinprep4', 'position': 'Prep 4', 'day': 'Saturday', 'time': '4:00pm - 6:00pm'}
    ]},
    {'name': 'Saturday Dinner Cook',
     'shifts': [
        {'shift_id': 'satdincook1', 'position': 'Cook 1', 'day': 'Saturday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'satdincook2', 'position': 'Cook 2', 'day': 'Saturday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'satdincook3', 'position': 'Cook 3', 'day': 'Saturday', 'time': '6:00pm - 8:00pm'},
        {'shift_id': 'satdincook4', 'position': 'Cook 4', 'day': 'Saturday', 'time': '6:00pm - 8:00pm'}
    ]},
    {'name': 'Saturday Dinner Serve',
     'shifts': [
        {'shift_id': 'satdinserve1', 'position': 'Serve 1', 'day': 'Saturday', 'time': '7:00pm - 9:00pm'},
        {'shift_id': 'satdinserve2', 'position': 'Serve 2', 'day': 'Saturday', 'time': '7:00pm - 9:00pm'}
    ]},
    {'name': 'Saturday Dinner Clean',
     'shifts': [
        {'shift_id': 'satdinclean1', 'position': 'Clean 1', 'day': 'Saturday', 'time': '8:00pm - 9:30pm'},
        {'shift_id': 'satdinclean2', 'position': 'Clean 2', 'day': 'Saturday', 'time': '8:00pm - 9:30pm'},
        {'shift_id': 'satdinclean3', 'position': 'Clean 3', 'day': 'Saturday', 'time': '8:00pm - 9:30pm'},
        {'shift_id': 'satdinclean4', 'position': 'Clean 4', 'day': 'Saturday', 'time': '8:00pm - 9:30pm'}
    ]},
    {'name': 'Sunday Brunch, Prep and Serve',
     'shifts': [
        {'shift_id': 'sunbrunchprep1', 'position': 'Prep 1', 'day': 'Sunday', 'time': '8:00am - 10:00am'},
        {'shift_id': 'sunbrunchprep2', 'position': 'Prep 2', 'day': 'Sunday', 'time': '8:00am - 10:00am'},
        {'shift_id': 'sunbrunchprep3', 'position': 'Prep 3', 'day': 'Sunday', 'time': '8:00am - 10:00am'},
        {'shift_id': 'sunbrunchprep4', 'position': 'Prep 1', 'day': 'Sunday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'sunbrunchprep5', 'position': 'Prep 2', 'day': 'Sunday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'sunbrunchprep6', 'position': 'Prep 3', 'day': 'Sunday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'sunbrunchserv1', 'position': 'Serve 1', 'day': 'Sunday', 'time': '10:00am - 12:00pm'},
        {'shift_id': 'sunbrunchserv2', 'position': 'Serve 2', 'day': 'Sunday', 'time': '10:00am - 12:00pm'}
    ]},
    {'name': 'Sunday Brunch Clean',
     'shifts': [
        {'shift_id': 'sunbrunchclean1', 'position': 'Clean 1', 'day': 'Sunday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'sunbrunchclean2', 'position': 'Clean 2', 'day': 'Sunday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'sunbrunchclean3', 'position': 'Clean 3', 'day': 'Sunday', 'time': '12:00pm - 1:00pm'},
        {'shift_id': 'sunbrunchclean4', 'position': 'Clean 4', 'day': 'Sunday', 'time': '12:00pm - 1:00pm'}
    ]},
    {'name': 'Sunday Cleanup',
     'shifts': [
        {'shift_id': 'sunclean1', 'position': 'Cleanup 1', 'day': 'Sunday', 'time': '12:00pm - 2:00pm'},
        {'shift_id': 'sunclean2', 'position': 'Cleanup 2', 'day': 'Sunday', 'time': '12:00pm - 2:00pm'},
        {'shift_id': 'sunclean3', 'position': 'Cleanup 3', 'day': 'Sunday', 'time': '12:00pm - 2:00pm'},
        {'shift_id': 'sunclean4', 'position': 'Cleanup 4', 'day': 'Sunday', 'time': '12:00pm - 2:00pm'},
    ]},
    {'name': 'Overnight Cleanup (selecting this shift means staying over Sunday night to clean) *',
     'shifts': [
        {'shift_id': 'sunovernightclean1', 'position': 'Overnight Cleanup 1', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
        {'shift_id': 'sunovernightclean2', 'position': 'Overnight Cleanup 2', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
        {'shift_id': 'sunovernightclean3', 'position': 'Overnight Cleanup 3', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
        {'shift_id': 'sunovernightclean4', 'position': 'Overnight Cleanup 4', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
        {'shift_id': 'sunovernightclean5', 'position': 'Overnight Cleanup 5', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
        {'shift_id': 'sunovernightclean6', 'position': 'Overnight Cleanup 6', 'day': 'Sunday', 'time': '2:00pm - 10:00am', 'code': 'sc'},
    ]},
]


def get(name, default=None):
    "Get the value of a variable in the settings module scope."
    return globals().get(name, default)
