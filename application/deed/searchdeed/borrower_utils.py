
# True if all borrowers have signed.
def check_all_signed(deed_data):
    borrowers = no_of_borrowers(deed_data)
    signatures = 0
    if deed_data is not None:
        for borrower in deed_data['deed']['borrowers']:
            if 'signature' in borrower:
                signatures += 1
    return signatures == borrowers


# counts the number of borrowers and returns
def no_of_borrowers(deed_data):
    borrower_count = 0
    if deed_data is not None:
        for borrower in deed_data['deed']['borrowers']:
            borrower_count += 1
    return borrower_count
