import logging

from conversion import MortgageMarketConversion
from market import Global
from market.dispersy.authentication import MemberAuthentication, DoubleMemberAuthentication
from market.dispersy.community import Community
from market.dispersy.conversion import DefaultConversion
from market.dispersy.destination import CommunityDestination, CandidateDestination
from market.dispersy.distribution import DirectDistribution
from market.dispersy.message import Message, DelayMessageByProof
from market.dispersy.resolution import PublicResolution
from market.models import DatabaseModel
from market.models.user import User
from payload import DatabaseModelPayload, ModelRequestPayload
from market.models.loans import LoanRequest, Mortgage, Campaign, Investment
from market.models.house import House
from market.models.profiles import BorrowersProfile
from market.models.document import Document

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
        self._user = None


    def initialize(self):
        super(MortgageMarketCommunity, self).initialize()
        logger.info("Example community initialized")

    def on_introduction_response(self, messages):
        super(MortgageMarketCommunity, self).on_introduction_response(messages)
        for message in messages:
            self.send_introduce_user(['user',], {'user': self.user}, message.candidate)

    def initiate_meta_messages(self):
        return super(MortgageMarketCommunity, self).initiate_meta_messages() + [
            Message(self, u"document",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CommunityDestination(node_count=50),
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
                    CommunityDestination(node_count=50),
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
                    CommunityDestination(node_count=50),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_investment_reject),
            Message(self, u"model_request",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CommunityDestination(node_count=50),
                    ModelRequestPayload(),
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
            Message(self, u"introduce_user",
                MemberAuthentication(),
                PublicResolution(),
                DirectDistribution(),
                CandidateDestination(),
                DatabaseModelPayload(),
                self.check_message,
                self.on_user_introduction),
            Message(self, u"loan_request",
                    MemberAuthentication(),
                    PublicResolution(),
                    DirectDistribution(),
                    CandidateDestination(),
                    DatabaseModelPayload(),
                    self.check_message,
                    self.on_loan_request_receive),
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

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    def send_loan_request(self, fields, models, candidates, store=True, update=True, forward=True):
        assert LoanRequest._type in fields and LoanRequest._type in models
        assert House._type in fields and House._type in models
        assert BorrowersProfile._type in fields and BorrowersProfile._type in models

        meta = self.get_meta_message(u"loan_request")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)

    def send_document(self, fields, models, candidates, store=True, update=True, forward=True):
        for field in fields:
            assert isinstance(models[field], Document)
        print "Document being sent"
        meta = self.get_meta_message(u"document")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),)
                            #destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)
        print "Stored for sending"

    def send_loan_request_reject(self, fields, models, candidates, store=True, update=True, forward=True):
        assert LoanRequest._type in fields and LoanRequest._type in models

        meta = self.get_meta_message(u"loan_request_reject")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)

    def send_document_message(self, fields, models, candidates, store=True, update=True, forward=True):
        print "Sending document"
        meta = self.get_meta_message(u"send_document")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)


    def send_mortgage_offer(self, fields, models, candidates, store=True, update=True, forward=True):
        assert LoanRequest._type in fields and LoanRequest._type in models
        assert Mortgage._type in fields and Mortgage._type in models

        meta = self.get_meta_message(u"mortgage_offer")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)


    def send_mortgage_accept_signed(self, fields, models, store=True, update=True, forward=True):
        pass

    def send_mortgage_accept_unsigned(self, fields, models, store=True, update=True, forward=True):
        assert Campaign._type in fields and Campaign._type in models
        assert Mortgage._type in fields and Mortgage._type in models

        meta = self.get_meta_message(u"mortgage_accept_unsigned")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),)
        self.dispersy.store_update_forward([message], store, update, forward)

    def send_mortgage_reject(self, fields, models, candidates, store=True, update=True, forward=True):
        assert Mortgage.type in fields and Mortgage._type in models

        meta = self.get_meta_message(u"mortgage_reject")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)


    def send_investment_offer(self, fields, models, store=True, update=True, forward=True):
        pass # TODO: Ignore signed for now

    def send_investment_accept(self, fields, models, store=True, update=True, forward=True):
        pass # TODO: Ignore singned for now

    def send_investment_reject(self, fields, models, store=True, update=True, forward=True):
        assert Investment._type in fields and Investment._type in models

        meta = self.get_meta_message(u"investment_reject")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),)
        self.dispersy.store_update_forward([message], store, update, forward)


    def send_model_request(self, models, store=True, update=True, forward=True):
        assert isinstance(models, list)

        meta = self.get_meta_message(u"model_request")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(models,),)
        self.dispersy.store_update_forward([message], store, update, forward)

    def send_model_request_response(self, fields, models, candidates, store=True, update=True, forward=True):
        for field in fields:
            assert isinstance(models[field], DatabaseModel)

        meta = self.get_meta_message(u"model_request_response")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=candidates)
        self.dispersy.store_update_forward([message], store, update, forward)

    def send_introduce_user(self, fields, models, candidate, store=True, update=True, forward=True):
        for field in fields:
            assert isinstance(models[field], DatabaseModel)

        meta = self.get_meta_message(u"introduce_user")
        message = meta.impl(authentication=(self.my_member,),
                            distribution=(self.claim_global_time(),),
                            payload=(fields, models,),
                            destination=(candidate, ))
        self.dispersy.store_update_forward([message], store, update, forward)

    def on_loan_request_receive(self, messages):
        for message in messages:
            for field in message.payload.fields:
                obj = message.payload.models[field]
                self.api.db.post(obj.type, obj), obj

                # Save the loan request to the bank
                if isinstance(obj, LoanRequest):
                    if self.user.id in obj.banks:
                        self.user.update(self.api.db)
                        self.user.loan_request_ids.append(obj.id)
                        self.api.db.put(self.user.type, self.user.id, self.user)
                        print "Loan request saved to me (bank)"

    def on_document(self, messages):
        for message in messages:
            document = message.payload.models[Document._type]
            print "Received document ", document
            self.db.post(Document._type, document)

    def on_loan_request_reject(self, messages):
        for message in messages:
            loan_request = message.payload.models[LoanRequest._type]

            self.db.post(LoanRequest._type, loan_request)

    def on_mortgage_offer(self, messages):
        for message in messages:
            loan_request = message.payload.models[LoanRequest._type]
            mortgage = message.payload.models[Mortgage._type]

            self.db.post(Mortgage._type, mortgage)

    def on_mortgage_accept_signed(self, messages):
        for message in messages:
            mortgage = message.payload.models[Mortgage._type]
            campaign = message.payload.models[Campaign._type]

            self.db.post(Mortgage._type, mortgage)
            self.db.post(Campaign._type, campaign)

    def on_mortgage_accept_unsigned(self, messages):
        for message in messages:
            mortgage = message.payload.models[Mortgage._type]
            campaign = message.payload.models[Campaign._type]

            self.api.db.post(Mortgage._type, mortgage)
            self.api.db.post(Campaign._type, campaign)

    def on_mortgage_reject(self, messages):
        for message in messages:
            mortgage = message.payload.models[Mortgage._type]

            self.api.db.post(Mortgage._type, mortgage)

    def on_investment_offer(self, messages):
        for message in messages:
            investment = message.payload.models[Investment._type]

            self.api.db.post(Investment._type, investment)

    def on_investment_accept(self, messages):
        for message in messages:
            investment = message.payload.models[Investment._type]

            self.api.db.post(Investment._type, investment)

    def on_investment_reject(self, messages):
        for message in messages:
            investment = message.payload.models[Investment._type]

            self.api.db.post(Investment._type, investment)

    def on_model_request(self, messages):
        for message in messages:
            # Payload is a dictionary with {type : uuid}
            for model_type, model_id in message.payload.models:
                obj = self.api.db.get(model_type, model_id)
                self.send_model_request_response([obj.id], {obj.id: obj})

    def on_model_request_response(self, messages):
        for message in messages:
            for field in message.payload.fields:
                obj = message.payload.models[field]
                self.api.db.post(obj.type, obj)

    def on_user_introduction(self, messages):
        for message in messages:
            for field in message.payload.fields:
                obj = message.payload.models[field]
                if isinstance(obj, User) and not obj == self.user:
                    # Banks need to be overwritten
                    if obj.role_id == 3:
                        self.api.db.put(obj.type, obj.id, obj)
                    else:
                        self.api.db.post(obj.type, obj)

                    # Add the candidate at the end to prevent a race condition where a message containing the user may be sent
                    # before the model is saved.
                    self.api.user_candidate[obj.id] = message.candidate



    def allow_signature_request(self):
        pass

    def split_function(self):
        pass