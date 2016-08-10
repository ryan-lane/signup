import copy
import logging

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
    for shift_name, shift_section in shifts.items():
        for shift in shift_section:
            if _shift and _shift.shift_id == shift_id:
                shift['name'] = _shift.name
                shift['email'] = _shift.email
            return jsonify({'shift': shift})
    return jsonify({'error': 'Shift does not exist.'}), 404


@app.route('/v1/shift/<shift_id>', methods=['PUT'])
def put_shift(shift_id):
    shift_data = None
    for shift_name, shift_section in app.config['SHIFTS'].items():
        for _shift in shift_section:
            if _shift['shift_id'] == shift_id:
                shift_data = _shift
                break
    if shift_data is None:
        return jsonify({'error': 'Shift does not exist.'}), 404
    shift_code = shift_data.get('code', 'default')
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
                'text': app.config['TICKETS_EMAIL_BODY'].format(
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
    return jsonify({
        'shift': {
            'shift_id': shift.shift_id,
            'name': shift.name,
            'email': shift.email
        }
    })


@app.route('/v1/shift/<shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    shift_data = None
    for shift_name, shift_section in app.config['SHIFTS'].items():
        for _shift in shift_section:
            if _shift['shift_id'] == shift_id:
                shift_data = _shift
                break
    if shift_data is None:
        return jsonify({'error': 'Shift does not exist.'}), 404
    try:
        _shift = Shift.get(shift_id)
    except Shift.DoesNotExist:
        return jsonify({'error': 'Shift not found or shift already removed.'})
    try:
        _shift.delete()
    except DeleteError:
        return jsonify({'error': 'Failed to remove shift.'})
    return jsonify({
        'shift': {}
    })


@app.route('/v1/shifts', methods=['GET'])
def get_shifts():
    shifts = copy.deepcopy(app.config['SHIFTS'])
    _shifts = {}
    for _shift in Shift.scan():
        _shifts[_shift.shift_id] = {'name': _shift.name, 'email': _shift.email}
    for shift_name, shift_section in shifts.items():
        for shift in shift_section:
            shift_id = shift['shift_id']
            if shift_id in _shifts:
                shift.update(_shifts[shift_id])
    return jsonify({'shifts': shifts})
