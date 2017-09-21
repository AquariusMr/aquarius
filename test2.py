class Test(object):

    __slots__ = ("name", "_Test__string")

    def __init__(self, name):
        self.name = name
        self.__string = "s"

    @property
    def url(self):
        return "sss"

a = Test("shihongguang")

class Test1(Test):
    pass

b = Test1("ss")

print(Test.__dict__)