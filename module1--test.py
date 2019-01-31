
class OriginalClass(object):
    def __new__(cls, *args, **kwargs):
        print(cls)

a = OriginalClass()
