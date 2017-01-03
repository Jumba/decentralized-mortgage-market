import unittest
from twisted.python.threadable import registerAsIOThread

from dispersy.dispersy import Dispersy
from dispersy.member import DummyMember, Member

from dispersy.endpoint import ManualEnpoint
from market.api.api import MarketAPI
from market.community.community import MortgageMarketCommunity
from market.community.conversion import MortgageMarketConversion
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.models.house import House
from market.models.loans import LoanRequest
from market.models.profiles import BorrowersProfile
from market.models.user import User


class FakePayload(object):
    fields = []
    models = {}

class CommunityTestSuite(unittest.TestCase):
    """Conversion test cases."""

    def setUp(self):
        # Faking IOThread
        registerAsIOThread()

        # Object creation and preperation
        self.dispersy = Dispersy(ManualEnpoint(0), unicode("dispersy_temporary"))
        self.api = MarketAPI(MockDatabase(MemoryBackend()))
        self.api.db.backend.clear()

        user, _, priv = self.api.create_user()
        self.user = user
        self.private_key = priv

        self.dispersy._database.open()
        self.master_member = DummyMember(self.dispersy, 1, "a" * 20)
        self.member = self.dispersy.get_member(private_key=self.private_key.decode("HEX"))
        self.community = MortgageMarketCommunity.init_community(self.dispersy, self.master_member, self.member)

        self.community.api = self.api
        self.community.user = self.user
        self.api.community = self.community

        # Add our conversion to the community.
        self.conversion = MortgageMarketConversion(self.community)
        self.community._conversions = []
        self.community.add_conversion(self.conversion)

        self.setupModels()

    def setupModels(self):
        self.house = House('2500AA', '34', 'Aa Weg', 1000)
        self.house.post_or_put(self.api.db)

        self.loan_request = LoanRequest(user_key=self.user.id,
                                        house_id=self.house.id,
                                        house_link='http://www.example.com',
                                        seller_phone_number='06000000',
                                        seller_email='example@email.com',
                                        mortgage_type=1,
                                        banks=[],
                                        description=u'Unicode description',
                                        amount_wanted=10000,
                                        status={}
                                        )
        self.loan_request.post_or_put(self.api.db)
        self.profile = BorrowersProfile(first_name=u'Jebediah', last_name=u'Kerman', email='exmaple@asdsa.com', iban='sadasdas', phone_number='213131', current_postal_code='2312AA',
                                        current_house_number='2132', current_address='Damstraat 1', document_list=[])
        self.profile.post_or_put(self.api.db)

    def isModelInDB(self, model):
        return not self.api.db.get(model.type, model.id) is None

    def remove_from_db(self, model):
        self.api.db.backend.delete(model)

    def remove_payload_models_from_db(self, payload):
        for key in payload.models:
            self.remove_from_db(payload.models[key])


    def test_init(self):
        self.assertIsInstance(self.conversion, MortgageMarketConversion)
        self.assertIsInstance(self.community, MortgageMarketCommunity)
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.member, Member)
        self.assertEqual(self.user.id, self.member.public_key.encode("HEX"))

    def test_on_loan_request_receive(self):
        payload = FakePayload()
        payload.models = {self.house.type: self.house, self.loan_request.type: self.loan_request,
                          self.user.type: self.user, self.profile.type: self.profile}

        # Remove the models to act as a remote peer with none of the models saved.
        self.remove_payload_models_from_db(payload)

        self.assertFalse(self.isModelInDB(self.loan_request))
        self.assertFalse(self.isModelInDB(self.profile))
        self.assertFalse(self.isModelInDB(self.house))

        self.community.on_loan_request_receive(payload)
        
        self.assertTrue(self.isModelInDB(self.loan_request))
        self.assertTrue(self.isModelInDB(self.profile))
        self.assertTrue(self.isModelInDB(self.house))

        
        

    def tearDown(self):
        # Closing and unlocking dispersy database for other tests in test suite
        self.dispersy._database.close()



if __name__ == '__main__':
    unittest.main()
