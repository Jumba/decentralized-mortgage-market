from threading import Lock

from market.dispersy.message import Message


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
        print "Message pushed: ", message
        assert isinstance(message[0], unicode)
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
                self._api.community.send_api_message_community(request, fields, models)
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

                self._api.community.send_api_message_candidate(request, fields, models, tuple(candidates))


class IncomingMessageQueue(MessageQueue):

    def push(self, message):
        self._lock.acquire()
        assert isinstance(message, Message.Implementation)
        self._queue.append(message)
        self._lock.release()

    def process(self):
        community = self._api.community

        for message in self._queue:
            payload = message.payload

            request = payload.request
            remove_message = False
            # Handle each message.
            if request == u"investment_offer":
                remove_message = community.on_investment_offer(payload);
            elif request == u"loan_request":
                remove_message = community.on_loan_request_receive(payload)
            elif request == u"mortgage_accept_signed":
                remove_message = community.on_mortgage_accept_signed(payload)
            elif request == u"mortgage_accept_unsigned":
                remove_message = community.on_mortgage_accept_unsigned(payload)
            elif request == u"investment_accept":
                remove_message = community.on_investment_accept(payload)
            elif request == u"mortgage_reject":
                remove_message = community.on_mortgage_reject(payload)
            elif request == u"investment_reject":
                remove_message = community.on_investment_reject(payload)
            elif request == u"mortgage_offer":
                remove_message = community.on_mortgage_offer(payload)
            elif request == u"loan_request_reject":
                remove_message = community.on_loan_request_reject(payload)
            else:
                # Unknow message request, throw it away
                remove_message = True

            if remove_message:
                self.pop(message)
