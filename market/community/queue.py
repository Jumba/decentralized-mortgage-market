import community

class MessageQueue():
    def __init__(self, api):
        self._api = api
        self._queue = []

    def add_message(self, message_name, fields, models, receivers):
        message = [message_name, fields, models, receivers]
        self._queue.append(message)

    def send_messages(self):

        for message in self._queue:
            message_name, fields, models, receivers = message

            # if receivers is an empty list it's a community message
            if len(receivers) == 0:
                message_name(fields, models, ())
                self._queue.remove(message)
            else:
                candidates = []
                for user in receivers:
                    if user.id in self._api.user_candidate:
                        candidates.append(self._api.user_candidate[user.id])
                        message[3].remove(user)

                # Remove the message if all receivers were found
                if len(message[3]) == 0:
                    self._queue.remove(message)

                message_name(fields, models, tuple(candidates))




