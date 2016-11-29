from market.models import DatabaseModel


class User(DatabaseModel):
    _type = 'users'

    def __init__(self, public_key, time_added, profile_id, loan_request_id, mortgage_ids, investment_ids):
        self._public_key = public_key
        self._time_added = time_added
        self._profile_id = profile_id
        self._loan_request_id = loan_request_id
        self._mortgage_ids = mortgage_ids
        self._investment_ids = investment_ids

    @property
    def user_key(self):
        return self._public_key

    @property
    def time_added(self):
        return self._time_added

    def generate_id(self):
        return self.user_key

    @property
    def profile_id(self):
        return self._profile_id

    @property
    def loan_request_id(self):
        return self._loan_request_id

    @property
    def mortgage_ids(self):
        return self._mortgage_ids

    @property
    def investment_ids(self):
        return self._investment_ids