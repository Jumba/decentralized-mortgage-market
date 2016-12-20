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
        self.define_meta_message(chr(16), community.get_meta_message(u"signed_confirm"), self._encode_signed_confirm, self._decode_signed_confirm)


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

    def _encode_signed_confirm(self, message):
        packet = encode((message.payload.benefactor, message.payload.beneficiary, message.payload.agreement.encode(), message.payload.time))
        return packet,

    def _decode_signed_confirm(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the SignedConfirm-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        benefactor, beneficiary, agreement_encoded, time = payload
        if not isinstance(benefactor, str):
            raise DropPacket("Invalid 'benefactor' type")
        if not isinstance(beneficiary, str):
            raise DropPacket("Invalid 'beneficiary' type")
        if not isinstance(time, int):
            raise DropPacket("Invalid 'int' type")

        agreement = DatabaseModel.decode(agreement_encoded)
        if not isinstance(agreement, DatabaseModel):
            raise DropPacket("Invalid 'agreement' type")

        return offset, placeholder.meta.payload.implement(benefactor, beneficiary, agreement, time)


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

    def encode_block(payload, benefactor, beneficiary:
        """
        This function encodes a block.
        :param payload: Payload containing the data as properties, not including the benefactor and beneficiary data.
        for example a signature request/response payload.
        :param benefactor: The benefactor of the block as a dispersy member
        :param beneficiary: The beneficiary of the block as a dispersy member
        :return: encoding
        """
        # Test code sometimes run a different curve with a different key length resulting in hard to catch bugs.
        #assert len(benefactor[1].public_key) == PK_LENGTH
        #assert len(beneficiary[1].public_key) == PK_LENGTH
        return pack(crawl_response_format, *(payload.up, payload.down,
                                             payload.total_up_benefactor, payload.total_down_benefactor,
                                             payload.sequence_number_benefactor, payload.previous_hash_benefactor,
                                             payload.total_up_beneficiary, payload.total_down_beneficiary,
                                             payload.sequence_number_beneficiary, payload.previous_hash_beneficiary,
                                             benefactor[1].public_key, benefactor[0],
                                             beneficiary[1].public_key, beneficiary[0]))

    def encode_block_benefactor_half(payload, public_key_benefactor, public_key_beneficiary, signature_benefactor):
        return pack(benefactor_half_format, *(public_key_benefactor, public_key_beneficiary,
                                             payload.up, payload.down,
                                             payload.total_up_benefactor, payload.total_down_benefactor,
                                             payload.sequence_number_benefactor, payload.previous_hash_benefactor,
                                             signature_benefactor))
