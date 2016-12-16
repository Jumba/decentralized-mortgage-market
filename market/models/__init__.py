import json
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

    def generate_id(self, force=False):
        if not self._id or force:
            self._id = uuid.uuid1()
        return self._id

    def encode(self, encoding='base64'):
        """
        Pickles the object and encodes it using the given encoding. Defaults to 'base64'

        :param encoding: The chosen encoding
        :type encoding: str
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

    def update(self, database):
        updated_self = database.get(self.type, self.id)
        assert isinstance(updated_self, type(self))
        assert updated_self.id == self.id
        for attr in vars(self):
            setattr(self, attr, getattr(updated_self, attr))

    def post_or_put(self, database):
        me = database.get(self.type, self.id)
        if me:
            database.put(self.type, self.id, self)
        else:
            database.post(self.type, self)

    def serialize(self):
        output = {'class': type(self).__name__ }
        for attr in vars(self):
            output[attr] = getattr(self, attr)

        return json.dumps(output)


