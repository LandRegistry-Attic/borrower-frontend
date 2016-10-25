from flask import Blueprint, render_template, jsonify
import logging
from application.service.deed_api import make_deed_api_client

LOGGER = logging.getLogger(__name__)


health = Blueprint('health', __name__,
                   template_folder='/templates',
                   static_folder='static')


@health.route('/')
def health_main():
    return render_template('health.html')


@health.route('/service-check')
def service_check_routes():

    # Attempt to connect to deed-api which will attempt to connect to all
    # other services that are related to it.
    service_response = ""
    service_list = ""

    service_dict = {
        "status_code": 500,
        "service_from": "borrower frontend",
        "service_to": "deed-api",
        "service_message": "Successfully connected"
    }

    try:
        # Create the interface that allows us to call the deed api's health route
        # and retrieve the response
        deed_interface = make_deed_api_client()
        service_response = deed_interface.check_service_health()
        
        status_code = service_response.status_code
        service_list = service_response.json()

        # Add the success dict for Borrower Front End to the list of services
        # If there was an exception it would not get to this point
        service_dict["status_code"] = status_code
        service_list["services"].append(service_dict)

    # If a 500 error is reported, it will be far easier to determine the cause by
    # throwing an exception, rather than by getting an "unexpected error" output
    except Exception as e:
        # A RequestException resolves the error that occurs when a connection cant be established
        # and the ValueError/TypeError exception may occur if the dict string / object is malformed
        LOGGER.error('An exception has occurred in the service-check route: %s', (e,), exc_info=True)

        # We either have a differing status code, add an error for this service
        # This would imply that we were not able to connect to deed-api
        service_dict["status_code"] = 500
        service_dict["service_message"] = "Error: Could not connect"

        service_list = {
            "services":
            [
                service_dict
            ]
        }

    # Return the dict object containing the status of each service
    return jsonify(service_list)
