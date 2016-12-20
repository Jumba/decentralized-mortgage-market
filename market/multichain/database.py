""" This file contains everything related to persistence for MultiChain.
"""
from os import path
from hashlib import sha256
from market.dispersy.database import Database

DATABASE_DIRECTORY = path.join(u"sqlite")
# Path to the database location + dispersy._workingdirectory
DATABASE_PATH = path.join(DATABASE_DIRECTORY, u"multichain.db")
# Version to keep track if the db schema needs to be updated.
LATEST_DB_VERSION = 1
# Schema for the MultiChain DB.
schema = u"""
CREATE TABLE IF NOT EXISTS multi_chain(
 public_key_benefactor		  TEXT NOT NULL,
 public_key_beneficiary		  TEXT NOT NULL,

 model_benefactor             TEXT NOT NULL,
 sequence_number_benefactor   INTEGER NOT NULL,
 previous_hash_benefactor	  TEXT NOT NULL,
 signature_benefactor		  TEXT NOT NULL,
 hash_benefactor		      TEXT PRIMARY KEY,

 model_beneficiary            TEXT NOT NULL,
 sequence_number_beneficiary  INTEGER NOT NULL,
 previous_hash_beneficiary	  TEXT NOT NULL,
 signature_beneficiary		  TEXT NOT NULL,
 hash_beneficiary	          TEXT NOT NULL,

 insert_time                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
 );

CREATE TABLE option(key TEXT PRIMARY KEY, value BLOB);
INSERT INTO option(key, value) VALUES('database_version', '""" + str(LATEST_DB_VERSION) + u"""');
"""


class MultiChainDB(Database):
    """
    Persistence layer for the MultiChain Community.
    Connection layer to SQLiteDB.
    Ensures a proper DB schema on startup.
    """

    def __init__(self, dispersy, working_directory):
        """
        Sets up the persistence layer ready for use.
        :param dispersy: Dispersy stores the PK.
        :param working_directory: Path to the working directory
        that will contain the the db at working directory/DATABASE_PATH
        :return:
        """
        super(MultiChainDB, self).__init__(path.join(working_directory, DATABASE_PATH))
        self._dispersy = dispersy
        self.open()

    def add_block(self, block):
        """
        Persist a block
        :param block: The data that will be saved.
        """
        data = (buffer(block.public_key_benefactor), buffer(block.public_key_beneficiary),
                buffer(block.model_benefactor),
                block.sequence_number_benefactor, buffer(block.previous_hash_benefactor),
                buffer(block.signature_benefactor), buffer(block.hash_benefactor),
                buffer(block.model_beneficiary),
                block.sequence_number_beneficiary, buffer(block.previous_hash_beneficiary),
                buffer(block.signature_beneficiary), buffer(block.hash_beneficiary))

        self.execute(
            u"INSERT INTO multi_chain (public_key_benefactor, public_key_beneficiary, "
            u"model_benefactor, sequence_number_benefactor, previous_hash_benefactor, "
            u"signature_benefactor, hash_benefactor, "
            u"model_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, "
            u"signature_beneficiary, hash_beneficiary) "
            u"VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
            data)
        self.commit()

    def update_block_with_beneficiary(self, block):
        """
        Update an existing block
        :param block: The data that will be saved.
        """
        data = (
            buffer(block.model_beneficiary),
            block.sequence_number_beneficiary, buffer(block.previous_hash_beneficiary),
            buffer(block.signature_beneficiary), buffer(block.hash_beneficiary), buffer(block.hash_benefactor))

        self.execute(
            u"UPDATE multi_chain "
            u"SET model_beneficiary = ?, "
            u"sequence_number_beneficiary = ?, previous_hash_beneficiary = ?, "
            u"signature_beneficiary = ?, hash_beneficiary = ? "
            u"WHERE hash_benefactor = ?",
            data)
        self.commit()

    def get_latest_hash(self, public_key):
        """
        Get the relevant hash of the latest block in the chain for a specific public key.
        Relevant means the hash_benefactor if the last block was a request,
        hash_beneficiary if the last block was a response.
        :param public_key: The public_key for which the latest hash has to be found.
        :return: the relevant hash
        """
        public_key = buffer(public_key)
        db_query = u"SELECT block_hash, MAX(sequence_number) FROM (" \
                   u"SELECT hash_benefactor AS block_hash, sequence_number_benefactor AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_benefactor = ? " \
                   u"UNION " \
                   u"SELECT hash_beneficiary AS block_hash, sequence_number_beneficiary AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_beneficiary = ?)"

        db_result = self.execute(db_query, (public_key, public_key)).fetchone()[0]

        return str(db_result) if db_result else None

    def get_latest_block(self, public_key):
        return self.get_by_hash(self.get_latest_hash(public_key))

    def get_by_hash_benefactor(self, hash_benefactor):
        """
        Returns a block saved in the persistence
        :param hash_benefactor: The hash_benefactor of the block that needs to be retrieved.
        :return: The block that was requested or None
        """
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, " \
                   u"model_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, hash_benefactor, " \
                   u"model_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, hash_beneficiary, insert_time " \
                   u"FROM `multi_chain` WHERE hash_benefactor = ? LIMIT 1"
        db_result = self.execute(db_query, (buffer(hash_benefactor),)).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    def get_by_hash(self, hash):
        """
        Returns a block saved in the persistence, based on a hash that can be either hash_benefactor or hash_beneficiary
        :param hash: The hash of the block that needs to be retrieved.
        :return: The block that was requested or None
        """
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, " \
                   u"model_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, hash_benefactor, " \
                   u"model_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, hash_beneficiary, insert_time " \
                   u"FROM `multi_chain` WHERE hash_benefactor = ? OR hash_beneficiary = ? LIMIT 1"
        db_result = self.execute(db_query, (buffer(hash), buffer(hash))).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    def get_by_public_key_and_sequence_number(self, public_key, sequence_number):
        """
        Returns a block saved in the persistence.
        :param public_key: The public key corresponding to the block
        :param sequence_number: The sequence number corresponding to the block.
        :return: The block that was requested or None"""
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, " \
                   u"model_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, hash_benefactor, " \
                   u"model_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, hash_beneficiary, insert_time " \
                   u"FROM (" \
                   u"SELECT *, sequence_number_benefactor AS sequence_number, " \
                   u"public_key_benefactor AS pk FROM `multi_chain` " \
                   u"UNION " \
                   u"SELECT *, sequence_number_beneficiary AS sequence_number," \
                   u"public_key_beneficiary AS pk FROM `multi_chain`) " \
                   u"WHERE sequence_number = ? AND pk = ? LIMIT 1"
        db_result = self.execute(db_query, (sequence_number, buffer(public_key))).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    def get_blocks_since(self, public_key, sequence_number):
        """
        Returns database blocks with sequence number higher than or equal to sequence_number, at most 100 results
        :param public_key: The public key corresponding to the member id
        :param sequence_number: The linear block number
        :return A list of DB Blocks that match the criteria
        """
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, " \
                   u"model_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, hash_benefactor, " \
                   u"model_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, hash_beneficiary, insert_time " \
                   u"FROM (" \
                   u"SELECT *, sequence_number_benefactor AS sequence_number," \
                   u" public_key_benefactor AS public_key FROM `multi_chain` " \
                   u"UNION " \
                   u"SELECT *, sequence_number_beneficiary AS sequence_number," \
                   u" public_key_beneficiary AS public_key FROM `multi_chain`) " \
                   u"WHERE sequence_number >= ? AND public_key = ? " \
                   u"ORDER BY sequence_number ASC " \
                   u"LIMIT 100"
        db_result = self.execute(db_query, (sequence_number, buffer(public_key))).fetchall()
        return [self._create_database_block(db_item) for db_item in db_result]

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

    def get_all_hash_benefactor(self):
        """
        Get all the hash_benefactor saved in the persistence layer.
        :return: list of hash_benefactor.
        """
        db_result = self.execute(u"SELECT hash_benefactor FROM multi_chain").fetchall()
        # Unpack the db_result tuples and decode the results.
        return [str(x[0]) for x in db_result]

    def contains(self, hash_benefactor):
        """
        Check if a block is existent in the persistence layer.
        :param hash_benefactor: The hash_benefactor that is queried
        :return: True if the block exists, else false.
        """
        db_query = u"SELECT hash_benefactor FROM multi_chain WHERE hash_benefactor == ? LIMIT 1"
        db_result = self.execute(db_query, (buffer(hash_benefactor),)).fetchone()
        return db_result is not None

    def get_latest_sequence_number(self, public_key):
        """
        Return the latest sequence number known for this public_key.
        If no block for the pk is know returns -1.
        :param public_key: Corresponding public key
        :return: sequence number (integer) or -1 if no block is known
        """
        public_key = buffer(public_key)
        db_query = u"SELECT MAX(sequence_number) FROM (" \
                   u"SELECT sequence_number_benefactor AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_benefactor == ? UNION " \
                   u"SELECT sequence_number_beneficiary AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_beneficiary = ? )"
        db_result = self.execute(db_query, (public_key, public_key)).fetchone()[0]
        return db_result if db_result is not None else -1

    def open(self, initial_statements=True, prepare_visioning=True):
        return super(MultiChainDB, self).open(initial_statements, prepare_visioning)

    def close(self, commit=True):
        return super(MultiChainDB, self).close(commit)

    def check_database(self, database_version):
        """
        Ensure the proper schema is used by the database.
        :param database_version: Current version of the database.
        :return:
        """
        assert isinstance(database_version, unicode)
        assert database_version.isdigit()
        assert int(database_version) >= 0
        database_version = int(database_version)

        if database_version < 1:
            self.executescript(schema)
            self.commit()

        return LATEST_DB_VERSION


class DatabaseBlock:
    """ DataClass for a multichain block. """

    def __init__(self, data):
        """ Create a block from data """
        # Common part
        self.public_key_benefactor = str(data[0])
        self.public_key_beneficiary = str(data[1])
        # Benefactor part
        self.model_benefactor = str(data[2])
        self.sequence_number_benefactor = data[3]
        self.previous_hash_benefactor = str(data[4])
        self.signature_benefactor = str(data[5])
        self.hash_benefactor = str(data[6])
        # Beneficiary part
        self.model_beneficiary = str(data[7])
        self.sequence_number_beneficiary = data[8]
        self.previous_hash_beneficiary = str(data[9])
        self.signature_beneficiary = str(data[10])
        self.hash_beneficiary = str(data[11])

        self.insert_time = data[12]

    # @classmethod
    # def from_signature_response_message(cls, message):
    #     payload = message.payload
    #     benefactor = message.authentication.signed_members[0]
    #     beneficiary = message.authentication.signed_members[1]
    #     return cls((benefactor[1].public_key, beneficiary[1].public_key,
    #                 payload.model_benefactor,
    #                 payload.sequence_number_benefactor, payload.previous_hash_benefactor,
    #                 benefactor[0], sha256(encode_block_benefactor_half(payload, benefactor[1].public_key,
    #                                                                    beneficiary[1].public_key, benefactor[0])).digest(),
    #                 payload.model_beneficiary,
    #                 payload.sequence_number_beneficiary, payload.previous_hash_beneficiary,
    #                 beneficiary[0], sha256(encode_block(payload, benefactor, beneficiary)).digest(),
    #                 None))
    #
    # @classmethod
    # def from_signature_request_message(cls, message):
    #     payload = message.payload
    #     benefactor = message.authentication.signed_members[0]
    #     beneficiary = message.authentication.signed_members[1]
    #     return cls((benefactor[1].public_key, beneficiary[1].public_key,
    #                 payload.model_benefactor,
    #                 payload.sequence_number_benefactor, payload.previous_hash_benefactor,
    #                 benefactor[0], sha256(encode_block_benefactor_half(payload, benefactor[1].public_key,
    #                                                                    beneficiary[1].public_key, benefactor[0])).digest(),
    #                 0,
    #                 -1, EMPTY_HASH,
    #                 "", EMPTY_HASH,
    #                 None))
