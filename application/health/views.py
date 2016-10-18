from flask import Blueprint, render_template, jsonify
import requests
from application import config
from flask.ext.api import status

health = Blueprint('health', __name__,
                   template_folder='/templates',
                   static_folder='static')


webseal_headers = {
    "Content-Type": "application/json",
    "Iv-User-L": "CN=DigitalMortgage%20DigitalMortgage,OU=devices,O=Land%20Registry%20Internal,O=*,C=gb"
}


@health.route('/')
def health_main():
    return render_template('health.html')

"""
Connect to the health endpoint of deed-api, which will return
a list of services that it can or cannot connect to.

TODO: security check on each service? As anyone can call this get method.

@return A JSON object that contains a list of services.
        For each service, it will either have:
        200: OK
        500:
"""
@health.route('/service-check')
def service_check_routes():

    # Attempt to connect to deed-api which will attempt to connect to all
    # other services that are related to it.
    service_response = ""
    status_code = 500 # default
    service_json = ""

    try:
        service_response = requests.get(config.DEED_API_BASE_HOST + '/health/service-check',
                                        headers=webseal_headers)
        status_code = service_response.status_code
        service_json = service_response.json()

    except requests.exceptions.RequestException as e:
        # A RequestException resolves the error that occurs when a connection cant be established
        status_code = 500

    if status_code != 200:
        # We either have a differing status code, add an error for this service
        # This would imply that we were not able to connect to deed-api
        service_json = {
            "services" :
            [{
                "status_code": str(status_code),
                "service_from": "borrower-frontend",
                "service_to": "deed-api",
                "service_message": "Error: Could not connect"
            }]
        }

    # Return the json object containing the status of each service
    return jsonify(service_json)
