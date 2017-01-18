from dispersy.conversion import BinaryConversion
from dispersy.conversion import DropPacket
from market.community.encoding import encode, decode
from market.models import DatabaseModel


class MortgageMarketConversion(BinaryConversion):
    def __init__(self, community):
        super(MortgageMarketConversion, self).__init__(community, "\x04")
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
        if not isinstance(request, int):
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
        packet = encode(
                (
                    message.payload.benefactor,
                    message.payload.beneficiary,
                    message.payload.agreement_benefactor.encode(),
                    message.payload.agreement_beneficiary and message.payload.agreement_beneficiary.encode() or "",
                    message.payload.sequence_number_benefactor,
                    message.payload.sequence_number_beneficiary,
                    message.payload.previous_hash_benefactor,
                    message.payload.previous_hash_beneficiary,
                    message.payload.signature_benefactor,
                    message.payload.signature_beneficiary,
                    message.payload.insert_time
                 )
                )
        return packet,


    def _decode_signed_confirm(self, placeholder, offset, data):
        try:
            offset, payload = decode(data, offset)
        except ValueError:
            raise DropPacket("Unable to decode the SignedConfirm-payload")

        if not isinstance(payload, tuple):
            raise DropPacket("Invalid payload type")

        # benefactor, 0
        # beneficiary, 1
        # agreement_benefactor_encoded, 2
        # agreement_beneficiary_encoded, 3
        # sequence_number_benefactor, 4
        # sequence_number_beneficiary, 5
        # previous_hash_benefactor, 6
        # previous_hash_beneficiary, 7
        # signature_benefactor, 8
        # signature_beneficiary, 9
        # insert_time 10

        if not isinstance(payload[0], str):
            raise DropPacket("Invalid 'benefactor' type")
        if not isinstance(payload[1], str):
            raise DropPacket("Invalid 'beneficiary' type")
        #TODO: Do the rest.

        agreement_benefactor = DatabaseModel.decode(payload[2])
        agreement_beneficiary = DatabaseModel.decode(payload[3])

        return offset, placeholder.meta.payload.implement(
            payload[0],
            payload[1],
            agreement_benefactor,
            agreement_beneficiary,
            payload[4],
            payload[5],
            payload[6],
            payload[7],
            payload[8],
            payload[9],
            payload[10],
        )


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


