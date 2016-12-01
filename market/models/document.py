import mimetypes

from market.models import DatabaseModel


class Document(DatabaseModel):
    _type = 'document'

    def __init__(self, mime, data):
        assert isinstance(mime, str)
        assert isinstance(data, str)

        self._mime = mime
        self._data = data

    @property
    def mime(self):
        return self._mime

    @property
    def data(self):
        return self._data

    def decode_document(self, path):
        with open(path, 'wb') as file:
            file.write(self.data.decode('base64'))


    @staticmethod
    def encode_document(path):
        return Document(mimetypes.guess_type(path)[0], open(path, 'rb').read().encode('base64', 'strict'))