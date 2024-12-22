
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other: 'Number'):
        return Number(self.value + other.value)

    def __str__(self):
        return str(self.value)