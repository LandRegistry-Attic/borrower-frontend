import inflect
import string
import hashlib


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


def get_ordered_borrowers(deed_data, signed_in_token):

    borrowers = []

    if deed_data:
        for idx, borrower in enumerate(deed_data['deed']['borrowers']):
            forename = borrower['forename'] + ' '
            middle_name = borrower['middle_name'] + ' ' if 'middle_name' in borrower else ''
            surname = borrower['surname']

            # Ensure logged in  borrower's index is 0 - at the top of the below created OrderedDict; so it appears
            # at the top of the 'How to proceed page'.
            borrowers.append({'borrower_name': forename + middle_name + surname,
                              'order': 0 if borrower['token'] == signed_in_token else idx + 1,
                              'signed': True if 'signature' in borrower else False})

    # Order the dict, so that the logged in borrower is at the top
    ordered_borrowers = sorted(borrowers, key=lambda k: k['order'])

    return ordered_borrowers


def inflect_ordered_borrowers(ordered_borrowers):

    p = inflect.engine()

    if ordered_borrowers:
        for idx, borrower in enumerate(ordered_borrowers):

            # Assuming we have four borrowers using the ordered dict from the get_ordered_borrowers function
            borrower['order'] = string.capwords(p.ordinal(p.number_to_words(idx + 1)))

    return ordered_borrowers


def get_signed_in_borrower(deed_data, borrower_token):
    result = ''
    if deed_data:
        for borrower in deed_data['deed']['borrowers']:
            if borrower['token'] == borrower_token:
                forename = borrower['forename'] + ' '
                middle_name = borrower['middle_name'] + ' ' if 'middle_name' in borrower else ''
                surname = borrower['surname']
                result = forename + middle_name + surname
    return result


def hash_for(data):
    hash_id = hashlib.sha256()
    hash_id.update(repr(data).encode('utf-8'))
    return hash_id.hexdigest()
