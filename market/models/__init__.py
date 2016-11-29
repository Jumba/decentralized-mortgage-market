import pickle
import uuid


class DatabaseModel(object):
    _type = 'database_model'

    def __init__(self, id=None):
        self._id = id

    def save(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    def generate_id(self):
        self._id = uuid.uuid4()
        return self._id

    def encode(self, encoding='base64'):
        """
        Pickles the object and encodes it using the given encoding. Defaults to 'base64'
        :param encoding: The chosen encoding
        :return: An `encoding` encoded representation of the object.
        """
        pickled = pickle.dumps(self)
        return pickled.encode(encoding)

    @staticmethod
    def decode(data, encoding='base64'):
        pickled = data.decode(encoding)
        return pickle.loads(pickled)

    def __eq__(self, other):
        return self.id == other.id
