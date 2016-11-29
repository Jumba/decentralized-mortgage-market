from market.models import DatabaseModel


class Profile(DatabaseModel):
    _type = 'profile'

    def __init__(self, first_name, last_name, email, iban, phone_number):
        assert isinstance(first_name, str)
        assert isinstance(last_name, str)
        assert isinstance(email, str)
        assert isinstance(iban, str)
        assert isinstance(phone_number, str)

        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._iban = iban
        self._phonenumber = phone_number


class BorrowersProfile(Profile):
    _type = 'borrowers_profile'

    def __init__(self, first_name, last_name, email, iban, phone_number, current_postal_code, current_house_number, document_list):
        super(BorrowersProfile, self).__init__(first_name, last_name, email, iban, phone_number)

        assert isinstance(current_postal_code, str)
        assert isinstance(current_house_number, str)
        assert isinstance(document_list, list)

        self._current_postal_code = current_postal_code
        self._current_house_number = current_house_number
        self._document_list = document_list
