from flask import Blueprint, render_template, Response, request, session, redirect
from application import config

borrower_landing = Blueprint('borrower_landing', __name__,
                             template_folder='/templates',
                             static_folder='static')


@borrower_landing.route('/how-to-proceed', methods=['POST', 'GET'])
def verified():
    return render_template('howtoproceed.html')


@borrower_landing.route('/')
def home():
    return render_template("start.html")


@borrower_landing.route('/start')
def start():
    if config.VERIFY:
        return redirect('/identity-verified', code=307)
    else:
        return redirect('/borrower-reference', code=307)


@borrower_landing.route('/identity-verified', methods=['GET'])
def identity_verified():
    if 'deed_token' not in session:
        return Response('Unauthenticated', 401, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
    else:
        return render_template("identity-verified.html")


@borrower_landing.route('/confirm-naa', methods=['GET', 'POST'])
def confirm_network_agreement():
    if request.method == "GET":
        return render_template('confirm-borrower-naa.html')
    elif request.method == "POST":
        if 'accept-naa' in request.form:
            session['agreement_naa'] = "accepted"
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
        else:
            return redirect('/verify-error', code=302)

        return redirect('/identity-verified', code=302)
    else:
        return redirect('/verify-error', code=302)


@borrower_landing.route('/verify-error', methods=['GET'])
def verify_error():
    return render_template('verify-error.html')


def get_borrower_details(verify_pid):
    deed_api_client = getattr(borrower_landing, 'deed_api_client')
    return deed_api_client.get_borrower_details_by_verify_pid(verify_pid)
