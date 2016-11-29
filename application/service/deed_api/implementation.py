import requests
from application import config
from flask.ext.api import status

webseal_headers = {
    "Content-Type": "application/json",
    "Iv-User-L": "CN=DigitalMortgage%20DigitalMortgage,OU=devices,O=Land%20Registry%20Internal,O=*,C=gb"
}


def get_deed(deed_reference):  # pragma: no cover
    data = None
    resp = requests.get(config.DEED_API_BASE_HOST + '/deed/' +
                        str(deed_reference),
                        headers=webseal_headers)

    if resp.status_code == status.HTTP_200_OK:
        data = resp.json()

    return data


def send_naa(borrower_id):
    resp = requests.post(config.DEED_API_BASE_HOST + '/naa/accept/' +
                         str(borrower_id),
                         headers=webseal_headers)
    return resp


def validate_borrower(payload):  # pragma: no cover
    resp = requests.post(config.DEED_API_BASE_HOST +
                         '/borrower/validate', json=payload,
                         headers=webseal_headers)
    if resp.status_code == status.HTTP_200_OK:
        return resp.json()


def request_auth_code(deed_reference, borrower_token):  # pragma: no cover
    payload = {"borrower_token": borrower_token}
    response = requests.post(config.DEED_API_BASE_HOST +
                             '/deed/' + deed_reference + '/request-auth-code', json=payload, headers=webseal_headers)
    return response


def verify_auth_code(deed_reference, borrower_token, authentication_code):  # pragma: no cover
    payload = {"borrower_token": borrower_token, "authentication_code": authentication_code}
    response = requests.post(config.DEED_API_BASE_HOST +
                             '/deed/' + deed_reference + '/verify-auth-code', json=payload, headers=webseal_headers)
    return response


def get_borrower_details_by_verify_pid(verify_pid):  # pragma: no cover
    response = requests.get(config.DEED_API_BASE_HOST +
                            "/borrower/verify/pid/" + str(verify_pid), headers=webseal_headers)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        return None


def check_health():
    service_response = requests.get(config.DEED_API_BASE_HOST + '/health/service-check')

    return service_response


def get_conveyancer_for_deed(deed_reference):  # pragma: no cover
    data = None
    resp = requests.get(config.DEED_API_BASE_HOST + '/deed/' + str(deed_reference) + '/conveyancer-name',
                        headers=webseal_headers)
    if resp.status_code == status.HTTP_200_OK:
        data = resp.json()

    return data
