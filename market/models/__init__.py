import hashlib
import json
import pickle
import time
import uuid

from dispersy.crypto import ECCrypto


class DatabaseModel(object):
    """
    This DatabaseModel implements all common functions that models that can be saved in the market.database.Database must have.

    All other models extend this class.
    """
    type = 'database_model'
    _hash_exclude = ['_signature', '_time_signed', '_signer']

    def __init__(self, id=None):
        self._id = id
        self._time_signed = 0
        self._signature = None
        self._signer = None

    def save(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @property
    def signature(self):
        return self._signature

    @property
    def signer(self):
        return self._signer

    @property
    def time_signed(self):
        return self._time_signed

    def generate_id(self, force=False):
        """
        Generate a new id if one doesn't already exist, except if forced to generate a new one.
        :param force: Force generate a new id even if one already exists.
        :return: The object id.
        """
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
        try:
            pickled = data.decode(encoding)
            return pickle.loads(pickled)
        except:
            return None

    # TODO: Implement a deep compare.
    def __eq__(self, other):
        return self.id == other.id

    def update(self, database):
        """
        Update the current object with the latest data. This is to ensure that the same object pointer is used instead of when
        a new version of the object is retrieved from the database.
        """
        updated_self = database.get(self.type, self.id)
        assert isinstance(updated_self, type(self))
        assert updated_self.id == self.id

        # Update all attributes with the newer version.
        for attr in vars(self):
            setattr(self, attr, getattr(updated_self, attr))

    def post_or_put(self, database, check_time=False):
        """
        Post or Put the object in the database. In the case of `put' the check_time variable can be set to True, which will then ensure
        that objects are only replaced if the time_signed of the object being placed is greater than that of the object stored in the
        database
        """
        me = database.get(self.type, self.id)
        if me:
            if not check_time or (check_time and me.time_signed < self.time_signed):
                database.put(self.type, self.id, self)
        else:
            database.post(self.type, self)

    def generate_sha1_hash(self):
        output = []
        for attr in vars(self):
            if attr not in self._hash_exclude:
                attribute = getattr(self, attr)
                if isinstance(attribute, list) or isinstance(attribute, dict):
                    new_list = []
                    if isinstance(attribute, list):
                        new_list = sorted(attribute)
                    elif isinstance(attribute, dict):
                        new_list = sorted(attribute.items())
                    output.append(str(new_list))
                else:
                    output.append(str(attribute))

        sha1_hash = hashlib.sha1(json.dumps(output)).hexdigest()
        return sha1_hash

    def sign(self, api):
        """
        Sign a model by hashing its contents and signing this hash.
        """
        if not self.id:
            raise RuntimeError("Can't sign an unsaved model")

        ec = ECCrypto()
        hash = self.generate_sha1_hash()

        private_key = api.db.backend.get_option('user_key_priv')
        public_key = api.db.backend.get_option('user_key_pub')
        signing_key = ec.key_from_private_bin(private_key.decode('HEX'))

        self._signature = ec.create_signature(signing_key, hash)
        self._signer = public_key
        self._time_signed = int(time.time())

        self.post_or_put(api.db)

    def _has_signature(self):
        return self.signature and self.signer

    @classmethod
    def signature_valid(cls, obj):
        ec = ECCrypto()
        signing_key = ec.key_from_public_bin(obj._signer.decode("HEX"))
        signature_valid = ec.is_valid_signature(signing_key, obj.generate_sha1_hash(), obj.signature)
        return signature_valid
