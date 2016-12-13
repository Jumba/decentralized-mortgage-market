from Tribler.Core.Utilities.encoding import encode, decode
from market.dispersy.conversion import BinaryConversion
from market.dispersy.message import DropPacket
from market.models import DatabaseModel


class MortgageMarketConversion(BinaryConversion):

    def __init__(self, community):
        super(MortgageMarketConversion, self).__init__(community, "\x01")
        self.define_meta_message(chr(1), community.get_meta_message(u"loan_request"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(2), community.get_meta_message(u"document"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(3), community.get_meta_message(u"loan_request_reject"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(4), community.get_meta_message(u"mortgage_offer"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(5), community.get_meta_message(u"mortgage_accept_signed"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(6), community.get_meta_message(u"mortgage_accept_unsigned"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(7), community.get_meta_message(u"mortgage_reject"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(8), community.get_meta_message(u"investment_offer"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(9), community.get_meta_message(u"investment_accept"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(10), community.get_meta_message(u"investment_reject"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(11), community.get_meta_message(u"model_request"), self._encode_model_request, self._decode_model_request)
        self.define_meta_message(chr(12), community.get_meta_message(u"model_request_response"), self._encode_model, self._decode_model)



    def _encode_model(self, message):
        encoded_models = dict()

        for field in message.payload.fields:
            encoded_models[field] = message.payload.models[field].encode()

        packet = encode((message.payload.fields, encoded_models))
        return packet,

    def _decode_model(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the example-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        fields, encoded_models = payload
        if not isinstance(fields, list):
            raise DropPacket("Invalid 'fields' type")
        if not isinstance(encoded_models, dict):
            raise DropPacket("Invalid 'models' type")

        decoded_models = dict()
        for field in fields:
            decoded_models[field] = DatabaseModel.decode(encoded_models[field])

        return offset, placeholder.meta.payload.implement(fields, decoded_models)

    def _encode_model_request(self, message):
        packet = encode((message.payloads.models, ))
        return packet

    def _decode_model_request(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the model request payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        models = payload
        if not isinstance(models, list):
            raise DropPacket("Invalid 'models' type")

        return offset, placeholder.meta.payload.implement(models)
