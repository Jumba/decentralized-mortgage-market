from threading import Lock

from dispersy.message import Message
from market.api import APIMessage


class MessageQueue(object):
    """
    Message queues for handling incoming and outgoing `api_message_*` messages.
    """
    def __init__(self, api):
        self._api = api
        self._queue = []
        self._lock = Lock()

    def push(self, message):
        raise NotImplementedError

    def pop(self, message):
        self._lock.acquire()
        self._queue.remove(message)
        self._lock.release()

    def process(self):
        raise NotImplementedError


class OutgoingMessageQueue(MessageQueue):

    def push(self, message):
        assert isinstance(message[0], APIMessage)
        assert isinstance(message[1], list)
        assert isinstance(message[2], dict)
        assert isinstance(message[3], list)

        self._lock.acquire()
        self._queue.append(message)
        self._lock.release()

    def process(self):
        for message in self._queue:
            request, fields, models, receivers = message

            # if receivers is an empty list it's a community message
            if len(receivers) == 0:
                self._api.community.send_api_message_community(request.value, fields, models)
                self.pop(message)
            else:
                candidates = []
                for user in receivers:
                    if user.id in self._api.user_candidate:
                        candidates.append(self._api.user_candidate[user.id])
                        message[3].remove(user)

                # Remove the message if all receivers were found
                if len(message[3]) == 0:
                    self.pop(message)

                self._api.community.send_api_message_candidate(request.value, fields, models, tuple(candidates))


class IncomingMessageQueue(MessageQueue):

    def __init__(self, api):
        # Set the handler to None which stops processing messages until the handlers are assigned.
        self.handler = None
        super(IncomingMessageQueue, self).__init__(api)

    def assign_message_handlers(self, community):
        # Assign the handlers.
        self.handler = {
            APIMessage.INVESTMENT_OFFER: community.on_investment_offer,
            APIMessage.LOAN_REQUEST: community.on_loan_request_receive,
            APIMessage.MORTGAGE_ACCEPT_SIGNED: community.on_mortgage_accept_signed,
            APIMessage.MORTGAGE_ACCEPT_UNSIGNED: community.on_mortgage_accept_unsigned,
            APIMessage.INVESTMENT_ACCEPT: community.on_investment_accept,
            APIMessage.MORTGAGE_REJECT: community.on_mortgage_reject,
            APIMessage.INVESTMENT_REJECT: community.on_investment_reject,
            APIMessage.MORTGAGE_OFFER: community.on_mortgage_offer,
            APIMessage.LOAN_REQUEST_REJECT: community.on_loan_request_reject,
            APIMessage.CAMPAIGN_BID: community.on_campaign_bid,
        }
        

    def push(self, message):
        self._lock.acquire()
        assert isinstance(message, Message.Implementation)
        self._queue.append(message)
        self._lock.release()

    def process(self):
        if self.handler:
            for message in self._queue:
                payload = message.payload
                remove_message = False
                try:
                    request = APIMessage(payload.request)
                    # Handle each message.
                    if request in self.handler:
                        remove_message = self.handler[request](payload)
                    else:
                        remove_message = True
                except ValueError:
                    # Unknow message request, throw it away
                    remove_message = True

                if remove_message:
                    self.pop(message)
