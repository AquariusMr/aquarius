class Request(object):

    __slots__ = ("uri", "version", "method", "headers", "body", "has_token")

    def __init__(self):
        self.uri = ""
        self.version = "1.1"
        self.method = ""
        self.headers = {}
        self.body = []

        self.has_token = False

    @property
    def url(self):
        return self.uri.split("?", 1)[0]

    def __query_string_parameters(self):
        _query_string = {}

        try:
            query_string = self.uri.split("?", 1)[1]
            for string in query_string.split("&"):
                parameters = string.split("=", 1)
                name, value = parameters if len(parameters) == 2 else parameters.append("")
                _query_string.update({name: value})
        finally:
            return _query_string

    @property
    def request_args(self):
        return self.__query_string_parameters()
