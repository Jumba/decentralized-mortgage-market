import time
import unittest
from twisted.python.threadable import registerAsIOThread
from uuid import UUID

from dispersy.candidate import LoopbackCandidate
from dispersy.dispersy import Dispersy
from dispersy.endpoint import ManualEnpoint
from dispersy.member import DummyMember
from market.api.api import STATUS, MarketAPI
from market.community.community import MortgageMarketCommunity
from market.database.backends import PersistentBackend
from market.database.database import MockDatabase
from market.models import DatabaseModel
from market.models.loans import Mortgage
from market.database.backends import DatabaseBlock


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
    """
    Tests the blockchain functionality.

    PersistentBackend is neccesary as the MemoryBackend does not implement BlockChain!
    """

    def setUp(self):
        # Faking IOThread
        registerAsIOThread()

        # Object creation and preperation
        self.dispersy = Dispersy(ManualEnpoint(0), unicode("dispersy_temporary_mc1"))
        self.dispersy_bank = Dispersy(ManualEnpoint(0), unicode("dispersy_temporary_mc2"))

        self.api = MarketAPI(MockDatabase(PersistentBackend('.', u'borrower.db')))
        self.api_bank = MarketAPI(MockDatabase(PersistentBackend('.', u'bank.db')))

        self.api.db.backend.clear()
        self.api_bank.db.backend.clear()

        self.user, _, priv_user = self.api.create_user()
        self.bank, _, priv_bank = self.api_bank.create_user()

        self.dispersy._database.open()
        self.dispersy_bank._database.open()

        self.master_member = DummyMember(self.dispersy, 1, "a" * 20)

        self.member = self.dispersy.get_member(private_key=priv_user.decode("HEX"))
        self.member_bank = self.dispersy_bank.get_member(private_key=priv_bank.decode("HEX"))

        self.community = MortgageMarketCommunity.init_community(self.dispersy, self.master_member, self.member)
        self.community_bank = MortgageMarketCommunity.init_community(self.dispersy_bank, self.master_member,
                                                                     self.member_bank)

        self.community.api = self.api
        self.community.user = self.user
        self.api.community = self.community

        self.community_bank.api = self.api_bank
        self.community_bank.user = self.bank
        self.api_bank.community = self.community_bank

        self.db = self.api.db.backend
        self.bank_db = self.api_bank.db.backend

        self.community.persistence = self.db
        self.community_bank.persistence = self.bank_db

        # Models
        self.mortgage = Mortgage(UUID('b97dfa1c-e125-4ded-9b1a-5066462c529c'),
                                 UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'),
                                 'ING', 80000, 1, 2.5, 1.5, 2.5, 36, 'A', [], STATUS.ACCEPTED)
        t = int(time.time())
        self.payload = (
            self.bank.id,
            self.user.id,
            self.mortgage,
            self.mortgage,
            2,
            1,
            'prev_hash_bene',
            'prev_hash_beni',
            'sig_bene',
            'sig_beni',
            t,
        )

        self.payload2 = (
            self.bank.id,
            '',
            self.mortgage,
            None,
            2,
            1,
            'prev_hash_bene',
            '',
            'sig_bene',
            '',
            t,
        )

    def test_from_signed_confirmed(self):
        """
        This test checks the functionality of making a block with the payload from a message.
        """
        meta = self.community.get_meta_message(u"signed_confirm")
        message = meta.impl(authentication=([self.member, self.member_bank],),
                            distribution=(self.community.claim_global_time(),),
                            payload=self.payload,
                            destination=(LoopbackCandidate(),))

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

    def test_add_get(self):
        """
        This test checks the functionality of adding a block to the blockchain then retrieving it.
        """

        meta = self.community.get_meta_message(u"signed_confirm")
        message = meta.impl(authentication=([self.member, self.member_bank],),
                            distribution=(self.community.claim_global_time(),),
                            payload=self.payload,
                            destination=(LoopbackCandidate(),))
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

        meta = self.community.get_meta_message(u"signed_confirm")
        message1 = meta.impl(authentication=([self.member, self.member_bank],),
                             distribution=(self.community.claim_global_time(),),
                             payload=self.payload,
                             destination=(LoopbackCandidate(),))

        message2 = meta.impl(authentication=([self.member, self.member_bank],),
                             distribution=(self.community.claim_global_time(),),
                             payload=self.payload2,
                             destination=(LoopbackCandidate(),))

        block1 = DatabaseBlock.from_signed_confirm_message(message1)
        block2 = DatabaseBlock.from_signed_confirm_message(message2)

        # Add the blocks to the blockchain
        self.db.add_block(block1)
        self.bank_db.add_block(block1)

        self.db.add_block(block2)
        self.bank_db.add_block(block2)

        # Get the blocks by the hash of the block
        result1 = self.db.get_by_hash(block1.hash_block)
        result2 = self.db.get_by_hash(block2.hash_block)

        # Get the latest hash
        latest_hash_benefactor = self.db.get_latest_hash()
        latest_hash_beneficiary = self.bank_db.get_latest_hash()

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

        meta = self.community.get_meta_message(u"signed_confirm")
        message_no_ben = meta.impl(authentication=([self.member, self.member_bank],),
                                   distribution=(self.community.claim_global_time(),),
                                   payload=self.payload2,
                                   destination=(LoopbackCandidate(),))

        message_ben = meta.impl(authentication=([self.member, self.member_bank],),
                                distribution=(self.community.claim_global_time(),),
                                payload=self.payload,
                                destination=(LoopbackCandidate(),))

        # Add the block with only the information from benefactor to the blockchain
        self.community.persist_signature(message_no_ben)
        # Create the block manually for assertions
        block_benefactor = DatabaseBlock.from_signed_confirm_message(message_no_ben)

        # Update the block with the information from the beneficiary
        self.community.update_signature(message_ben)
        # Create the block manually for assertions
        block_beneficiary = DatabaseBlock.from_signed_confirm_message(message_ben)

        # Get the updated block by the hash of the block
        result = self.db.get_by_hash(block_beneficiary.hash_block)

        self.assertEqualBlocks(block_beneficiary, result)
        # Get the updated block by the public key and the sequence number
        result_benefactor = self.db.get_by_public_key_and_sequence_number(message_ben.payload.benefactor,
                                                                          block_benefactor.sequence_number_benefactor)
        result_beneficiary = self.db.get_by_public_key_and_sequence_number(message_ben.payload.beneficiary,
                                                                           block_beneficiary.sequence_number_beneficiary)

        # Check whether the block was updated correctly
        self.assertEqualBlocks(result_benefactor, result_beneficiary)
        self.assertEqualBlocks(result_benefactor, result)
        self.assertEqualBlocks(result_beneficiary, result)

    def tearDown(self):
        self.dispersy._database.close()
        self.dispersy_bank._database.close()
        self.api.db.backend.close()
        self.api_bank.db.backend.close()
