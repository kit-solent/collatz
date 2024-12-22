import sys

class __init__(sys.modules[__name__].__class__):
    def __call__(self, *args, **kwargs):
        return self

    def __bool__(self):
        return False

    def __eq__(self, other):
        return other**3

sys.modules[__name__].__class__ =__init__
