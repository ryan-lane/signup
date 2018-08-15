import copy
import logging
import base64

import requests
from flask import request
from flask import jsonify
from pynamodb.exceptions import PutError, DeleteError

from signup import app
from signup.models.shifts import Shift


@app.route('/v1/shift/<shift_id>', methods=['GET'])
def get_shift(shift_id):
    try:
        _shift = Shift.get(shift_id)
    except Shift.DoesNotExist:
        _shift = None
    shifts = copy.deepcopy(app.config['SHIFTS'])
    for shift_item in shifts:
        for shift in shift_item['shifts']:
            if _shift and _shift.shift_id == shift['shift_id']:
                shift['name'] = _shift.name
                shift['email'] = _shift.email
                return jsonify({'shift': shift})
            elif shift_id == shift['shift_id']:
                return jsonify({'shift': shift})
    return jsonify({'error': 'Shift does not exist.'}), 404


@app.route('/v1/shift/<shift_id>', methods=['PUT'])
def put_shift(shift_id):
    #return jsonify({'error': 'Signup is shut down.'}), 403
    try:
        shift = Shift.get(shift_id)
        old_email = shift.email
    except Shift.DoesNotExist:
        old_email = None
    shift_data = None
    for shift_item in app.config['SHIFTS']:
        for _shift in shift_item['shifts']:
            if _shift['shift_id'] == shift_id:
                shift_data = _shift
                break
    if shift_data is None:
        return jsonify({'error': 'Shift does not exist.'}), 404
    shift_code = shift_data.get('code', 'default')
    body = base64.b64decode(app.config['TICKETS_EMAIL_BODY'])
    code = app.config['TICKETS_CODE'].get(shift_code)
    data = request.get_json()
    shift = Shift(
        shift_id=shift_id,
        name=data['name'],
        email=data['email']
    )
    if data.get('change', False):
        shift.save()
    else:
        try:
            shift.save(email__null=True)
        except PutError:
            return jsonify({'error': 'Shift already taken.'}), 400
    try:
        ret = requests.post(
            '{0}/messages'.format(app.config['MAILGUN_URL']),
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'from': app.config['MAILGUN_FROM_ADDRESS'],
                'to': shift.email,
                'subject': app.config['TICKETS_EMAIL_SUBJECT'],
                'text': body.format(
                    code=code,
                    position=shift_data['position'],
                    day=shift_data['day'],
                    time=shift_data['time']
                )
            }
        )
        msg = 'Sent email to {0} via mailgun. Status: {1} Return body: {2}'
        logging.info(
            msg.format(
                shift.email,
                ret.status_code,
                ret.text
            )
        )
    except requests.exceptions.RequestException:
        logging.exception('Failed to send email to {0}.'.format(shift.email))
    if old_email:
        body = base64.b64decode(app.config['TICKETS_EMAIL_BODY_TAKEN'])
        try:
            ret = requests.post(
                '{0}/messages'.format(app.config['MAILGUN_URL']),
                auth=('api', app.config['MAILGUN_API_KEY']),
                data={
                    'from': app.config['MAILGUN_FROM_ADDRESS'],
                    'to': old_email,
                    'subject': app.config['TICKETS_EMAIL_SUBJECT_TAKEN'],
                    'text': body.format(
                        name=shift.name,
                        email=shift.email,
                        position=shift_data['position'],
                        day=shift_data['day'],
                        time=shift_data['time']
                    )
                }
            )
            msg = 'Sent email to {0} via mailgun. Status: {1} Return body: {2}'
            logging.info(
                msg.format(
                    old_email,
                    ret.status_code,
                    ret.text
                )
            )
        except requests.exceptions.RequestException:
            logging.exception(
                'Failed to send email to {0}.'.format(old_email)
            )
    body = base64.b64decode(app.config['CHANGELOG_BODY'])
    try:
        ret = requests.post(
            '{0}/messages'.format(app.config['MAILGUN_URL']),
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'from': app.config['MAILGUN_FROM_ADDRESS'],
                'to': app.config['CHANGELOG_ADDRESS'],
                'subject': app.config['CHANGELOG_SUBJECT'],
                'text': body.format(
                    name=shift.name,
                    email=shift.email,
                    position=shift_data['position'],
                    day=shift_data['day'],
                    time=shift_data['time']
                )
            }
        )
    except requests.exceptions.RequestException:
        logging.exception(
            'Failed to send email to {0}.'.format(old_email)
        )
    msg = 'Sent email to {0} via mailgun. Status: {1} Return body: {2}'
    logging.info(
        msg.format(
            app.config['CHANGELOG_ADDRESS'],
            ret.status_code,
            ret.text
        )
    )
    return jsonify({
        'shift': {
            'shift_id': shift.shift_id,
            'name': shift.name,
            'email': shift.email
        }
    })


@app.route('/v1/shift/<shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    #return jsonify({'error': 'Signup is shut down.'}), 403
    shift_data = None
    for shift_item in app.config['SHIFTS']:
        for _shift in shift_item['shifts']:
            if _shift['shift_id'] == shift_id:
                shift_data = _shift
                break
    if shift_data is None:
        return jsonify({'error': 'Shift does not exist.'}), 404
    try:
        _shift = Shift.get(shift_id)
    except Shift.DoesNotExist:
        return jsonify({'error': 'Shift not found or shift already removed.'})
    name = _shift.name
    email = _shift.email
    try:
        _shift.delete()
    except DeleteError:
        return jsonify({'error': 'Failed to remove shift.'})
    body = base64.b64decode(app.config['TICKETS_EMAIL_BODY_REMOVED'])
    try:
        ret = requests.post(
            '{0}/messages'.format(app.config['MAILGUN_URL']),
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'from': app.config['MAILGUN_FROM_ADDRESS'],
                'to': email,
                'subject': app.config['TICKETS_EMAIL_SUBJECT_REMOVED'],
                'text': body.format(
                    position=shift_data['position'],
                    day=shift_data['day'],
                    time=shift_data['time']
                )
            }
        )
        msg = 'Sent email to {0} via mailgun. Status: {1} Return body: {2}'
        logging.info(
            msg.format(
                email,
                ret.status_code,
                ret.text
            )
        )
    except requests.exceptions.RequestException:
        logging.exception(
            'Failed to send email to {0}.'.format(email)
        )
    body = base64.b64decode(app.config['CHANGELOG_BODY_REMOVED'])
    try:
        ret = requests.post(
            '{0}/messages'.format(app.config['MAILGUN_URL']),
            auth=('api', app.config['MAILGUN_API_KEY']),
            data={
                'from': app.config['MAILGUN_FROM_ADDRESS'],
                'to': app.config['CHANGELOG_ADDRESS'],
                'subject': app.config['CHANGELOG_SUBJECT'],
                'text': body.format(
                    name=name,
                    email=email,
                    position=shift_data['position'],
                    day=shift_data['day'],
                    time=shift_data['time']
                )
            }
        )
    except requests.exceptions.RequestException:
        logging.exception(
            'Failed to send email to {0}.'.format(email)
        )
    return jsonify({
        'shift': {}
    })


@app.route('/v1/shifts', methods=['GET'])
def get_shifts():
    shifts = copy.deepcopy(app.config['SHIFTS'])
    _shifts = {}
    for _shift in Shift.scan():
        _shifts[_shift.shift_id] = {'name': _shift.name, 'email': _shift.email}
    for shift_item in shifts:
        for shift in shift_item['shifts']:
            shift_id = shift['shift_id']
            if shift_id in _shifts:
                shift.update(_shifts[shift_id])
    return jsonify({'shifts': shifts})
