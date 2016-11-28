from market.models import DatabaseModel


class Document(DatabaseModel):
    def __init__(self, id, mime, data):
        assert isinstance(id, str)
        assert isinstance(mime, str)
        assert isinstance(data, str)

        self._id = id
        self._mime = mime
        self._data = data

    @property
    def id(self):
        return self._id

    @property
    def mime(self):
        return self._mime

    @property
    def data(self):
        return self._data

    @staticmethod
    def encode_document(path):
        return open(path, 'rb').read().encode('base64', 'strict')