class Response:
    """
    Response class
    """
    msg = None
    code = None
    data = None

    def __init__(self, msg='success', code=200, data=None):
        self.msg = msg
        self.code = code
        self.data = data
