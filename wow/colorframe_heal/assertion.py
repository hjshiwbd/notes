def state(condition, message):
    if not condition:
        raise MinorException(message)


class MinorException(Exception):
    def __init__(self, message):
        self.message = message
