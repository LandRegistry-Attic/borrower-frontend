from application.service import akuma
from copy import deepcopy


class Akuma:

    @staticmethod
    def do_check(json_payload, check_type, borrower_token, deed_token):

        akuma_payload = deepcopy(json_payload)

        akuma_payload['title_no'] = str(json_payload['deed']['title_number'])
        akuma_payload['borrower_token'] = borrower_token
        akuma_payload['deed_token'] = str(deed_token)

        payload = {
            "service": "digital mortgage",
            "activity": check_type,
            "payload": akuma_payload
        }

        akuma_client = akuma.make_akuma_client()

        check_result = akuma_client.perform_check(payload)

        return check_result
