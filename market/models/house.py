from market.models import DatabaseModel


class House(DatabaseModel):
    _type = 'house'

    def __init__(self, postal_code, house_number, price):
        super(House, self).__init__()
        assert isinstance(postal_code, str)
        assert isinstance(house_number, str)
        assert isinstance(price, int)

        self._postal_code = postal_code
        self._house_number = house_number
        self._price = price

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def house_number(self):
        return self._house_number

    @property
    def price(self):
        return self._price
