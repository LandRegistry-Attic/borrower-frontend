from flask import session
import inflect
import string

# True if all borrowers have signed.
def check_all_signed(deed_data):
    borrowers = no_of_borrowers(deed_data)
    signatures = 0
    if deed_data:
        for borrower in deed_data['deed']['borrowers']:
            if 'signature' in borrower:
                signatures += 1
    return signatures == borrowers


# counts the number of borrowers and returns
def no_of_borrowers(deed_data):
    borrower_count = 0
    if deed_data:
        for borrower in deed_data['deed']['borrowers']:
            borrower_count += 1
    return borrower_count


def get_borrower_information(deed_data):
    p = inflect.engine()

    borrowers = {
        'borrowers':
            [

            ]
    }

    if deed_data is not None:
        for idx, borrower in enumerate(deed_data['deed']['borrowers']):
            forename = borrower['forename']
            middle_name = borrower['middle_name'] if 'middle_name' in borrower else ''
            surname = borrower['surname']

            if borrower['token'] == session['borrower_token']:
                borrowers['borrowers'].append({'name': forename + ' ' + middle_name + ' ' + surname,
                                               'order': 'First',
                                               'signed': True if 'signature' in borrower else False})
            else:
                borrowers['borrowers'].append({'name': forename + ' ' + middle_name + ' ' + surname,
                                               'order': string.capwords(p.ordinal(p.number_to_words(idx + 2))),
                                               'signed': True if 'signature' in borrower else False})

    return borrowers
