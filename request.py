class Request(object):

    def __init__(self):
        self.uri = ""
        self.version = "1.1"
        self.method = None
        self.headers = {}
        self.body = []

        self.__query_string = {}

    @property
    def url(self):
        return self.uri.split("?", 1)[0]

    def query_string_parameters(self):
        try:
            query_string = self.uri.split("?", 1)[1]
            for string in query_string.split("&"):
                parameters = string.split("=", 1)
                name, value = parameters if len(parameters) == 2 else parameters.append("")
                self.__query_string.update({name: value})
        except IndexError:
            pass

    @property
    def query_string(self):
        self.query_string_parameters()
        return self.__query_string
