from flask import Blueprint, render_template, Response, request, session, redirect
from application import config

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
        return redirect('/identity-verified', code=307)
    else:
        return redirect('/borrower-reference', code=307)


@borrower_landing.route('/identity-verified', methods=['GET'])
def identity_verified():
    if 'deed_token' not in session:
        return Response('Unauthenticated', 401, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
    else:
        return render_template("identity-verified.html")


@borrower_landing.route('/borrower-naa', methods=['GET'])
def show_network_agreement():
        return render_template("borrower-naa.html")


@borrower_landing.route('/confirm-naa', methods=['GET', 'POST'])
def confirm_network_agreement():
        form = request.form

        if 'validate' in form:
            form.error = validate_naa(form)
            if form.error is None:
                dob = form["dob-day"] + "/" + form["dob-month"] + "/" + form["dob-year"]
                result = validate_borrower(form['borrower_token'], dob)
                if result is not None:
                    session['deed_token'] = result['deed_token']
                    session['phone_number'] = result['phone_number']
                    session['borrower_token'] = form['borrower_token']
                    return redirect('/how-to-proceed', code=307)
                else:
                    session['error'] = "True"
                    return redirect('/borrower-reference', code=307)

        return render_template('enterdob.html', form=form)
        return render_template("confirm-borrower-naa.html")


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


def validate_naa(form):
    error = None
    try:

        if dob_date >= present:
            raise Exception("Date cannot be in the future")

    except:
        error = "You must agree to these Terms and Conditions to proceed"

    return error
