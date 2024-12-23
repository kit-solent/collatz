
class Number():
    def __init__(self, value:int|str|bytes|'Number'):
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f'Failed to convert value: {value} of type: {type(value)} to type int.')

        if value < 1:
            raise ValueError('Value must be greater than 0.')

        self.value = value

    #region operators
    # +
    def __add__(self, other):
        other = Number(other)

        # no validation required.

        return Number(self.value + other.value)

    # -
    def __sub__(self, other):
        other = Number(other)

        if self.value < other.value:
            raise ValueError('The result of the subtraction is less than 0.')

        return Number(self.value - other.value)

    # *
    def __mul__(self, other):
        other = Number(other)

        # no validation required.

        return Number(self.value * other.value)

    # /
    def __truediv__(self, other):
        other = Number(other)

        if self.value % other.value != 0:
            raise ValueError('The result of the division is not an integer.')

        return Number(self.value / other.value)

    # //
    def __floordiv__(self, other):
        other = Number(other)

        # no validation required.

        return Number(self.value // other.value)

    # %
    def __mod__(self, other):
        other = Number(other)

        # no validation required.

        return Number(self.value % other.value)

    # **
    def __pow__(self, other):
        other = Number(other)

        # no validation required.

        return Number(self.value ** other.value)
    #endregion
    #region reverse operators
    # +
    __radd__ = lambda self, other: self + other

    # -
    __rsub__ = lambda self, other: self - other

    # *
    __rmul__ = lambda self, other: self * other

    # /
    __rtruediv__ = lambda self, other: self / other

    # //
    __rfloordiv__ = lambda self, other: self // other

    # %
    __rmod__ = lambda self, other: self % other

    # **
    __rpow__ = lambda self, other: self ** other
    #endregion
    #region in-place operators
    # +=
    def __iadd__(self, other):
        self = self + other
        return self

    # -=
    def __isub__(self, other):
        self = self - other
        return self

    # *=
    def __imul__(self, other):
        self = self * other
        return self

    # /=
    def __itruediv__(self, other):
        self = self / other
        return self

    # //=
    def __ifloordiv__(self, other):
        self = self // other
        return self

    # %=
    def __imod__(self, other):
        self = self % other
        return self

    # **=
    def __ipow__(self, other):
        self = self ** other
        return self
    #endregion
    #region bitwise operators
    # &
    def __and__(self, other):
        other = Number(other)

        return Number(self.value & other.value)

    # |
    def __or__(self, other):
        other = Number(other)

        return Number(self.value | other.value)

    # ^
    def __xor__(self, other):
        other = Number(other)

        return Number(self.value ^ other.value)

    # <<
    def __lshift__(self, other):
        other = Number(other)

        return Number(self.value << other.value)

    # >>
    def __rshift__(self, other):
        other = Number(other)

        return Number(self.value >> other.value)
    #endregion
    #region reverse bitwise operators
    # &
    __rand__ = lambda self, other: self & other

    # |
    __ror__ = lambda self, other: self | other

    # ^
    __rxor__ = lambda self, other: self ^ other

    # <<
    __rlshift__ = lambda self, other: self << other

    # >>
    __rrshift__ = lambda self, other: self >> other
    #endregion
    #region in-place bitwise operators
    # &=
    def __iand__(self, other):
        self = self & other
        return self

    # |=
    def __ior__(self, other):
        self = self | other
        return self

    # ^=
    def __ixor__(self, other):
        self = self ^ other
        return self

    # <<=
    def __ilshift__(self, other):
        self = self << other
        return self

    # >>=
    def __irshift__(self, other):
        self = self >> other
        return self
    #endregion
    #region unary operators
    # +
    def __pos__(self):
        return self

    # -
    def __neg__(self):
        raise ValueError('Type Number does not support negative values.')

    # ~
    def __invert__(self):
        raise ValueError('Type Number does not support negative values. The ~ operator is therfore not supported.')
    #endregion
    #region comparison operators
    # ==
    def __eq__(self, other):
        other = Number(other)

        return self.value == other.value

    # !=
    def __ne__(self, other):
        other = Number(other)

        return self.value != other.value

    # <
    def __lt__(self, other):
        other = Number(other)

        return self.value < other.value

    # <=
    def __le__(self, other):
        other = Number(other)

        return self.value <= other.value

    # >
    def __gt__(self, other):
        other = Number(other)

        return self.value > other.value

    # >=
    def __ge__(self, other):
        other = Number(other)

        return self.value >= other.value
    #endregion
    #region conversion operators
    # int
    def __int__(self):
        return self.value

    # float
    def __float__(self):
        return float(self.value)

    # complex
    def __complex__(self):
        return complex(self.value)

    # str
    def __str__(self):
        return str(self.value)

    # bytes
    def __bytes__(self):
        return bytes(self.value)

    # repr
    def __repr__(self):
        return f'Number({self.value})'

    # hash
    def __hash__(self):
        return hash(self.value)
    #endregion
    #region other operators
    # abs
    def __abs__(self):
        # Number objects are already positive.
        return Number(self.value)

    # round
    def __round__(self, n:int = 0):
        # Number objects are already integers.
        return Number(self.value)

    # floor
    def __floor__(self):
        # Number objects are already integers.
        return Number(self.value)

    # ceil
    def __ceil__(self):
        # Number objects are already integers.
        return Number(self.value)
    #endregion

    def is_even(self):
        """
        Returns True if the number is even, False otherwise.
        """
        return self % 2 == 0

    def is_odd(self):
        """
        Returns True if the number is odd, False otherwise.
        """
        return not self.is_even()

    def step(self, shortcut:bool = False):
        """
        Returns the next number in the Collatz sequence.
        if shortcut is True, the shortcut form of the conjecture is used.
        """
        if self.is_even():
            return self / 2
        else:
            if shortcut:
                return (3 * self + 1) / 2
            else:
                return 3 * self + 1

    def reverse_step(self, shortcut:bool = False):
        """
        Returns the one or two numbers from which this number can be reached in the Collatz sequence.
        if shortcut is True, the shortcut form of the conjecture is used.
        """
        numbers = [self * 2]

        if shortcut:
            # y = (3x + 1) / 2
            # x = (2y - 1) / 3
            if (self * 2 - 1) % 3 == 0:
                numbers.append((self * 2 - 1) / 3)
        else:
            # y = 3x + 1
            # x = (y - 1) / 3
            if (self - 1) % 3 == 0:
                numbers.append((self - 1) / 3)

        return numbers

    def series(self, shortcut:bool = False):
        """
        Returns a list of numbers in the Collatz sequence.
        if shortcut is True, the shortcut form of the conjecture is used.
        """
        sequence = [self]

        while sequence[-1] != 1:
            sequence.append(self.step(shortcut))

        return sequence

    def steps(self):
        """
        Returns the number of steps it takes to reach 1 in the Collatz sequence.
        """
        return len(self.series()) - 1

    def steps_to_fall(self):
        """
        Returns the number of steps it takes to reach a number less than the starting number in the Collatz sequence.
        """
        count = 0
        number = self

        while number >= self:
            number = number.step()
            count += 1

        return count

class Form():
    """
    Reperesents all numbers of the linear form an + b
    """
    def __init__(self, a:int|str|bytes|'Number', b:int|str|bytes|'Number'):
        """
        NOTE: a and b are stored as integers rather than Number objects because
        0 is a valid value for b and the Number class does not support 0.
        """
        try:
            a = int(a)
            assert a > 0
        except ValueError:
            raise ValueError(f'Failed to convert value: {a} of type: {type(a)} to type int.')
        except AssertionError:
            raise ValueError('Value a must be greater than 0.')

        try:
            b = int(b)
        except ValueError:
            raise ValueError(f'Failed to convert value: {b} of type: {type(b)} to type int.')

        self.a = int(a)
        self.b = int(b)


    #region operators
    # +
    def __add__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a, self.b + other)
        elif isinstance(other, Form):
            return Form(self.a + other.a, self.b + other.b)
        else:
            raise ValueError(f'Cannot add Form with type: {type(other)}.')

    # -
    def __sub__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a, self.b - other)
        elif isinstance(other, Form):
            return Form(self.a - other.a, self.b - other.b)
        else:
            raise ValueError(f'Cannot subtract Form with type: {type(other)}.')

    # *
    def __mul__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a * other, self.b * other)
        elif isinstance(other, Form):
            raise ValueError('Multiplying two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot multiply Form with type: {type(other)}.')

    # /
    def __truediv__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a / other, self.b / other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # //
    def __floordiv__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a // other, self.b // other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # %
    def __mod__(self, other:int|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a % other, self.b % other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')
    #endregion
    #region comparison operators
    # ==
    def __eq__(self, other:'Form'):
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        return self.a == other.a and self.b == other.b

    # !=
    def __ne__(self, other:'Form'):
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        return self.a != other.a or self.b != other.b

    # <
    def __lt__(self, other:'Form'):
        """
        Return True if self is smaller than other for all positive values of n, otherwise return False.
        """
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        if self.a == other.a:
            # if a is the same, then the form with the smaller b is smaller.
            return self.b < other.b
        else:
            # if a is different, then the forms (modeled as lines) will intersect at some point.
            # an + b = xn + y
            # an - xn = n(a - x) = y - b
            # n = (y - b) / (a - x)

            # This is the x value of the intersection point.
            point = (other.b - self.b) / (self.a - other.a)

            if point <= 0:
                # if the intersection point is negative then the bigger form can be established by testing n = 1.
                return self.a + self.b < other.a + other.b
            else:
                # if the intersection point is positive then all values of n smaller than that point will be smaller for either self or other
                # and all values of n greater than that point will be smaller for the other form.
                # Since there are values for which self is bigger and values for which it is smaller return False as this is a strict test.
                return False

    # <= # NOTE: This is a less strict version of the < operator and is not what you might expect from the <= operator.
    # use `self < other or self == other` for this behavior instead.
    def __le__(self, other:'Form'):
        """
        Return True if self is smaller than other for large enough positive values of n, otherwise return False.
        """
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        if self.a == other.a:
            # if a is the same, then the form with the smaller b is smaller.
            return self.b < other.b
        else:
            # if a is different, then the forms (modeled as lines) will intersect at some point.
            # an + b = xn + y
            # an - xn = n(a - x) = y - b
            # n = (y - b) / (a - x)

            # This is the x value of the intersection point.
            point = (other.b - self.b) / (self.a - other.a)

            if point <= 0:
                # if the intersection point is negative then the bigger form can be established by testing n = 1.
                return self.a + self.b < other.a + other.b
            else:
                # if the intersection point is positive then all values of n smaller than that point will be smaller for either self or other
                # and all values of n greater than that point will be smaller for the other form.
                # As this is the non-strict version of the < test we can test any point greater than the intersection point.
                new_point = point + 1
                return new_point * self.a + self.b < new_point * other.a + other.b

    # >
    def __gt__(self, other:'Form'):
        """
        Return True if self is greater than other for all positive values of n, otherwise return False.
        """
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        return not (self < other or self == other)

    # >= # NOTE: This is a less strict version of the > operator and is not what you might expect from the >= operator.
    # use `self > other or self == other` for this behavior instead.
    def __ge__(self, other:'Form'):
        """
        Return True if self is greater than other for large enough positive values of n, otherwise return False.
        """
        raise NotImplementedError('The >= operator is not yet implemented for Form objects.')

        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        return not (self < other)
    #endregion
    #region other operators
    # bool
    def __bool__(self):
        return True
    #endregion

    def is_even(self):
        """
        Returns True if the form is even, False otherwise.
        Returns None if the parity of the form cannot be determined.
        """
        if self.a % 2 == 0:
            return self.b % 2 == 0
        else:
            return None # if a is odd then the parity of the form cannot be determined.

    def is_odd(self):
        """
        Returns True if the form is odd, False otherwise.
        Return None if the parity of the form cannot be determined.
        """
        if self.a % 2 == 0:
            return self.b % 2 == 1
        else:
            return None # if a is odd then the parity of the form cannot be determined.

    def step(self):
        """
        Returns the next form in the Collatz sequence.
        Return None if the next form cannot be determined.
        """
        if self.is_even():
            return Form(self.a // 2, self.b // 2)
        elif self.is_odd():
            return Form(3*self.a, 3*self.b + 1)
        else:
            return None


