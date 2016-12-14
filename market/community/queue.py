import community

class MessageQueue():
    def __init__(self):
        self._queue = []

    def add_message(self, message_name, fields, models, receivers):
        message = [message_name, fields, models, receivers]
        self._queue.append(message)

    def send_message(self, message, message_name):
        [message_name, fields, models, receivers] = message

        # TODO Check for candidate
        if True:
            self._queue.remove(message)
            message_name(fields, models, receivers, True, True, True)
        # no candidate
        else:
            pass