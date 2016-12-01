from market.models import DatabaseModel

class LoanRequest(DatabaseModel):
    _type = 'loan_request'

    def __init__(self, house_id, mortgage_type, banks, description, amount_wanted, status):
        assert isinstance(house_id, str)
        assert isinstance(mortgage_type, int)
        assert isinstance(banks, list)
        assert isinstance(description, unicode)
        assert isinstance(amount_wanted, int)
        assert isinstance(status, str)

        self._house_id = house_id
        self._mortgage_type = mortgage_type
        self._banks = banks
        self._description = description
        self._amount_wanted = amount_wanted
        self._status = status

    @property
    def house_id(self):
        return self._house_id

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


class Mortgage(DatabaseModel):
    _type = 'mortgage'

    def __init__(self, request_id, house_id, bank, amount, mortgage_type, interest_rate, max_invest_rate, default_rate, duration, risk, investors, status):
        assert isinstance(request_id, str)
        assert isinstance(house_id, str)
        assert isinstance(bank, str)
        assert isinstance(amount, int)
        assert isinstance(mortgage_type, int)
        assert isinstance(interest_rate, float)
        assert isinstance(max_invest_rate, float)
        assert isinstance(default_rate, float)
        assert isinstance(duration, int)
        assert isinstance(risk, str)
        assert isinstance(investors, list)
        assert isinstance(status, str)

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
    def default_rate(self):
        return self._default_rate

    @property
    def duration(self):
        return self._duration

    @property
    def status(self):
        return self._status


class Investment(DatabaseModel):
    _type = 'investment'

    def __init__(self, user_key, amount, duration, interest_rate, mortgage_id, status):
        assert isinstance(user_key, str)
        assert isinstance(amount, int)
        assert isinstance(duration, int)
        assert isinstance(interest_rate, float)
        assert isinstance(mortgage_id, str)
        assert isinstance(status, str)

        self._user_key = user_key
        self._amount = amount
        self._duration = duration
        self._interest_rate = interest_rate
        self._mortgage_id = mortgage_id
        self._status = status

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

class Campaign(DatabaseModel):
    _type = 'campaign'

    def __init__(self, mortgage_id, end_date, completed):
        assert isinstance(mortgage_id, str)
        assert isinstance(end_date, str)
        assert isinstance(completed, bool)

        self._mortgage_id = mortgage_id
        self._end_date = end_date
        self._completed = completed