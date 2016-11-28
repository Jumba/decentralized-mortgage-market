from market.models import DatabaseModel

ROLES = (
    'NONE',
    'BORROWER',
    'INVESTOR',
    'FINANCIAL_INSTITUTION'
)


class Role(DatabaseModel):
    def __init__(self, user_key, role):
        assert 0 <= role < len(ROLES)

        self._user_key = user_key
        self._role = role

    @property
    def role(self):
        return self._role

    @property
    def role_name(self):
        return ROLES[self.role]

    @property
    def user_key(self):
        return self._user_key
