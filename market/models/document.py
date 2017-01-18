import mimetypes

from market.models import DatabaseModel


class Document(DatabaseModel):
    type = 'document'

    def __init__(self, mime, data, name):
        super(Document, self).__init__()
        assert isinstance(mime, str)
        assert isinstance(data, str)

        self._mime = mime
        self._data = data
        self._name = name

    @property
    def mime(self):
        return self._mime

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    def decode_document(self, path):
        with open(path, 'wb') as f:
            f.write(self.data.decode('base64'))

    @staticmethod
    def encode_document(name, path):
        return Document(mimetypes.guess_type(path)[0], open(path, 'rb').read().encode('base64', 'strict'), name)
