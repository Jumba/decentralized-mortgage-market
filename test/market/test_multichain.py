import unittest
from uuid import UUID

from market.api.api import STATUS
from market.models import DatabaseModel
from market.models.loans import Mortgage, Investment
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
        self.db = MultiChainDB('.', u'test.db')

        self.mortgage1 = Mortgage(UUID('b97dfa1c-e125-4ded-9b1a-5066462c529c'), UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                             'ING', 80000, 1, 2.5, 1.5, 2.5, 36, 'A', [], STATUS.ACCEPTED)
        self.investment1 = Investment('benefactor-key-i298w4yjexrw', 1000, 24, 1.5,
                                      UUID('b97dfa1c-e125-4ded-9b1a-5066462c5299'), STATUS.ACCEPTED)

        self.payload_request1 = Payload('benefactor-key-hiuwehduiee2u8', 'beneficiary-key-d8923yr94fh3re', self.mortgage1, None,
                                   3, 0, 'prev-hash-benefactor-urc89utqhoird', '', '', '', 300)
        self.payload_response1 = Payload('benefactor-key-hiuwehduiee2u8', 'beneficiary-key-d8923yr94fh3re', self.mortgage1,
                                    self.mortgage1, 3, 2, 'prev-hash-benefactor-urc89utqhoird',
                                    'prev-hash-beneficiary-cru894yhfrri2', 'signature-benefactor-8397yhdi287r',
                                    'signature-beneficiary-e89ydughdb23', 300)

        self.payload_response_multiple_blocks1 = Payload('benefactor-key-0ed203rd2', 'beneficiary-key-jfwru9f3w8',
                                    self.investment1, self.investment1, 5, 4,
                                    'prev-hash-benefactor-ik12ei3', 'prev-hash-beneficiary-fj039r',
                                    'signature-benefactor-mdioaw030', 'signature-beneficiary-jfrkf29', 800)
        self.payload_response_multiple_blocks2 = Payload('benefactor-key-0ed203rd2', 'beneficiary-key-jfwru9f3w8',
                                                        self.investment1, self.investment1, 6, 5,
                                                        'prev-hash-benefactor-ik12ei38', 'prev-hash-beneficiary-fj039r8',
                                                        'signature-benefactor-mdioaw030',
                                                        'signature-beneficiary-jfrkf29', 900)

        self.payload_request_latest_hash = Payload('benefactor-key-i298w4yjexrw', 'beneficiary-key-d893dyt4rew', self.investment1, None,
                                   5, 0, 'prev-hash-benefactor-urc89utqhokp9', '', '', '', 600)
        self.payload_response_latest_hash = Payload('benefactor-key-i298w4yjexrw', 'beneficiary-key-d893dyt4rew',
                                    self.investment1, self.investment1, 5, 4,
                                    'prev-hash-benefactor-urc89utqhokp9', 'prev-hash-beneficiary-98eud284r',
                                    'signature-benefactor-eu8392ye', 'signature-beneficiary-eu8923yr', 600)

        self.payload_request_latest_hash_two_blocks1 = Payload('benefactor-key-i298w4yje5wd', 'beneficiary-key-d893djw9a83ry',
                                                   self.investment1, None,
                                                   5, 0, 'prev-hash-benefactor-urc89utf924f0fj', '', '', '', 400)
        self.payload_response_latest_hash_two_blocks1 = Payload('benefactor-key-i298w4yje5wd', 'beneficiary-key-d893djw9a83ry',
                                                    self.investment1, self.investment1, 5, 4,
                                                    'prev-hash-benefactor-urc89utf924f0fj',
                                                    'prev-hash-beneficiary-98eud284r9e0',
                                                    'signature-benefactor-eu8392ye', 'signature-beneficiary-eu8923yr',
                                                    400)

        self.payload_request_latest_hash_two_blocks2 = Payload('benefactor-key-i298w4yje5wd', 'beneficiary-key-d893djw9a83ry',
                                                   self.investment1, None,
                                                   8, 0, 'prev-hash-benefactor-93rudf9e8wjf', '', '', '', 900)
        self.payload_response_latest_hash_two_blocks2 = Payload('benefactor-key-i298w4yje5wd', 'beneficiary-key-d893djw9a83ry',
                                                    self.investment1, self.investment1, 8, 7,
                                                    'prev-hash-benefactor-93rudf9e8wjf',
                                                    'prev-hash-beneficiary-jcse09i3rgh',
                                                    'signature-benefactor-eu8392ye', 'signature-beneficiary-eu8923yr',
                                                    900)

        self.payload_request_latest_sequence_number = Payload('benefactor-key-i298w4y483xrw', 'beneficiary-key-d893dyt4rei920',
                                                   self.mortgage1, None,
                                                   8, 0, 'prev-hash-benefactor-urc89utqhokp9', '', '', '', 500)
        self.payload_response_latest_sequence_number = Payload('benefactor-key-i298w4y483xrw', 'beneficiary-key-d893dyt4rei920',
                                                    self.mortgage1, self.mortgage1,
                                                    8, 6, 'prev-hash-benefactor-urc89utqhokp9',
                                                    'prev-hash-beneficiary-dqf9df',
                                                    'signature-benefactor-ci90sje', 'signature-beneficiary-943uwr',
                                                    500)

    def test_from_signed_confirm_message(self):
        """
        This test checks the functionality of making a block with the payload from a message.
        """

        message = Message(self.payload_response1)
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

        message = Message(self.payload_response1)
        block = DatabaseBlock.from_signed_confirm_message(message)

        # Add the block to the blockchain
        self.db.add_block(block)
        # Get the block by the hash of the block
        result = self.db.get_by_hash(block.hash_block)

        # Check whether the block was added correctly
        self.assertEqualBlocks(block, result)

    def test_add_multiple_blocks(self):
        """
        This test checks the functionality of adding two blocks to the blockchain.
        """

        message1 = Message(self.payload_response_multiple_blocks1)
        message2 = Message(self.payload_response_multiple_blocks2)
        block1 = DatabaseBlock.from_signed_confirm_message(message1)
        block2 = DatabaseBlock.from_signed_confirm_message(message2)

        # Add the blocks to the blockchain
        self.db.add_block(block1)
        self.db.add_block(block2)

        # Get the blocks by the hash of the block
        result1 = self.db.get_by_hash(block1.hash_block)
        result2 = self.db.get_by_hash(block2.hash_block)

        # Get the latest hash
        latest_hash_benefactor = self.db.get_latest_hash(message1.payload.benefactor)
        latest_hash_beneficiary = self.db.get_latest_hash(message1.payload.beneficiary)

        # Check whether the blocks were added correctly
        self.assertEqualBlocks(block1, result1)
        self.assertEqualBlocks(block2, result2)
        self.assertNotEqual(block1.hash_block, block2.hash_block)
        self.assertEqual(latest_hash_benefactor, latest_hash_beneficiary)
        self.assertEqual(latest_hash_benefactor, block2.hash_block)
        self.assertEqual(latest_hash_beneficiary, block2.hash_block)
        self.assertNotEqual(latest_hash_benefactor, block1.hash_block)
        self.assertNotEqual(latest_hash_beneficiary, block1.hash_block)

    def test_update_block_with_beneficiary(self):
        """
        This test checks the functionality of updating a block in the blockchain.
        """

        message_request = Message(self.payload_request1)
        message_response = Message(self.payload_response1)

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

        message_request = Message(self.payload_request_latest_hash)
        message_response = Message(self.payload_response_latest_hash)

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
        #print "latest_hash_beneficiary = " + str(latest_hash_beneficiary)
        #print "latest_block_beneficiary.hash_block = " + str(latest_block_beneficiary.hash_block) # different one
        #print "latest_block_benefactor.hash_block = " + str(latest_block_benefactor.hash_block)
        #print "latest_hash_benefactor = " + str(latest_hash_benefactor)
        #print "block_beneficiary.hash_block = " + str(block_beneficiary.hash_block)

        self.assertEqual(latest_hash_benefactor, latest_block_benefactor.hash_block)
        self.assertEqual(latest_hash_beneficiary, latest_block_beneficiary.hash_block)
        self.assertEqual(latest_hash_benefactor, latest_hash_beneficiary)
        self.assertEqual(block_beneficiary.hash_block, latest_hash_benefactor)
        self.assertEqual(block_beneficiary.hash_block, latest_hash_beneficiary)

    def test_get_latest_hash_two_blocks(self):
        """
        This test checks the functionality of getting the latest hash of a user when two blocks are added.
        """

        # Add the first block
        message_request1 = Message(self.payload_request_latest_hash_two_blocks1)
        message_response1 = Message(self.payload_response_latest_hash_two_blocks1)
        # Add the block with only the information from benefactor to the blockchain
        block_benefactor1 = DatabaseBlock.from_signed_confirm_message(message_request1)
        self.db.add_block(block_benefactor1)
        # Update the block with the information from the beneficiary
        block_beneficiary1 = DatabaseBlock.from_signed_confirm_message(message_response1)
        self.db.update_block_with_beneficiary(block_beneficiary1)

        # Add the second block
        message_request2 = Message(self.payload_request_latest_hash_two_blocks2)
        message_response2 = Message(self.payload_response_latest_hash_two_blocks2)

        # Add the block with only the information from benefactor to the blockchain
        block_benefactor2 = DatabaseBlock.from_signed_confirm_message(message_request2)
        self.db.add_block(block_benefactor2)
        # Update the block with the information from the beneficiary
        block_beneficiary2 = DatabaseBlock.from_signed_confirm_message(message_response2)
        self.db.update_block_with_beneficiary(block_beneficiary2)

        # Get the latest block added
        latest_block_benefactor = self.db.get_by_public_key_and_sequence_number(message_request2.payload.benefactor,
                                                                                block_benefactor2.sequence_number_benefactor)
        latest_block_beneficiary = self.db.get_by_public_key_and_sequence_number(message_request2.payload.beneficiary,
                                                                                 block_beneficiary2.sequence_number_beneficiary)

        # Get the latest hash
        latest_hash_benefactor = self.db.get_latest_hash(message_request2.payload.benefactor)
        latest_hash_beneficiary = self.db.get_latest_hash(message_request2.payload.beneficiary)

        # Check whether the hash is the right one
        self.assertEqual(latest_hash_benefactor, latest_block_benefactor.hash_block)
        self.assertEqual(latest_hash_beneficiary, latest_block_beneficiary.hash_block)
        self.assertEqual(latest_hash_benefactor, latest_hash_beneficiary)
        self.assertEqual(block_beneficiary2.hash_block, latest_hash_benefactor)
        self.assertEqual(block_beneficiary2.hash_block, latest_hash_beneficiary)


    def test_get_latest_hash_nonexistent(self):
        """
        This test checks the functionality of getting a nonexistent latest hash.
        """

        self.assertEqual(self.db.get_latest_hash('benefactor-key-ey8391yuq3'), '')

    def test_get_latest_sequence_number(self):
        """
        This test checks the functionality of getting the latest sequence number
        """

        message_request = Message(self.payload_request_latest_sequence_number)
        message_response = Message(self.payload_response_latest_sequence_number)

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

    def test_get_latest_sequence_number_nonexistent(self):
        """
        This test checks the functionality of getting a nonexistent latest sequence number.
        """

        self.assertEqual(self.db.get_latest_sequence_number('benefactor-key-34892yrqwe'), 0)

    def tearDown(self):
        self.db.close()


class Payload(object):
    def __init__(self, benefactor, beneficiary, agreement_benefactor, agreement_beneficiary,
                 sequence_number_benefactor, sequence_number_beneficiary, previous_hash_benefactor,
                 previous_hash_beneficiary, signature_benefactor, signature_beneficiary, time):

        self._benefactor = benefactor
        self._beneficiary = beneficiary
        self._agreement_benefactor = agreement_benefactor
        self._agreement_beneficiary = agreement_beneficiary
        self._sequence_number_benefactor = sequence_number_benefactor
        self._sequence_number_beneficiary = sequence_number_beneficiary
        self._previous_hash_benefactor = previous_hash_benefactor
        self._previous_hash_beneficiary = previous_hash_beneficiary
        self._signature_benefactor = signature_benefactor
        self._signature_beneficiary = signature_beneficiary
        self._time = time

    @property
    def benefactor(self):
        return self._benefactor

    @property
    def beneficiary(self):
        return self._beneficiary

    @property
    def agreement_benefactor(self):
        return self._agreement_benefactor

    @property
    def agreement_beneficiary(self):
        return self._agreement_beneficiary

    @property
    def sequence_number_benefactor(self):
        return self._sequence_number_benefactor

    @property
    def sequence_number_beneficiary(self):
        return self._sequence_number_beneficiary

    @property
    def previous_hash_benefactor(self):
        return self._previous_hash_benefactor

    @property
    def previous_hash_beneficiary(self):
        return self._previous_hash_beneficiary

    @property
    def signature_benefactor(self):
        return self._signature_benefactor

    @property
    def signature_beneficiary(self):
        return self._signature_beneficiary

    @property
    def time(self):
        return self._time

class Message(object):
    def __init__(self, payload):
        self._payload = payload

    @property
    def payload(self):
        return self._payload