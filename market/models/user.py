from market.models import DatabaseModel


class User(DatabaseModel):
    _type = 'users'

    def __init__(self, public_key, time_added):
        self._public_key = public_key
        self._time_added = time_added

    @property
    def user_key(self):
        return self._public_key

    @property
    def time_added(self):
        return self._time_added

    def generate_id(self):
        return self.user_key