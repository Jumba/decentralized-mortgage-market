from market.models import DatabaseModel


class House(DatabaseModel):
    _type = 'house'

    def __init__(self, id, postal_code, house_number, price):
        assert isinstance(id, str)
        assert isinstance(postal_code, str)
        assert isinstance(house_number, str)
        assert isinstance(price, int)

        self._id = id
        self._postal_code = postal_code
        self._house_number = house_number
        self._price = price

    @property
    def id(self):
        return self._id

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def house_number(self):
        return self._house_number

    @property
    def price(self):
        return self._price
