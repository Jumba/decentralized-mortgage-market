import time

from market.dispersy.payload import Payload
from market.models import DatabaseModel


class DatabaseModelPayload(Payload):
    """
    This is a DatabaseModelPayload, a generic payload that can be used to pass an arbitrary number of models to other
    users on the network.

    `fields' is a list of fields being based in the `models` dictionary. Thus the amount of models transfered is determined by the amount of fields defined.
    """
    class Implementation(Payload.Implementation):
        def __init__(self, meta, fields, models):
            assert isinstance(fields, list)
            assert isinstance(models, dict)
            for field in fields:
                assert field in models
                assert isinstance(models[field], DatabaseModel)

            super(DatabaseModelPayload.Implementation, self).__init__(meta)

            self._fields = fields
            self._models = models

        @property
        def models(self):
            return self._models

        @property
        def fields(self):
            return self._fields

        def get(self, field):
            if field in self._models:
                return self._models[field]


