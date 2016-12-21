""" This file contains everything related to persistence for MultiChain.
"""
from os import path
from hashlib import sha256

from market.community.encoding import encode
from market.dispersy.database import Database
from market.models import DatabaseModel

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
 hash_block                   TEXT NOT NULL,

 agreement_benefactor         TEXT NOT NULL,
 sequence_number_benefactor   INTEGER NOT NULL,
 previous_hash_benefactor	  TEXT NOT NULL,
 signature_benefactor		  TEXT NOT NULL,

 agreement_beneficiary        TEXT NOT NULL,
 sequence_number_beneficiary  INTEGER NOT NULL,
 previous_hash_beneficiary	  TEXT NOT NULL,
 signature_beneficiary		  TEXT NOT NULL,

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

    def __init__(self, working_directory, database_name):
        """
        Sets up the persistence layer ready for use.
        :param working_directory: Path to the working directory
        that will contain the the db at working directory/DATABASE_PATH
        :return:
        """
        print path.join(working_directory, DATABASE_DIRECTORY, 'multichain-%s' % database_name)

        super(MultiChainDB, self).__init__(path.join(working_directory, DATABASE_DIRECTORY, 'multichain-%s.db' % database_name))

        self.open()

    def add_block(self, block):
        """
        Persist a block
        :param block: The data that will be saved.
        """
        data = (buffer(block.public_key_benefactor), buffer(block.public_key_beneficiary), buffer(block.hash_block),
                buffer(block.agreement_benefactor), block.sequence_number_benefactor,
                buffer(block.previous_hash_benefactor), buffer(block.signature_benefactor),
                buffer(block.agreement_beneficiary), block.sequence_number_beneficiary,
                buffer(block.previous_hash_beneficiary), buffer(block.signature_beneficiary))

        self.execute(
            u"INSERT INTO multi_chain (public_key_benefactor, public_key_beneficiary, hash_block, "
            u"agreement_benefactor, sequence_number_benefactor, previous_hash_benefactor, "
            u"signature_benefactor, "
            u"agreement_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, "
            u"signature_beneficiary) "
            u"VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            data)
        self.commit()

    def update_block_with_beneficiary(self, block):
        """
        Update an existing block
        :param block: The data that will be saved.
        """
        data = (
            buffer(block.agreement_beneficiary),
            block.sequence_number_beneficiary, buffer(block.previous_hash_beneficiary),
            buffer(block.signature_beneficiary), buffer(block.hash_block), block.sequence_number_benefactor)

        self.execute(
            u"UPDATE multi_chain "
            u"SET agreement_beneficiary = ?, "
            u"sequence_number_beneficiary = ?, previous_hash_beneficiary = ?, "
            u"signature_beneficiary = ?, hash_block = ? "
            u"WHERE sequence_number_benefactor = ?",
            data)
        self.commit()

    def get_latest_hash(self, public_key):
        """
        Get the hash of the latest block in the chain for a specific public key.
        :param public_key: The public_key for which the latest hash has to be found.
        :return: the relevant hash
        """
        public_key = buffer(public_key)
        db_query = u"SELECT block_hash, MAX(sequence_number) FROM (" \
                   u"SELECT hash_block AS block_hash, sequence_number_benefactor AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_benefactor = ? " \
                   u"UNION " \
                   u"SELECT hash_block AS block_hash, sequence_number_beneficiary AS sequence_number " \
                   u"FROM multi_chain WHERE public_key_beneficiary = ?)"

        db_result = self.execute(db_query, (public_key, public_key)).fetchone()[0]

        return str(db_result) if db_result else ''

    # Could be used for testing
    def get_by_hash(self, hash):
        """
        Returns a block saved in the persistence.
        :param hash: The hash of the block that needs to be retrieved.
        :return: The block that was requested or None
        """
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, hash_block, " \
                   u"agreement_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, " \
                   u"agreement_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, insert_time " \
                   u"FROM `multi_chain` WHERE hash_block = ? LIMIT 1"
        db_result = self.execute(db_query, buffer(hash)).fetchone()
        # Create a DB Block or return None
        return self._create_database_block(db_result)

    # Could be used for testing
    def get_by_public_key_and_sequence_number(self, public_key, sequence_number):
        """
        Returns a block saved in the persistence.
        :param public_key: The public key corresponding to the block
        :param sequence_number: The sequence number corresponding to the block.
        :return: The block that was requested or None"""
        db_query = u"SELECT public_key_benefactor, public_key_beneficiary, hash_block, " \
                   u"agreement_benefactor, sequence_number_benefactor, previous_hash_benefactor, " \
                   u"signature_benefactor, " \
                   u"agreement_beneficiary, sequence_number_beneficiary, previous_hash_beneficiary, " \
                   u"signature_beneficiary, insert_time " \
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
        self.public_key_benefactor = str(data[0])
        self.public_key_beneficiary = str(data[1])
        self.agreement_benefactor = str(DatabaseModel.encode(data[2]))
        self.agreement_beneficiary = str(DatabaseModel.encode(data[3]))
        self.sequence_number_benefactor = data[4]
        self.sequence_number_beneficiary = data[5]
        self.previous_hash_benefactor = str(data[6])
        self.previous_hash_beneficiary = str(data[7])
        self.signature_benefactor = str(data[8])
        self.signature_beneficiary = str(data[9])

        self.insert_time = data[10]

        self.hash_block = sha256(self.hash()).hexdigest()

    def hash(self):
        packet = encode(
            (
                self.public_key_benefactor,
                self.public_key_beneficiary,
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
        return cls((payload.benefactor, payload.beneficiary, payload.agreement_benefactor, payload.agreement_beneficiary,
                   payload.sequence_number_benefactor, payload.sequence_number_beneficiary, payload.previous_hash_benefactor,
                   payload.previous_hash_beneficiary, payload.signature_benefactor, payload.signature_beneficiary, payload.time))
