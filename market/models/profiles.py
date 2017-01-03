from market.models import DatabaseModel


class Profile(DatabaseModel):
    type = 'profile'

    def __init__(self, first_name, last_name, email, iban, phone_number):
        super(Profile, self).__init__()
        assert isinstance(first_name, unicode)
        assert isinstance(last_name, unicode)
        assert isinstance(email, str)
        assert isinstance(iban, str)
        assert isinstance(phone_number, str)

        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._iban = iban
        self._phone_number = phone_number

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def iban(self):
        return self._iban

    @property
    def phone_number(self):
        return self._phone_number

class BorrowersProfile(Profile):
    type = 'borrowers_profile'

    def __init__(self, first_name, last_name, email, iban, phone_number, current_postal_code, current_house_number, current_address, document_list):
        super(BorrowersProfile, self).__init__(first_name, last_name, email, iban, phone_number)

        assert isinstance(current_postal_code, str)
        assert isinstance(current_house_number, str)
        assert isinstance(current_address, str)
        assert isinstance(document_list, list)

        self._current_postal_code = current_postal_code
        self._current_house_number = current_house_number
        self._current_address = current_address
        self._document_list = document_list

    @property
    def current_postal_code(self):
        return self._current_postal_code

    @property
    def current_house_number(self):
        return self._current_house_number

    @property
    def current_address(self):
        return self._current_address

    @property
    def document_list(self):
        return self._document_list

