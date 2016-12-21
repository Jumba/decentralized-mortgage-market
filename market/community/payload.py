from dispersy.payload import Payload
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


class APIMessagePayload(Payload):
    """
    This is a DatabaseModelPayload, a generic payload that can be used to pass an arbitrary number of models to other
    users on the network.

    `fields' is a list of fields being based in the `models` dictionary. Thus the amount of models transfered is determined by the amount of fields defined.
    """

    class Implementation(Payload.Implementation):
        def __init__(self, meta, request, fields, models):
            assert isinstance(request, unicode)
            assert isinstance(fields, list)
            assert isinstance(models, dict)

            for field in fields:
                assert field in models
                assert isinstance(models[field], DatabaseModel)

            super(APIMessagePayload.Implementation, self).__init__(meta)

            self._request = request
            self._fields = fields
            self._models = models

        @property
        def request(self):
            return self._request

        @property
        def models(self):
            return self._models

        @property
        def fields(self):
            return self._fields

        def get(self, field):
            if field in self._models:
                return self._models[field]


class SignedConfirmPayload(Payload):
    class Implementation(Payload.Implementation):
        def __init__(self, meta, benefactor, beneficiary, agreement, time):
            assert isinstance(benefactor, str)
            assert isinstance(beneficiary, str)
            assert isinstance(agreement, DatabaseModel)
            assert isinstance(time, int)

            super(SignedConfirmPayload.Implementation, self).__init__(meta)

            self._benefactor = benefactor
            self._beneficiary = beneficiary
            self._agreement = agreement
            self._time = time
            
        @property
        def benefactor(self):
            return self._benefactor

        @property
        def beneficiary(self):
            return self._beneficiary

        @property
        def agreement(self):
            return self._agreement

        @property
        def time(self):
            return self._time

class ModelRequestPayload(Payload):
    class Implementation(Payload.Implementation):
        def __init__(self, meta, models):
            assert isinstance(models, list)
            super(ModelRequestPayload.Implementation, self).__init__(meta)
            self._model_ids = models

        @property
        def models(self):
            return self._model_ids
