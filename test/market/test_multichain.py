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

        message = MessageBeneficiary()
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

        message = MessageBeneficiary()
        block = DatabaseBlock.from_signed_confirm_message(message)

        # Add the block to the blockchain
        self.db.add_block(block)
        # Get the block by the hash of the block
        result = self.db.get_by_hash(block.hash_block)

        # Check whether the block was added correctly
        self.assertEqualBlocks(block, result)

    def test_update_block_with_beneficiary(self):
        """
        This test checks the functionality of updating a block in the blockchain.
        """

        message_request = MessageBenefactor()
        message_response = MessageBeneficiary()

        # Add the block with only the information from benefactor to the blockchain
        block_benefactor = DatabaseBlock.from_signed_confirm_message(message_request)
        self.db.add_block(block_benefactor)
        # Update the block with the information from the beneficiary
        block_beneficiary = DatabaseBlock.from_signed_confirm_message(message_response)
        self.db.update_block_with_beneficiary(block_beneficiary)

        # Get the updated block by the hash of the block
        result = self.db.get_by_hash(block_beneficiary.hash_block)
        # Get the updated block by the public key and the sequence number
        result_benefactor = self.db.get_by_public_key_and_sequence_number(message_request.payload.benefactor,
                                                                           block_benefactor.sequence_number_benefactor)
        result_beneficiary = self.db.get_by_public_key_and_sequence_number(message_request.payload.beneficiary,
                                                                           block_beneficiary.sequence_number_beneficiary)

        #Check whether the block was updated correctly
        self.assertEqualBlocks(result_benefactor, result_beneficiary)
        self.assertEqualBlocks(result_benefactor, result)
        self.assertEqualBlocks(result_beneficiary, result)

    def test_get_latest_hash(self):
        """
        This test checks the functionality of getting the latest hash of a user.
        """

        message_request = MessageBenefactor()
        message_response = MessageBeneficiary()

        # Add the block with only the information from benefactor to the blockchain
        block_benefactor = DatabaseBlock.from_signed_confirm_message(message_request)
        self.db.add_block(block_benefactor)
        # Update the block with the information from the beneficiary
        block_beneficiary = DatabaseBlock.from_signed_confirm_message(message_response)
        self.db.update_block_with_beneficiary(block_beneficiary)

        # Get the latest block added
        latest_block_benefactor = self.db.get_by_public_key_and_sequence_number(message_request.payload.benefactor,
                                                                                block_benefactor.sequence_number_benefactor)
        latest_block_beneficiary = self.db.get_by_public_key_and_sequence_number(message_request.payload.beneficiary,
                                                                                 block_beneficiary.sequence_number_beneficiary)

        # Get the latest hash
        latest_hash_benefactor = self.db.get_latest_hash(message_request.payload.benefactor)
        latest_hash_beneficiary = self.db.get_latest_hash(message_request.payload.beneficiary)

        # Check whether the hash is the right one
        self.assertEqual(latest_hash_benefactor, latest_block_benefactor.hash_block)
        self.assertEqual(latest_hash_beneficiary, latest_block_beneficiary.hash_block)
        self.assertEqual(latest_hash_benefactor, latest_hash_beneficiary)

    def test_get_latest_sequence_number(self):
        """
        This test checks he functionality of getting the latest sequence number
        """

        message_request = MessageBenefactor()
        message_response = MessageBeneficiary()

        # Add the block with only the information from benefactor to the blockchain
        block_benefactor = DatabaseBlock.from_signed_confirm_message(message_request)
        self.db.add_block(block_benefactor)
        # Update the block with the information from the beneficiary
        block_beneficiary = DatabaseBlock.from_signed_confirm_message(message_response)
        self.db.update_block_with_beneficiary(block_beneficiary)

        # Get the latest block added
        latest_block_benefactor = self.db.get_by_public_key_and_sequence_number(message_request.payload.benefactor,
                                                                                block_benefactor.sequence_number_benefactor)
        latest_block_beneficiary = self.db.get_by_public_key_and_sequence_number(message_request.payload.beneficiary,
                                                                                 block_beneficiary.sequence_number_beneficiary)

        # get the latest sequence number
        latest_sequence_number_benefactor = self.db.get_latest_sequence_number(message_request.payload.benefactor)
        latest_sequence_number_beneficiary = self.db.get_latest_sequence_number(message_request.payload.beneficiary)

        # Check whether the sequence numbers are the right ones
        self.assertEqual(latest_sequence_number_benefactor, latest_block_benefactor.sequence_number_benefactor)
        self.assertEqual(latest_sequence_number_beneficiary, latest_block_beneficiary.sequence_number_beneficiary)

    def tearDown(self):
        self.db.close()


class PayloadBeneficiary(object):
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

class MessageBeneficiary(object):
    payload = PayloadBeneficiary()

class PayloadBenefactor(object):
    mortgage = Mortgage(UUID('b97dfa1c-e125-4ded-9b1a-5066462c529c'), UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                        'ING', 80000, 1, 2.5, 1.5, 2.5, 36, 'A', [], STATUS.ACCEPTED)

    benefactor = 'benefactor-key-hiuwehduiee2u8'
    beneficiary = 'beneficiary-key-d8923yr94fh3re'
    agreement_benefactor = mortgage
    agreement_beneficiary = None
    sequence_number_benefactor = 3
    sequence_number_beneficiary = 0
    previous_hash_benefactor = 'prev-hash-benefactor-urc89utqhoird'
    previous_hash_beneficiary = ''
    signature_benefactor = ''
    signature_beneficiary = ''
    time = 300

class MessageBenefactor(object):
    payload = PayloadBeneficiary()