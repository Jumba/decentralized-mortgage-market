import pickle


class DatabaseModel(object):
    def save(self, id):
        self._id = id

    @property
    def id(self):
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
