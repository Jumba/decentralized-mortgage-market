import unittest
from uuid import UUID

from market.api.api import STATUS
from market.models import DatabaseModel
from market.models.loans import Mortgage
from market.multichain.database import MultiChainDB, DatabaseBlock


class MultichainDatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = MultiChainDB('.', 'test-db')

    def test_from_signed_confirm_message(self):
        message = Message()
        block = DatabaseBlock.from_signed_confirm_message(message)


        self.assertEqual(block.public_key_benefactor, message.payload.benefactor)
        self.assertEqual(block.public_key_beneficiary, message.payload.beneficiary)
        self.assertEqual(DatabaseModel.decode(block.agreement_benefactor), message.payload.agreement_benefactor)
        self.assertEqual(DatabaseModel.decode(block.agreement_beneficiary), message.payload.agreement_beneficiary)
        self.assertEqual(block.sequence_number_benefactor, message.payload.sequence_number_benefactor)
        self.assertEqual(block.sequence_number_beneficiary, message.payload.sequence_number_beneficiary)
        self.assertEqual(block.previous_hash_benefactor, message.payload.previous_hash_benefactor)
        self.assertEqual(block.previous_hash_beneficiary, message.payload.previous_hash_beneficiary)
        self.assertEqual(block.insert_time, message.payload.time)

    def tearDown(self):
        pass

class Payload(object):
    mortgage = Mortgage(UUID('b97dfa1c-e125-4ded-9b1a-5066462c529c'), UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                                    'ING', 80000, 1, 2.5, 1.5, 2.5, 36, 'A', [], STATUS.ACCEPTED)

    benefactor = 'benefactor-key-hiuwehduiee2u8'
    beneficiary = 'beneficiary-key-d8923yr94fh3re'
    agreement_benefactor = mortgage
    agreement_beneficiary = mortgage
    sequence_number_benefactor = 3
    sequence_number_beneficiary = 1
    previous_hash_benefactor = 'prev-hash-benefactor-urc89utqhoird'
    previous_hash_beneficiary = 'prev-hash-beneficiary-cru894yhfrri2'
    signature_benefactor = 'signature-benefactor-8397yhdi287r'
    signature_beneficiary = 'signature-beneficiary-e89ydughdb23'
    time = 300

class Message(object):
    payload = Payload()