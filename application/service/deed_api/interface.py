class DeedApiInterface(object):  # pragma: no cover
    def __init__(self, implementation):
        self.implementation = implementation

    def get_deed(self, deed_reference):
        return self.implementation.get_deed(deed_reference)

    def validate_borrower(self, payload):
            return self.implementation.validate_borrower(payload)

    def request_auth_code(self, deed_reference, borrower_token):
        return self.implementation.request_auth_code(deed_reference, borrower_token)

    def verify_auth_code(self, deed_reference, borrower_token, authentication_code):
        return self.implementation.verify_auth_code(deed_reference, borrower_token, authentication_code)

    def get_borrower_details_by_verify_pid(self, verify_pid):
        return self.implementation.get_borrower_details_by_verify_pid(verify_pid)

    def check_service_health(self):
        return self.implementation.check_health()

    def send_naa(self, borrower_id):
        return self.implementation.send_naa(borrower_id)

    def get_conveyancer_for_deed(self, deed_token):
        return self.implementation.get_conveyancer_for_deed(deed_token)['result']