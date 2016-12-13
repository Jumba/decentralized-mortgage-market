import logging

from conversion import MortgageMarketConversion
from market.dispersy.authentication import MemberAuthentication, DoubleMemberAuthentication
from market.dispersy.community import Community
from market.dispersy.conversion import DefaultConversion
from market.dispersy.destination import CommunityDestination, CandidateDestination
from market.dispersy.distribution import DirectDistribution
from market.dispersy.message import Message, DelayMessageByProof
from market.dispersy.resolution import PublicResolution
from market.models import DatabaseModel
from payload import DatabaseModelPayload
from twisted.internet import reactor
from market.models.loans import LoanRequest
from market.models.house import House
from market.models.profiles import Profile, BorrowersProfile

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)




class MortgageMarketCommunity(Community):

    @classmethod
    def get_master_members(cls, dispersy):
        master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040578e79f08d3270c5af04ace5b572ecf46eef54502c1" \
                     "4f3dc86f4cd29e86f05dad976b08da07b8d97d73fc8243459e09b6b208a2c8cbf6fdc7b78ae2668606388f39ef0fa715cf2" \
                     "104ad21f1846dd8f93bb25f2ce785cced2c9231466a302e5f9e0e70f72a3a912f2dae7a9a38a5e7d00eb7aef23eb42398c38" \
                     "59ffadb28ca28a1522addcaa9be4eec13095f48f7cf35".decode("HEX")

        master = dispersy.get_member(public_key=master_key)
        return [master]

    def __init__(self, dispersy, master, my_member):
        super(MortgageMarketCommunity, self).__init__(dispersy, master, my_member)
        self._api = None



    def initialize(self):
        super(MortgageMarketCommunity, self).initialize()
        logger.info("Example community initialized")

    def on_introduction_response(self, messages):
        super(MortgageMarketCommunity, self).on_introduction_response(messages)
        for message in messages:
            print "adding ", message.candidate
            #self.candidates.add(message.candidate)

    def initiate_meta_messages(self):
        return super(MortgageMarketCommunity, self).initiate_meta_messages() + [
            Message(self, u"loan_request",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_loan_request),
            Message(self, u"document",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_document),
            Message(self, u"loan_request_reject",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_loan_request_reject),
            Message(self, u"mortgage_offer",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_mortgage_offer),
            Message(self, u"mortgage_accept_signed",
                    DoubleMemberAuthentication(
                        allow_signature_func=self.allow_signature_request, split_payload_func=self.split_function),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_mortgage_accept_signed),
            Message(self, u"mortgage_accept_unsigned",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_mortgage_accept_signed),
            Message(self, u"mortgage_reject",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_mortgage_reject),
            Message(self, u"investment_offer",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_investment_offer),
            Message(self, u"investment_accept",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_investment_accept),
               Message(self, u"investment_reject",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_investment_reject),
            Message(self, u"model_request",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_model_request),
            Message(self, u"model_request_response",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_model_request_response),
        ]

    def initiate_conversions(self):
        return [DefaultConversion(self), MortgageMarketConversion(self)]

    def check_message(self, messages):
        for message in messages:
            allowed, _ = self._timeline.check(message)
            if allowed:
                yield message
            else:
                yield DelayMessageByProof(message)

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, api):
        self._api = api

    def send_direct_model(self, model, time, candidates, store=True, update=True, forward=True):
        logger.debug("sending direct model")
        meta = self.get_meta_message(u"databasemodel_direct")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            destination=tuple(candidates),
                            payload=(model, time,),
                            )

        self.dispersy.store_update_forward([message], store, update, forward)

    def send_community_model(self, model, time, store=True, update=True, forward=True):
        logger.debug("sending community model")
        meta = self.get_meta_message(u"databasemodel_flood")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(model,time,),)
        self.dispersy.store_update_forward([message], store, update, forward)
        
    def send_loan_request(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_document(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_loan_request_reject(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_mortgage_offer(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_mortgage_accept_signed(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_mortgage_accept_unsigned(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_mortgage_reject(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_investment_offer(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_investment_accept(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_investment_reject(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_model_request(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_model_request_respsendse(self, fields, models, store=True, update=True, forward=True):
        pass

    def on_model(self, messages):
        print "message in?"
        for message in messages:
            print message.payload.fields
            for field in message.payload.fields:
                print message.payload.models[field]

    def on_loan_request(self, messages):
        for message in messages:
            loan_request = message.payload.models[LoanRequest._type]
            house = message.payload.models[House._type]
            profile = message.payload.models[BorrowersProfile._type]

            self.db.post(LoanRequest._type, loan_request)
            self.db.post(House._type, house)
            self.db.post(BorrowersProfile._type, profile)

    def on_document(self, messages):
        pass

    def on_loan_request_reject(self, messages):
        pass

    def on_mortgage_offer(self, messages):
        pass

    def on_mortgage_accept_signed(self, messages):
        pass

    def on_mortgage_accept_unsigned(self, messages):
        pass

    def on_mortgage_reject(self, messages):
        pass

    def on_investment_offer(self, messages):
        pass

    def on_investment_accept(self, messages):
        pass

    def on_investment_reject(self, messages):
        pass

    def on_model_request(self, messages):
        pass

    def on_model_request_response(self, messages):
        pass

    def allow_signature_request(self):
        pass

    def split_function(self):
        pass