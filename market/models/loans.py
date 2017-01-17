from enum import Enum
from uuid import UUID

from datetime import datetime

from market.models import DatabaseModel

class LoanRequest(DatabaseModel):
    type = 'loan_request'

    def __init__(self, user_key, house_id, house_link, seller_phone_number, seller_email, mortgage_type, banks, description, amount_wanted, status):
        super(LoanRequest, self).__init__()
        assert isinstance(user_key, str)
        assert isinstance(house_id, UUID)
        assert isinstance(house_link, str)
        assert isinstance(seller_phone_number, str)
        assert isinstance(seller_email, str)
        assert isinstance(mortgage_type, int)
        assert isinstance(banks, list)
        assert isinstance(description, unicode)
        assert isinstance(amount_wanted, int)
        assert isinstance(status, dict)

        self._user_key = user_key
        self._house_id = house_id
        self._house_link = house_link
        self._seller_phone_number = seller_phone_number
        self._seller_email = seller_email
        self._mortgage_type = mortgage_type
        self._banks = banks
        self._description = description
        self._amount_wanted = amount_wanted
        self._status = status

    @property
    def user_key(self):
        return self._user_key

    @property
    def house_id(self):
        return self._house_id

    @property
    def house_link(self):
        return self._house_link

    @property
    def seller_phone_number(self):
        return self._seller_phone_number

    @property
    def seller_email(self):
        return self._seller_email

    @property
    def mortgage_type(self):
        return self._mortgage_type

    @property
    def banks(self):
        return self._banks

    @property
    def description(self):
        return self._description

    @property
    def amount_wanted(self):
        return self._amount_wanted

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


class Mortgage(DatabaseModel):
    type = 'mortgage'

    def __init__(self, request_id, house_id, bank, amount, mortgage_type, interest_rate, max_invest_rate, default_rate, duration, risk, investors, status, campaign_id=None):
        super(Mortgage, self).__init__()
        assert isinstance(request_id, UUID)
        assert isinstance(house_id, UUID)
        assert isinstance(bank, str)
        assert isinstance(amount, int)
        assert isinstance(mortgage_type, int)
        assert isinstance(interest_rate, float)
        assert isinstance(max_invest_rate, float)
        assert isinstance(default_rate, float)
        assert isinstance(duration, int)
        assert isinstance(risk, str)
        assert isinstance(investors, list)
        assert isinstance(status, Enum)
        # assert isinstance(campaign_id, UUID)

        self._request_id = request_id
        self._house_id = house_id
        self._bank = bank
        self._amount = amount
        self._mortgage_type = mortgage_type
        self._interest_rate = interest_rate
        self._max_invest_rate = max_invest_rate
        self._default_rate = default_rate
        self._duration = duration
        self._risk = risk
        self._investors = investors
        self._status = status
        self._campaign_id = None or campaign_id

    @property
    def request_id(self):
        return self._request_id

    @property
    def house_id(self):
        return self._house_id

    @property
    def bank(self):
        return self._bank

    @property
    def amount(self):
        return self._amount

    @property
    def mortgage_type(self):
        return self._mortgage_type

    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def max_invest_rate(self):
        return self._max_invest_rate

    @property
    def default_rate(self):
        return self._default_rate

    @property
    def duration(self):
        return self._duration

    @property
    def risk(self):
        return self._risk

    @property
    def status(self):
        return self._status

    @property
    def investors(self):
        return self._investors

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def campaign_id(self):
        return self._campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._campaign_id = value


class Investment(DatabaseModel):
    type = 'investment'

    def __init__(self, investor_key, amount, duration, interest_rate, mortgage_id, status):
        super(Investment, self).__init__()
        assert isinstance(investor_key, str)
        assert isinstance(amount, int)
        assert isinstance(duration, int)
        assert isinstance(interest_rate, float)
        assert isinstance(mortgage_id, UUID)
        assert isinstance(status, Enum)

        self._investor_key = investor_key
        self._amount = amount
        self._duration = duration
        self._interest_rate = interest_rate
        self._mortgage_id = mortgage_id
        self._status = status

    @property
    def investor_key(self):
        return self._investor_key

    @property
    def status(self):
        return self._status

    @property
    def amount(self):
        return self._amount

    @property
    def duration(self):
        return self._duration

    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def mortgage_id(self):
        return self._mortgage_id

    @status.setter
    def status(self, value):
        self._status = value


class Campaign(DatabaseModel):
    type = 'campaign'

    def __init__(self, mortgage_id, amount, end_date, completed):
        super(Campaign, self).__init__()
        assert isinstance(mortgage_id, UUID)
        assert isinstance(amount, int)
        assert isinstance(end_date, datetime)
        assert isinstance(completed, bool)

        self._mortgage_id = mortgage_id
        self._amount = amount
        self._end_date = end_date
        self._completed = completed

    def subtract_amount(self, investment):
        self._amount = self._amount - investment

        if self._amount <= 0:
            self._completed = True

    @property
    def mortgage_id(self):
        return self._mortgage_id

    @property
    def amount(self):
        return self._amount

    @property
    def end_date(self):
        return self._end_date

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        self._completed = value


