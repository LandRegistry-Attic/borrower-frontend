import logging
import datetime
from flask import Blueprint, render_template, request, redirect, session, url_for, jsonify
from flask.ext.api import status
from werkzeug import exceptions

from application.deed.searchdeed.address_utils import format_address_string
from application.akuma.service import Akuma

LOGGER = logging.getLogger(__name__)

searchdeed = Blueprint('searchdeed', __name__,
                       template_folder='/templates',
                       static_folder='static')


@searchdeed.route('/borrower-reference', methods=['GET', 'POST'])
def search_deed_main():
    if session.get("error"):
        session.pop("error")
        return render_template('searchdeed.html', error=True)
    else:
        session.clear()
        session.permanent = True
        return render_template('searchdeed.html', error=None)


@searchdeed.route('/date-of-birth', methods=['POST'])
def enter_dob():
    form = request.form
    form.current_year = str(datetime.datetime.now().year)

    if 'validate' in form:
        form.error = validate_dob(form)
        borrower_token = form['borrower_token'].upper()
        if form.error is None:
            dob = form["dob-day"] + "/" + form["dob-month"] + "/" + form["dob-year"]
            result = validate_borrower(borrower_token, dob)
            if result is not None:
                session['deed_token'] = result['deed_token']
                session['phone_number'] = result['phone_number']
                session['borrower_token'] = borrower_token
                return redirect('/how-to-proceed', code=307)
            else:
                session['error'] = "True"
                return redirect('/borrower-reference', code=307)

    return render_template('enterdob.html', form=form)


@searchdeed.route('/mortgage-deed', methods=['GET'])
def search_deed_search():
    if 'deed_token' not in session:
        return redirect('/session-ended', code=302)

    if ('agreement_naa' not in session) or (session['agreement_naa'] != 'accepted'):
        return redirect('/how-to-proceed', code=307)

    response = do_search_deed_search()
    return response, status.HTTP_200_OK


@searchdeed.route('/enter-authentication-code', methods=['GET', 'POST'])
def show_authentication_code_page():
    if 'deed_token' not in session:
        return redirect('/session-ended', code=302)

    if request.args.get('error', False):
        return render_template('authentication-code.html', error=True)

    send_auth_code()

    return render_template('authentication-code.html')


@searchdeed.route('/signing-mortgage-deed', methods=['POST'])
def show_confirming_deed_page():
    auth_code = request.form['auth_code']

    if auth_code is None or auth_code == '':
        return render_template('authentication-code.html', error=True)

    return render_template('signing-mortgage-deed.html', auth_code=request.form['auth_code'])


@searchdeed.route('/verify-auth-code', methods=['POST'])
def verify_auth_code(auth_code=None):
    if 'deed_token' not in session:
        return jsonify({'error': True, 'redirect': 'session-ended'})

    if request.form['auth_code']:
        auth_code = request.form['auth_code']

    try:
        deed_api_client = getattr(searchdeed, 'deed_api_client')
        response = deed_api_client.verify_auth_code(str(session.get('deed_token')),
                                                    str(session.get('borrower_token')),
                                                    auth_code)

        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return_val = jsonify(
                {'error': True, 'redirect': 'enter-authentication-code?error=True'})
        elif response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE \
                or response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return_val = jsonify(
                {'error': True, 'redirect': 'service-unavailable/deed-not-confirmed'})
        else:
            return_val = jsonify({'error': False})

        LOGGER.error("Status code: %s for auth code %s was returned" % (str(response.status_code), (str(auth_code))))
        return return_val
    except:
        session['service_timeout_at_verify_code'] = True
        raise exceptions.ServiceUnavailable


@searchdeed.route('/verify-auth-code-no-js', methods=['POST'])
def verify_auth_code_no_js():
    if 'deed_token' not in session:
        return redirect('/session-ended', code=302)

    auth_code = request.form['auth_code']

    if auth_code is None or auth_code == '':
        return redirect(url_for('searchdeed.show_authentication_code_page', error=True))

    response = verify_auth_code(auth_code)

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        return_val = redirect(url_for('authentication-code.html', error=True))
    elif response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE \
            or response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        return_val = redirect(url_for('searchdeed.show_internal_server_error_page'))
    elif response.status_code == status.HTTP_200_OK:
        return_val = redirect(url_for('searchdeed.show_final_page'))

    LOGGER.error("Status code: %s for auth code %s was returned" % (str(response.status_code), (str(auth_code))))
    return return_val


@searchdeed.route('/confirm-mortgage-is-signed', methods=['GET'])
def confirm_mortgage_is_signed():
    if deed_signed():
        return jsonify({'result': True, 'redirect': 'finished'})
    else:
        return jsonify({'result': False})


def send_auth_code():
    deed_api_client = getattr(searchdeed, 'deed_api_client')
    response = deed_api_client.request_auth_code(str(session.get('deed_token')), str(session.get('borrower_token')))

    if response.status_code != status.HTTP_200_OK:
        session['service_timeout_at_send_code'] = True
        raise exceptions.ServiceUnavailable


@searchdeed.route('/finished', methods=['GET', 'POST'])
def show_final_page():
    session.clear()
    return render_template('finished.html')


@searchdeed.route('/session-ended', methods=['GET'])
def session_ended():
    return render_template('session-ended.html')


@searchdeed.route('/service-unavailable/deed-not-confirmed')
def show_internal_server_error_page():
    return render_template('deed-not-confirmed.html')


@searchdeed.errorhandler(status.HTTP_503_SERVICE_UNAVAILABLE)
def internal_server_error(e):
    return redirect(url_for('searchdeed.show_internal_server_error_page'))


def validate_dob(form):
    error = None
    try:
        present = datetime.datetime.now()

        day = int(form["dob-day"])
        month = int(form["dob-month"])
        year = int(form["dob-year"])

        dob_date = datetime.datetime(year, month, day)

        if dob_date >= present:
            raise Exception("Date cannot be in the future")

    except:
        error = "Please enter a valid date of birth"

    return error


def validate_borrower(borrower_token, dob):
    if borrower_token is not None and borrower_token != '':
        payload = {
            "borrower_token": borrower_token,
            "dob": str(dob)
        }
        deed_api_client = getattr(searchdeed, 'deed_api_client')
        result = deed_api_client.validate_borrower(payload)
        return result


def do_search_deed_search():
    deed_data = lookup_deed(session['deed_token'])
    if deed_data is not None:
        if 'effective_date' in deed_data["deed"]:
            temp = datetime.datetime.strptime(deed_data["deed"]["effective_date"], "%Y-%m-%d %H:%M:%S")
            deed_data["deed"]["effective_date"] = temp.strftime("%d/%m/%Y")

        # Akuma Check
        Akuma.do_check(deed_data, "borrower view", session['borrower_token'], session['deed_token'])

        deed_data["deed"]["property_address"] = format_address_string(deed_data["deed"]["property_address"])
        if deed_signed():
            response = render_template('viewdeed.html', deed_data=deed_data, signed=True)
        else:
            response = render_template('viewdeed.html', deed_data=deed_data, signed=False)
    else:
        return render_template('searchdeed.html', error=True)

    return response


def lookup_deed(deed_reference):
    if deed_reference is not None and deed_reference != '':
        deed_api_client = getattr(searchdeed, 'deed_api_client')
        deed_data = deed_api_client.get_deed(str(deed_reference))
    else:
        deed_data = None

    return deed_data


def deed_signed():
    deed_data = lookup_deed(session['deed_token'])
    if deed_data is not None:
        for borrower in deed_data['deed']['borrowers']:
            if 'signature' in borrower and borrower['token'] == session.get('borrower_token'):
                return True
