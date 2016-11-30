from market.models import DatabaseModel


class User(DatabaseModel):
    _type = 'users'

    def __init__(self, public_key, time_added, role_id=None, profile_id=None, loan_request_id=None, mortgage_ids=[], investment_ids=[], pending_loan_request_ids=[]):
        self._public_key = public_key
        self._time_added = time_added
        self._role_id = role_id
        self._profile_id = profile_id
        self._loan_request_id = loan_request_id
        self._mortgage_ids = mortgage_ids
        self._investment_ids = investment_ids
        self._pending_loan_request_ids = pending_loan_request_ids

    @property
    def user_key(self):
        return self._public_key

    @property
    def time_added(self):
        return self._time_added

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

    @property
    def role_id(self):
        return self._role_id

    def generate_id(self):
        return self.user_key

    @profile_id.setter
    def profile_id(self, value):
        self._profile_id = value

    @role_id.setter
    def role_id(self, value):
        self._role_id = value

    # TODO add functions to add and remove mortgages and investments from their list
    def add_mortgage_id(self, mortgage_id):
        # TODO
        self._mortgage_ids = self._mortgage_ids.append(mortgage_id)
        pass

    def remove_mortgage_id(self, mortgage_id):
        # TODO
        self._mortgage_ids = self._mortgage_ids.remove(mortgage_id)
        pass

    def add_investment(self, investment_id):
        # TODO
        self._investment_ids = self._investment_ids.append(investment_id)
        pass

    def remove_investment(self, investment_id):
        # TODO
        self._investment_ids = self._investment_ids.remove(investment_id)
        pass

    # TODO add functions to add and remove pending loan requests from their lists

