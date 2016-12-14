class MessageQueue():
    def __init__(self):
        self._queue = []

    def add_message(self, message_name, fields, models, receivers):
        message = [message_name, fields, models, receivers]
        self._queue.append(message)

    # TODO Figure out how to tell when a message is sent
    def send_message(self, message):
        pass