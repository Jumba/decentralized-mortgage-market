import unittest
from uuid import UUID

from market.api.api import STATUS
from market.models import DatabaseModel
from market.models.loans import Mortgage
from market.multichain.database import MultiChainDB, DatabaseBlock

class CustomAssertions(object):
    """
    This function checks whether two blocks: block1 and block2, are the same block.
    """
    def assertEqualBlocks(self, block1, block2):
        self.assertEqual(block1.benefactor, block2.benefactor)
        self.assertEqual(block1.beneficiary, block2.beneficiary)
        self.assertEqual(block1.agreement_benefactor, block2.agreement_benefactor)
        self.assertEqual(block1.agreement_beneficiary, block2.agreement_beneficiary)
        self.assertEqual(block1.sequence_number_benefactor, block2.sequence_number_benefactor)
        self.assertEqual(block1.sequence_number_beneficiary, block2.sequence_number_beneficiary)
        self.assertEqual(block1.previous_hash_benefactor, block2.previous_hash_benefactor)
        self.assertEqual(block1.previous_hash_beneficiary, block2.previous_hash_beneficiary)
        self.assertEqual(block1.signature_benefactor, block2.signature_benefactor)
        self.assertEqual(block1.signature_beneficiary, block2.signature_beneficiary)
        self.assertEqual(block1.time, block2.time)
        self.assertEqual(block1.hash_block, block2.hash_block)

class MultichainDatabaseTest(unittest.TestCase, CustomAssertions):
    def setUp(self):
        self.db = MultiChainDB('.', 'test-db')

    def test_from_signed_confirm_message(self):
        """
        This test checks the functionality of making a block with the payload from a message.
        """
        message = Message()
        block = DatabaseBlock.from_signed_confirm_message(message)

        self.assertEqual(block.benefactor, message.payload.benefactor)
        self.assertEqual(block.beneficiary, message.payload.beneficiary)
        self.assertEqual(DatabaseModel.decode(block.agreement_benefactor), message.payload.agreement_benefactor)
        self.assertEqual(DatabaseModel.decode(block.agreement_beneficiary), message.payload.agreement_beneficiary)
        self.assertEqual(block.sequence_number_benefactor, message.payload.sequence_number_benefactor)
        self.assertEqual(block.sequence_number_beneficiary, message.payload.sequence_number_beneficiary)
        self.assertEqual(block.previous_hash_benefactor, message.payload.previous_hash_benefactor)
        self.assertEqual(block.previous_hash_beneficiary, message.payload.previous_hash_beneficiary)
        self.assertEqual(block.time, message.payload.time)

    def test_add_block(self):
        """
        This test checks the functionality of adding a block to the blockchain.
        """
        message = Message()
        block = DatabaseBlock.from_signed_confirm_message(message)

        # Add the block to the blockchain
        self.db.add_block(block)
        # Get the block by the hash of the block
        result = self.db.get_by_hash(block.hash_block)

        # Check whether the block was added correctly
        self.assertEqualBlocks(block, result)


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