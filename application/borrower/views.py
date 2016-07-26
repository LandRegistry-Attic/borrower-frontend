from flask import Blueprint, render_template, Response, request, session, redirect, url_for
from application import config
import logging

LOGGER = logging.getLogger(__name__)

borrower_landing = Blueprint('borrower_landing', __name__,
                             template_folder='/templates',
                             static_folder='static')


@borrower_landing.route('/how-to-proceed', methods=['POST'])
def verified():
    return render_template('howtoproceed.html')


@borrower_landing.route('/')
def home():
    return render_template("start.html")


@borrower_landing.route('/start')
def start():
    if config.VERIFY:
        return redirect(url_for('borrower_landing.identity_verified'), code=307)
    else:
        return redirect(url_for('searchdeed.search_deed_main'), code=307)


@borrower_landing.route('/identity-verified', methods=['GET'])
def identity_verified():
    if 'deed_token' not in session:
        return Response('Unauthenticated', 401, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
    else:
        return render_template("identity-verified.html")


@borrower_landing.route('/verify', methods=['POST'])
def verify_identity():
    if 'Pid' in request.headers:
        verify_pid = request.headers.get('Pid')
        result = get_borrower_details(verify_pid)
        if result is not None:
            session['deed_token'] = result['deed_token']
            session['phone_number'] = result['phone_number']
            session['borrower_token'] = result['borrower_token']
        else:
            # Verify has worked, a match was made, but PID cannot now be found. Application fault.
            LOGGER.error("verify-PID-not-found")
            return redirect('/server-error', code=302)
        return redirect(url_for('borrower_landing.identity_verified'), code=302)
    else:
        if 'Verify-response-status' in request.headers:
            # Verify has worked, but an error has occurred, depending on status decide what to do
            if "no-match" in request.headers.get('Verify-response-status'):
                # no-match - Basic no match
                LOGGER.warn("verify-no-match")
                return redirect(url_for('borrower_landing.verify_no_match'), code=302)
            elif "NoAuthnContext" in request.headers.get('Verify-response-status'):
                # NoAuthnContext - No authentication context (this is when the user cancels the process)
                LOGGER.warn("verify-NoAuthnContext")
                return redirect(url_for('borrower_landing.verify_error'), code=302)
            elif "AuthnFailed" in request.headers.get('Verify-response-status'):
                # AuthnFailed - Authentication failed
                LOGGER.warn("verify-AuthnFailed")
                return redirect(url_for('borrower_landing.verify_error'), code=302)
            elif "Requester" in request.headers.get('Verify-response-status'):
                # Requester - Requester error (this is when the request is invalid)
                LOGGER.warn("verify-Requester")
                return redirect(url_for('borrower_landing.verify_error'), code=302)
            else:
                # Catch unknown error
                LOGGER.warn("verify-error-unknown")
                return redirect(url_for('borrower_landing.verify_error'), code=302)
        else:
            # No PID and No Verify-response-status - This should never happen
            LOGGER.error("no-pid-no-status")
            return redirect('/server-error', code=302)


@borrower_landing.route('/verify-error', methods=['GET'])
def verify_error():
    return render_template('verify-error.html')


@borrower_landing.route('/verify-no-match', methods=['GET'])
def verify_no_match():
    return render_template('verify-no-match.html')


def get_borrower_details(verify_pid):
    deed_api_client = getattr(borrower_landing, 'deed_api_client')
    return deed_api_client.get_borrower_details_by_verify_pid(verify_pid)
