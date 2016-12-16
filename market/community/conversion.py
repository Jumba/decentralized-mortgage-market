from market.community.encoding import encode, decode
from market.dispersy.conversion import BinaryConversion
from market.dispersy.message import DropPacket
from market.models import DatabaseModel


class MortgageMarketConversion(BinaryConversion):
    def __init__(self, community):
        super(MortgageMarketConversion, self).__init__(community, "\x03")
        self.define_meta_message(chr(11), community.get_meta_message(u"model_request"), self._encode_model_request, self._decode_model_request)
        self.define_meta_message(chr(12), community.get_meta_message(u"model_request_response"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(13), community.get_meta_message(u"introduce_user"), self._encode_model, self._decode_model)
        self.define_meta_message(chr(14), community.get_meta_message(u"api_message_community"), self._encode_api_message, self._decode_api_message)
        self.define_meta_message(chr(15), community.get_meta_message(u"api_message_candidate"), self._encode_api_message, self._decode_api_message)

    def _encode_api_message(self, message):
        encoded_models = dict()

        for field in message.payload.fields:
            encoded_models[field] = message.payload.models[field].encode()

        packet = encode((message.payload.request, message.payload.fields, encoded_models))
        return packet,

    def _decode_api_message(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the example-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        request, fields, encoded_models = payload
        if not isinstance(request, unicode):
            raise DropPacket("Invalid 'request' type")
        if not isinstance(fields, list):
            raise DropPacket("Invalid 'fields' type")
        if not isinstance(encoded_models, dict):
            raise DropPacket("Invalid 'models' type")

        decoded_models = dict()
        for field in fields:
            decoded_models[field] = DatabaseModel.decode(encoded_models[field])

        return offset, placeholder.meta.payload.implement(request, fields, decoded_models)

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
            raise DropPacket("Unable to decode the model payload")

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
        packet = encode((message.payload.models,))
        return packet,

    def _decode_model_request(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the model request payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        models = payload[0]
        if not isinstance(models, list):
            raise DropPacket("Invalid 'models' type")

        return offset, placeholder.meta.payload.implement(models)
