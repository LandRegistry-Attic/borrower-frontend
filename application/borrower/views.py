from flask import Blueprint, render_template, Response, request, session, redirect, url_for
from application import config
from application.service.deed_api import make_deed_api_client
from application.deed.searchdeed.views import deed_signed, lookup_deed
from application.deed.searchdeed.borrower_utils import get_ordered_borrowers, inflect_ordered_borrowers
import logging

LOGGER = logging.getLogger(__name__)

borrower_landing = Blueprint('borrower_landing', __name__)


def get_conveyancer_for_deed():
    interface = make_deed_api_client()
    return interface.get_conveyancer_for_deed(session['deed_token'])


def get_inflected_borrower_data(deed_data):
    ordered_borrower_data = get_ordered_borrowers(deed_data, session['borrower_token'])
    return inflect_ordered_borrowers(ordered_borrower_data)


@borrower_landing.route('/how-to-proceed', methods=['POST', 'GET'])
def verified():
    conveyancer = get_conveyancer_for_deed()
    signed = deed_signed()
    deed_data = lookup_deed(session['deed_token'])
    inflected_borrower_data = get_inflected_borrower_data(deed_data)

    return render_template('howtoproceed.html', borrower_data=inflected_borrower_data, conveyancer=conveyancer, signed=signed)


@borrower_landing.route('/borrow-naa', methods=['POST', 'GET'])
def borrow_naa():
    return render_template('confirm-borrower-naa.html')


@borrower_landing.route('/')
def home():
    return render_template("start.html", verify=config.VERIFY)


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
        return redirect(url_for('borrower_landing.verified'), code=307)


@borrower_landing.route('/confirm-naa', methods=['GET', 'POST'])
def confirm_network_agreement():
    if request.method == "GET":
        return render_template('howtoproceed.html')
    elif request.method == "POST":
        if 'accept-naa' in request.form:
            session['agreement_naa'] = "accepted"
            borrower_id = session['borrower_id']
            interface = make_deed_api_client()
            result = interface.send_naa(borrower_id)
            if result.status_code == 500:
                LOGGER.warning("error- status code has returned as 500 and the audit has not been created")
                return redirect('/server-error')
            elif result.status_code == 200:
                LOGGER.info("success- status code has returned as 200 and the audit has been created")
                return redirect('/mortgage-deed', code=302)
        else:
            session['agreement_naa'] = "declined"
            return redirect('/how-to-proceed', code=307)


@borrower_landing.route('/verify', methods=['POST'])
def verify_identity():
    if 'Pid' in request.headers:
        verify_pid = request.headers.get('Pid')
        result = get_borrower_details(verify_pid)
        if result is not None:
            session['deed_token'] = result['deed_token']
            session['phone_number'] = result['phone_number']
            session['borrower_token'] = result['borrower_token']
            session['borrower_id'] = result['borrower_id']
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


@borrower_landing.route('/feedback', methods=['GET'])
def user_feedback():
    return render_template('user-feedback.html')


@borrower_landing.route('/get-pdf', methods=['POST'])
def get_pdf():
    deed_api_client = make_deed_api_client()
    deed_pdf = deed_api_client.get_deed(request.form["deed_id"], "application/pdf")

    if deed_pdf.status_code == 200:
        return deed_pdf
    else:
        return render_template('404.html')


def get_borrower_details(verify_pid):
    deed_api_client = getattr(borrower_landing, 'deed_api_client')
    return deed_api_client.get_borrower_details_by_verify_pid(verify_pid)
