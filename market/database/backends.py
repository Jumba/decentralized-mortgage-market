from hashlib import sha256
from os import path
import time

from dispersy.database import Database
from market.community.encoding import encode


class Backend(object):
    """
    The backend interface
    """

    def get(self, _type, _id):
        """
        Get an item out of the key value store.
        :param _type: The type name of the value
        :param _id: The id of the value
        :return: The value
        :raises: IndexError if not found
        """
        raise NotImplementedError

    def post(self, _type, _id, obj):
        """
        Save a value to the key value store
        :param _type: The type name of the value
        :param _id: The id of the value
        :param obj: The value
        :return: True if succeeds, IndexError if `_id` already in use.
        """
        raise NotImplementedError

    def put(self, _type, _id, obj):
        """
        Replace a value in the key value store
        :param _type: The type name of the value
        :param _id:  The id of the value
        :param obj: The value
        :return: True if succeeds, False if <type, id> not already in use. (Won't be saved either)
        """
        raise NotImplementedError

    def delete(self, obj):
        """
        Delete a value in the key value store
        :param obj:
        :return:
        """
        raise NotImplementedError

    def id_available(self, _id):
        """
        Check if an ID is available
        :param _id:
        :return:
        """
        raise NotImplementedError

    def exists(self, _type, _id):
        """
        Check if a <type, id> pair exists
        :param _type:
        :param _id:
        :return:
        """
        raise NotImplementedError

    def clear(self):
        """
        Purge the database
        :return:
        """
        raise NotImplementedError

    def get_all(self, _type):
        """
        Get all values of `_type`
        :param _type:
        :return:
        """
        raise NotImplementedError

    def get_option(self, option_name):
        """
        Return an option
        :param option_name:
        :return:
        """
        raise NotImplementedError

    def set_option(self, option_name, value):
        """
        Set an option
        :param option_name:
        :param value:
        :return:
        """
        raise NotImplementedError


class BlockChain(object):
    def add_block(self, block):
        """
        Persist a block
        :param block: The data that will be saved.
        """
        raise NotImplementedError

    def update_block_with_beneficiary(self, block):
        """
        Update an existing block
        :param block: The data that will be saved.
        """
        raise NotImplementedError

    def get_latest_hash(self):
        """
        Get the hash of the latest block in the chain.
        :return: the relevant hash
        """
        raise NotImplementedError

    def get_by_hash(self, hash):
        """
        Returns a block saved in the persistence.
        :param hash: The hash of the block that needs to be retrieved.
        :return: The block that was requested or None
        """
        raise NotImplementedError

    def get_by_public_key_and_sequence_number(self, public_key, sequence_number):
        """
        Returns a block saved in the persistence.
        :param public_key: The public key corresponding to the block
        :param sequence_number: The sequence number corresponding to the block.
        :return: The block that was requested or None"""
        raise NotImplementedError

    def _create_database_block(self, db_result):
        """
        Create a Database block or return None.
        :param db_result: The DB_result with the DatabaseBlock or None
        :return: DatabaseBlock if db_result else None
        """
        raise NotImplementedError

    def get_latest_sequence_number(self):
        """
        Return the latest sequence number.
        If no block is known returns 0.
        :return: sequence number (integer) or 0 if no block is known
        """
        raise NotImplementedError

    def get_next_sequence_number(self):
        """
        Return the next sequence number for this public_key.
        If no block for the pk is known return 0, else return latest sequence number + 1.
        :return: sequence number (integer)
        """
        raise NotImplementedError

    def create_genesis_block(self):
        """
        Generates the genesis block.
        :return: DatabaseBlock, the genesis block
        """
        raise NotImplementedError

    def check_add_genesis_block(self):
        """
        Persist the genesis block if there are no blocks yet in the blockchain.
        """
        raise NotImplementedError


class MemoryBackend(Backend):
    """
    An in memory implementation of the backend.
    """
    _data = {'__option': {}}
    _id = {}

    def get(self, type_name, value_id):
        try:
            return self._data[type_name][value_id]
        except:
            raise IndexError

    def post(self, type_name, value_id, obj):
        if type_name not in self._data:
            self._data[type_name] = {}

        if not self.id_available(value_id):
            raise IndexError("Index already in use")

        self._data[type_name][value_id] = obj
        self._id[value_id] = True

    def put(self, type_name, value_id, obj):
        if self.exists(type_name, value_id):
            self._data[type_name][value_id] = obj
            return True
        return False

    def delete(self, obj):
        if obj:
            if self.exists(obj.type, obj.id):
                del self._data[obj.type][obj.id]
                return True
        return False

    def id_available(self, value_id):
        return value_id not in self._id

    def exists(self, type_name, value_id):
        if type_name in self._data:
            return value_id in self._data[type_name]
        return False

    def clear(self):
        self._data = {'__option': {}}
        self._id = {}

    def get_all(self, type_name):
        try:
            return self._data[type_name].values()
        except:
            raise KeyError

    def set_option(self, option_name, value):
        self._data['__option'][option_name] = value

    def get_option(self, option_name):
        try:
            return self._data['__option'][option_name]
        except:
            raise KeyError


class PersistentBackend(Database, Backend, BlockChain):
    """
    A SQlite backed implementation of the backend.
    Uses the dispersy Database class.
    """

    # Path to the database location + dispersy._workingdirectory
    DATABASE_PATH = u"market.db"
    # Version to keep track if the db schema needs to be updated.
    LATEST_DB_VERSION = 1
    # Schema for the DB.
    schema = u"""
    CREATE TABLE IF NOT EXISTS market(
     id		                    TEXT NOT NULL,
     type_name		            TEXT NOT NULL,
     value                      TEXT NOT NULL,

     insert_time                TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
     );


    CREATE TABLE IF NOT EXISTS block_chain(
     benefactor		              TEXT NOT NULL,
     beneficiary		          TEXT NOT NULL,

     agreement_benefactor         TEXT NOT NULL,
     agreement_beneficiary        TEXT NOT NULL,
     sequence_number_benefactor   INTEGER NOT NULL,
     sequence_number_beneficiary  INTEGER NOT NULL,
     previous_hash_benefactor	  TEXT NOT NULL,
     previous_hash_beneficiary	  TEXT NOT NULL,
     signature_benefactor		  TEXT NOT NULL,
     signature_beneficiary		  TEXT NOT NULL,

     insert_time                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
     hash_block                   TEXT NOT NULL,
     previous_hash                TEXT NOT NULL,
     sequence_number              INTEGER NOT NULL
     );


    CREATE TABLE IF NOT EXISTS option(key TEXT PRIMARY KEY, value BLOB);
    INSERT INTO option(key, value) VALUES('database_version', '""" + str(LATEST_DB_VERSION) + u"""');
    """

    def __init__(self, working_directory, database_name=DATABASE_PATH):
        super(PersistentBackend, self).__init__(path.join(working_directory, database_name))
        self.open()

    def open(self, initial_statements=True, prepare_visioning=True):
        return super(PersistentBackend, self).open(initial_statements, prepare_visioning)

    def close(self, commit=True):
        return super(PersistentBackend, self).close(commit)

    def check_database(self, database_version):
        assert isinstance(database_version, unicode)
        assert database_version.isdigit()
        assert int(database_version) >= 0
        database_version = int(database_version)

        if database_version < self.LATEST_DB_VERSION:
            # Remove all previous data, since we have only been testing so far, and previous blocks might not be
            # reliable. In the future, we should implement an actual upgrade procedure
            self.executescript(self.schema)
            self.commit()

        return self.LATEST_DB_VERSION

    def get(self, type_name, value_id):
        db_query = u"SELECT value FROM `market` WHERE type_name = ? AND id = ?"
        db_result = self.execute(db_query, (unicode(type_name), unicode(value_id))).fetchall()

        if len(db_result) != 1:
            raise IndexError

        return db_result[0][0]

    def get_all(self, type_name):
        db_query = u"SELECT value FROM `market` WHERE type_name = ?"
        db_result = self.execute(db_query, (unicode(type_name),)).fetchall()

        return [t[0] for t in db_result]

    def post(self, type_name, value_id, obj):
        if not self.id_available(value_id):
            raise IndexError("Index already in use")

        db_query = u"INSERT INTO `market` (id, type_name, value) VALUES (?, ?, ?)"
        self.execute(db_query, (unicode(value_id), unicode(type_name), unicode(obj)))
        self.commit()

    def put(self, type_name, value_id, obj):
        if self.exists(type_name, value_id):
            db_query = u"UPDATE `market` SET value = ? WHERE id = ? AND type_name = ?"
            self.execute(db_query, (unicode(obj), unicode(value_id), unicode(type_name)))
            self.commit()
            return True
        else:
            return False

    def delete(self, obj):
        db_query = u"DELETE FROM `market` WHERE id = ?"
        cur = self.execute(db_query, (unicode(obj.id),))
        self.commit()
        return cur.rowcount > 0

    def id_available(self, value_id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ?"
        db_result = self.execute(db_query, (unicode(value_id),)).fetchall()
        return db_result[0][0] == 0

    def exists(self, type_name, value_id):
        db_query = u"SELECT COUNT(*) FROM `market` WHERE id = ? AND type_name = ?"
        db_result = self.execute(db_query, (unicode(value_id), unicode(type_name))).fetchall()
        return db_result[0][0] == 1

    def clear(self):
        self.execute(u"DELETE FROM market")
        self.execute(u"DELETE FROM multi_chain")
        self.execute(u"DELETE FROM option")

    def set_option(self, option_name, value):
        db_query = u"INSERT INTO `option` (key, value) VALUES (?, ?)"
        self.execute(db_query, (unicode(option_name), unicode(value),))
        self.commit()

    def get_option(self, option_name):
        db_query = u"SELECT value FROM `option` WHERE key = ?"
        db_result = self.execute(db_query, (unicode(option_name),)).fetchall()

        if len(db_result) != 1:
            raise IndexError

        return db_result[0][0]

    def add_block(self, block):
        """
        Persist a block
        :param block: The data that will be saved.
        """
        data = (buffer(block.benefactor), buffer(block.beneficiary),
                buffer(block.agreement_benefactor), buffer(block.agreement_beneficiary),
                block.sequence_number_benefactor, block.sequence_number_beneficiary,
                buffer(block.previous_hash_benefactor), buffer(block.previous_hash_beneficiary),
                buffer(block.signature_benefactor), buffer(block.signature_beneficiary),
                block.insert_time, buffer(block.hash_block), buffer(self.get_latest_hash()),
                self.get_next_sequence_number())

        self.execute(
            u"INSERT INTO block_chain (benefactor, beneficiary, "
            u"agreement_benefactor, agreement_beneficiary, sequence_number_benefactor, sequence_number_beneficiary, "
            u"previous_hash_benefactor, previous_hash_beneficiary, signature_benefactor, signature_beneficiary, "
            u"insert_time, hash_block, previous_hash, sequence_number) "
            u"VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            data)
        self.commit()

    def update_block_with_beneficiary(self, block):
        """
        Update an existing block
        :param block: The data that will be saved.
        """
        data = (
            buffer(block.beneficiary), buffer(block.agreement_beneficiary),
            block.sequence_number_beneficiary, buffer(block.previous_hash_beneficiary),
            buffer(block.signature_benefactor), buffer(block.signature_beneficiary), buffer(block.hash_block))

        where = (block.insert_time, block.sequence_number_benefactor, buffer(block.benefactor))

        self.execute(
            u"UPDATE block_chain "
            u"SET beneficiary = ?, agreement_beneficiary = ?, "
            u"sequence_number_beneficiary = ?, previous_hash_beneficiary = ?, signature_benefactor = ?,"
            u"signature_beneficiary = ?, hash_block = ? "
            u"WHERE insert_time = ? AND sequence_number_benefactor = ? AND benefactor = ?",
            data + where)
        self.commit()

    def get_latest_hash(self):
        """
        Get the hash of the latest block in the chain for a specific public key.
        :param public_key: The public_key for which the latest hash has to be found.
        :return: the relevant hash
        """
        db_query = u"SELECT hash_block FROM block_chain ORDER BY ROWID DESC LIMIT 1;"
        db_result = self.execute(db_query).fetchone()

        return str(db_result[0]) if db_result else ''

    def get_by_hash(self, hash):
        """
        Returns a block saved in the persistence.
        :param hash: The hash of the block that needs to be retrieved.
        :return: The block that was requested or None
        """
        db_query = u"SELECT benefactor, beneficiary, " \
                   u"agreement_benefactor, agreement_beneficiary, sequence_number_benefactor, " \
                   u"sequence_number_beneficiary, previous_hash_benefactor, " \
                   u"previous_hash_beneficiary, signature_benefactor, signature_beneficiary, " \
                   u"insert_time, hash_block, previous_hash, sequence_number " \
                   u"FROM `block_chain` WHERE hash_block = ? LIMIT 1"
        db_result = self.execute(db_query, (buffer(hash),)).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    def get_by_public_key_and_sequence_number(self, public_key, sequence_number):
        """
        Returns a block saved in the persistence.
        :param public_key: The public key corresponding to the block
        :param sequence_number: The sequence number corresponding to the block.
        :return: The block that was requested or None"""
        db_query = u"SELECT benefactor, beneficiary, " \
                   u"agreement_benefactor, agreement_beneficiary, " \
                   u"sequence_number_benefactor, sequence_number_beneficiary, " \
                   u"previous_hash_benefactor, previous_hash_beneficiary, " \
                   u"signature_benefactor, signature_beneficiary, insert_time, " \
                   u"hash_block, previous_hash, sequence_number " \
                   u"FROM (" \
                   u"SELECT *, sequence_number_benefactor AS seq_number, " \
                   u"benefactor AS pk FROM `block_chain` " \
                   u"UNION " \
                   u"SELECT *, sequence_number_beneficiary AS seq_number," \
                   u"beneficiary AS pk FROM `block_chain`) " \
                   u"WHERE seq_number = ? AND pk = ? LIMIT 1"
        db_result = self.execute(db_query, (sequence_number, buffer(public_key))).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    def _create_database_block(self, db_result):
        """
        Create a Database block or return None.
        :param db_result: The DB_result with the DatabaseBlock or None
        :return: DatabaseBlock if db_result else None
        """
        if db_result:
            return DatabaseBlock(db_result)
        else:
            return None

    def get_latest_sequence_number(self):
        """
        Return the latest sequence number known for this public_key.
        If no block for the pk is known returns 0.
        :param public_key: Corresponding public key
        :return: sequence number (integer) or 0 if no block is known
        """
        db_query = u"SELECT sequence_number FROM block_chain ORDER BY ROWID DESC LIMIT 1;"
        db_result = self.execute(db_query).fetchone()
        return db_result[0] if db_result is not None else 0

    def get_next_sequence_number(self):
        """
        Return the next sequence number for this public_key.
        If no block for the pk is known return 0, else return latest sequence number + 1.
        :return: sequence number (integer)
        """
        sequence_number = self.get_latest_sequence_number()

        if sequence_number == 0:
            return sequence_number
        else:
            return sequence_number + 1

    def create_genesis_block(self):
        """
        Generates the genesis block.
        :param public_key_benefactor: The public key of the benefactor
        :param public_key_beneficiary: The public key of the beneficiary
        :return: DatabaseBlock, the genesis block
        """
        packet = encode(
            (
                str(''),  # benefactor,
                str(''),  # beneficiary,
                str(None),  # agreement_benefactor,
                str(None),  # agreement_beneficiary,
                0,  # sequence_number_benefactor,
                0,  # sequence_number_beneficiary,
                str(''),  # previous_hash_benefactor,
                str(''),  # previous_hash_beneficiary,
                str(''),  # signature_benefactor,
                str(''),  # signature_beneficiary,
                0  # insert_time
            )
        )
        hash = sha256(packet).hexdigest()

        return DatabaseBlock((str(''), str(''), str(None), str(None), 0, 0,
                              str(''), str(''), str(''), str(''), 0, str(hash)))

    def check_add_genesis_block(self):
        """
        Persist the genesis block if there are no blocks yet in the blockchain.
        :param public_key_benefactor: The public key of the benefactor
        :param public_key_beneficiary The public key of the beneficiary
        """
        db_query = u"SELECT COUNT(*) FROM multi_chain"
        db_result = self.execute(db_query).fetchone()

        if db_result[0] == 0:
            genesis_block = self.create_genesis_block()
            self.add_block(genesis_block)


class DatabaseBlock:
    """ DataClass for a blockchain block. """

    def __init__(self, data):
        """ Create a block from data """
        self.benefactor = str(data[0])
        self.beneficiary = str(data[1])
        self.agreement_benefactor = str(data[2])
        self.agreement_beneficiary = str(data[3])
        self.sequence_number_benefactor = data[4]
        self.sequence_number_beneficiary = data[5]
        self.previous_hash_benefactor = str(data[6])
        self.previous_hash_beneficiary = str(data[7])
        self.signature_benefactor = str(data[8])
        self.signature_beneficiary = str(data[9])

        self.insert_time = data[10]

        self.hash_block = sha256(self.hash()).hexdigest()
        if len(data) > 12:
            self.previous_hash = str(data[12])
            self.sequence_number = data[13]

    def hash(self):
        packet = encode(
            (
                self.benefactor,
                self.beneficiary,
                self.agreement_benefactor,
                self.agreement_beneficiary,
                self.sequence_number_benefactor,
                self.sequence_number_beneficiary,
                self.previous_hash_benefactor,
                self.previous_hash_beneficiary,
                self.signature_benefactor,
                self.signature_beneficiary,
                self.insert_time,
            )
        )
        return packet

    @classmethod
    def from_signed_confirm_message(cls, message):
        payload = message.payload
        return cls((payload.benefactor, payload.beneficiary,
                    payload.agreement_benefactor and payload.agreement_benefactor.encode() or '',
                    payload.agreement_beneficiary and payload.agreement_beneficiary.encode() or '',
                    payload.sequence_number_benefactor, payload.sequence_number_beneficiary,
                    payload.previous_hash_benefactor, payload.previous_hash_beneficiary,
                    payload.signature_benefactor, payload.signature_beneficiary, payload.insert_time))
