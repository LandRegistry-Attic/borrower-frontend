from application.service import akuma
from copy import deepcopy


class Akuma:

    @staticmethod
    def do_check(json_payload, check_type, borrower_token):

        akuma_payload = deepcopy(json_payload)

        akuma_payload['title_no'] = str(json_payload['deed']['title_number'])
        akuma_payload['borrower_token'] = borrower_token


        payload = {
            "service": "digital mortgage",
            "activity": check_type,
            "payload": akuma_payload
        }

        print(str(payload))

        akuma_client = akuma.make_akuma_client()

        check_result = akuma_client.perform_check(payload)

        return check_result
