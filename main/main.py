from __future__ import annotations
import copy, math

class Number():
    def __init__(self, value:int|str|bytes|'Number'):
        try:
            value = int(value)
        except (ValueError, TypeError):
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
        self.value += Number(other).value
        return self

    # -=
    def __isub__(self, other):
        self.value -= Number(other).value
        return self

    # *=
    def __imul__(self, other):
        self.value *= Number(other).value
        return self

    # /=
    def __itruediv__(self, other):
        self.value /= Number(other).value
        return self

    # //=
    def __ifloordiv__(self, other):
        self.value //= Number(other).value
        return self

    # %=
    def __imod__(self, other):
        self.value %= Number(other).value
        return self

    # **=
    def __ipow__(self, other):
        self.value **= Number(other).value
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
        self.value &= Number(other).value
        return self

    # |=
    def __ior__(self, other):
        self.value |= Number(other).value
        return self

    # ^=
    def __ixor__(self, other):
        self.value ^= Number(other).value
        return self

    # <<=
    def __ilshift__(self, other):
        self.value <<= Number(other).value
        return self

    # >>=
    def __irshift__(self, other):
        self.value >>= Number(other).value
        return self
    #endregion
    #region unary operators
    # +
    def __pos__(self):
        return self

    # -
    def __neg__(self):
        raise ValueError('Type Number does not support negative values. Use `-int(num)` to get the negative value as an `int` type.')

    # ~
    def __invert__(self):
        raise ValueError('Type Number does not support negative values. The ~ operator is therefore not supported. Use `~int(num)` to get the bitwise inverse as an `int` type.')
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
        # use (bit_length + 7) // 8 to convert from bits to bytes and round up.
        return self.value.to_bytes((self.value.bit_length() + 7) // 8, byteorder='big')

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
        return self % 2 == 1

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
        # Start with twice our number. This value would havlve to
        # reach our number regardless of if the shortcut form is used or not.
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

class Transform():
    """
    Reperesents a transformation from one `Form` to another.
    NOTE: This class serves to store transformation information but
    does not validate the data it holds. The is_valid method can be used
    to check if the data is valid.
    """
    def __init__(self, start:Form, end:Form, transform:Form = None, steps:int = None, has_fallen:bool = None, min_value:int = None):
        """
        start: The starting form.
        end: The ending form.
        steps: The number of steps it took to reach the ending form.
        has_fallen: True if the form has fallen below the starting form, False if it has not, None if it is unknown.
        min_value: The minimum value at which the form has fallen below the starting form.
        """
        assert isinstance(start, Form), "start must be of type Form."
        assert isinstance(end, Form), "end must be of type Form."
        assert transform is None or isinstance(transform, Form), "transform must be of type Form."
        assert steps is None or isinstance(steps, int), "steps must be of type int."
        assert has_fallen is None or isinstance(has_fallen, bool), "has_fallen must be of type bool."
        assert min_value  is None or isinstance(min_value, int), "min_value must be of type int."

        self.start = start
        self.end = end
        self.transform = transform
        self.steps = steps
        self.has_fallen = has_fallen
        self.min_value = min_value

    def __repr__(self):
        # TODO: The condition means it returns an empty string.
        return f'Transform({self.start}, {self.end}, transform={self.transform}, steps={self.steps}' + \
                (f', has_fallen={self.has_fallen}' if self.has_fallen is not None else '') + \
                (f', min_value={self.min_value})' if (self.min_value is not None) and (self.has_fallen is not None) else ')')

    __str__ = __repr__

    def is_valid(self):
        """
        Returns True if the data stored in the Transform object is valid, False otherwise.
        This checks:
        a) does applying the given transformation to the start form result in the end form.
        b) does the number of steps match the number of steps it takes to reach the end form.
        c) does the form fall below the starting form if it is supposed to.
        """
        if self.transform:
            if self.transform(self.start) != self.end:
                return False
        if self.steps:
            if self.steps != self.start.compute_fall().steps:
                return False
        if self.has_fallen:
            if self.has_fallen != self.start.compute_fall().has_fallen:
                return False
        if self.min_value:
            if self.min_value != self.start.compute_fall().min_value:
                return False

class Form():
    """
    Reperesents all numbers of the linear form an + b
    """
    # We can't deffine it yet but we can type it.
    # BASIS = Form(1, 0)
    BASIS: 'Form'
    # ODD = Form(2, 1)
    ODD: 'Form'
    # EVEN = Form(2, 0)
    EVEN: 'Form'

    def __init__(self, a:int|float|str|bytes|'Number', b:int|float|str|bytes|'Number'):
        """
        NOTE: a and b are stored as integers rather than Number objects because
        0 is a valid value for b and the Number class does not support 0.
        """
        try:
            a = float(a)
            assert a > 0
        except ValueError:
            raise ValueError(f'Failed to convert value: {a} of type: {type(a)} to type float.')
        except AssertionError:
            raise ValueError('Value a must be greater than 0.')

        if not math.isfinite(a):
            raise ValueError('Value a must be finite.')

        try:
            b = float(b)
            assert not b < 0 # b can be 0 but no smaller.
        except ValueError:
            raise ValueError(f'Failed to convert value: {b} of type: {type(b)} to type float.')

        if not math.isfinite(b):
            raise ValueError('Value b must be finite.')

        self.a = float(a)
        self.b = float(b)

    #region operators
    # +
    def __add__(self, other:int|float|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a, self.b + other)
        elif isinstance(other, Form):
            return Form(self.a + other.a, self.b + other.b)
        else:
            raise ValueError(f'Cannot add Form with type: {type(other)}.')

    # -
    def __sub__(self, other:int|float|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a, self.b - other)
        elif isinstance(other, Form):
            return Form(self.a - other.a, self.b - other.b)
        else:
            raise ValueError(f'Cannot subtract Form with type: {type(other)}.')

    # *
    def __mul__(self, other:int|float|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a * other, self.b * other)
        elif isinstance(other, Form):
            raise ValueError('Multiplying two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot multiply Form with type: {type(other)}.')

    # /
    def __truediv__(self, other:int|float|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a / other, self.b / other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # //
    def __floordiv__(self, other:int|float|Number|'Form'):
        if isinstance(other, (int, Number)):
            return Form(self.a // other, self.b // other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # %
    def __mod__(self, other:int|float|Number|'Form'):
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
        Return True if self is smaller than other for large enough values of n, otherwise return False.
        Also returns the point at which the forms intersect.
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
            # n = (y - b) / (a - x) = (b - y) / (x - a)

            # This is the x value of the intersection point.
            point = (other.b - self.b) / (self.a - other.a)

            # check a point beyond the intersection point.
            check = (point + 1)*self.a + self.b < (point + 1)*other.a + other.b

            return check, point

    # <=
    __le__ = lambda self, other: self < other or self == other

    # >
    def __gt__(self, other:'Form'):
        """
        Return True if self is bigger than other for large enough values of n, otherwise return False.
        Also returns the point at which the forms intersect.
        """
        if not isinstance(other, Form):
            raise ValueError(f'Cannot compare Form with type: {type(other)}.')

        if self.a == other.a:
            # if a is the same, then the form with the smaller b is smaller.
            return self.b > other.b
        else:
            # if a is different, then the forms (modeled as lines) will intersect at some point.
            # an + b = xn + y
            # an - xn = n(a - x) = y - b
            # n = (y - b) / (a - x) = (b - y) / (x - a)

            # This is the x value of the intersection point.
            point = (other.b - self.b) / (self.a - other.a)

            # check a point beyond the intersection point.
            check = (point + 1)*self.a + self.b > (point + 1)*other.a + other.b

            return check, point

    # >=
    __ge__ = lambda self, other: self > other or self == other

    #endregion
    #region misc
    # bool
    def __bool__(self):
        return True

    # repr
    def __repr__(self):
        a = int(self.a) if self.a.is_integer() else self.a
        b = int(self.b) if self.b.is_integer() else self.b

        # Form(an + b) or Form(an)
        return f'Form({a}n{" + "+str(b) if b > 0 else ""})'

        # Form(a, b) as an alternative format
        # return f'Form({a}, {b})'

    # hash
    def __hash__(self):
        return hash((self.a, self.b))

    # call
    def __call__(self, n:int|float|Number|'Form'):
        """
        Returns the value of the form at n.
        """
        if type(n) in (int, float, Number):
            n = float(n)
            return self.a * n + self.b
        elif isinstance(n, Form):
            return Form(self.a * n.a, self.a * n.b + self.b)
        else:
            raise ValueError(f'Cannot call Form with type: {type(n)}.')
    #endregion

    def parity(self):
        """
        Returns the parity of the form.
        -1 = odd
        0 = unknown
        1 = even
        This can be used in boolean expressions to check if the parity is known as
        bool(1) == bool(-1) == True and bool(0) == False. bool(self.parity()) will
        return True if the parity is known and False otherwise.
        """
        if self.a % 2 == 0:
            return 1 if (self.b % 2 == 0) else -1
        else:
            return 0

        # NOTE: self.parity() is True if the parity is known because bool(1) == bool(-1) == True

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

    def step(self, shortcut = False): # TODO: add shortcut form
        """
        Returns the next form in the Collatz sequence and the transform required to get there.
        Return None if the next form cannot be determined.
        """
        if self.is_even():
            return Form(self.a // 2, self.b // 2), Form(0.5, 0.5)
        elif self.is_odd():
            return Form(3*self.a, 3*self.b + 1), Form(3, 1)
        else:
            return None

    def compute_fall(self):
        """
        Computes the form until it falls below the starting form or its parity cannot be determined.
        Returns True if it falls below it's starting value or False otherwise and
        the form at which it is below it's starting value or the form at which it's parity became unknown.
        If the fall is conditional then the minimum value for the fall is returned along with the form.
        returns `False, form, steps` or `True, form, steps` or `True, form, steps, min_value`
        """
        form = copy.copy(self)
        steps = 0
        transform = Form.BASIS

        while True:
            # compute the next step
            step = form.step()

            if step is None:
                return Transform(self, form, transform, steps, False)

            form = step[0]
            transform = step[1](transform)

            steps += 1
            comp = form < self
            if comp[0]:
                # the intersect must be strictly smaller than 1 for self to be bigger for every valid case (n > 0, n ∈ Z)
                if comp[1] < 1:
                    return Transform(self, form, transform, steps, True)
                else:
                    return Transform(self, form, transform, steps, True, comp[1])

    def compute_full(self):
        """
        Computes the form until it's parity becomes unknown and returns the form at which it's parity became unknown.
        If the parity is unknown from the start then a copy of the original form is returned.
        Also returns the number of steps it took to reach the unknown parity.
        """
        form = copy.copy(self)
        steps = 0
        transform = Form.BASIS

        while form.parity(): # True for known parity (-1 or 1), False for unknown parity (0).
            # will never be None due to the parity check.
            step = form.step()
            transform = step[1](transform)
            form = step[0]
            steps += 1

        return Transform(self, form, transform, steps)

    def split_form(self, parts:int):
        """
        Splits self into `parts` parts and returns them in a tuple.
        """
        # an + b
        # for parts = 2: (2a)n + b, (2a)n + (b + 1)
        # for parts = 3: (3a)n + b, (3a)n + (b + 1), (3a)n + (b + 2)
        # for parts = p: (pa)n + b, (pa)n + (b + 1), (pa)n + (b + 2), ..., (pa)n + (b + p - 1)
        parts_list = []
        for i in range(parts):
            parts_list.append(Form(parts*self.a, self.b + i*self.a))

        return tuple(parts_list)

    @classmethod
    def compute_set(cls, a:int, full:bool = False, filter_fallen:bool = False):
        """
        Computes all forms: `a`n + b where b ranges from 0 to `a` - 1.
        This runs compute_fall or compute_full on each and returns a list of the results.
        if filter_fallen is True remove results that fall below their starting form.
        """
        results = []
        for b in range(a):
            if full:
                new = Form(a, b).compute_full()
            else:
                new = Form(a, b).compute_fall()

            if not (filter_fallen and new.has_fallen):
                results.append(new)

        return results

    def tree(self, split:int, depth:int):
        """
        Recursivly calls compute_fall on the form splitting it by `split` whenever it's parity becomes unknown.
        Stop after `depth` levels of recursion.
        """
        if depth == 0:
            return self

        result = self.compute_fall()
        if result.has_fallen:
            return result
        else:
            # TODO: Consider splitting the form after the precomputation. i.e. replacing `self.split_form(split)` with `result.end.split_form(split)`
            # this would still cover all cases and would be more efficient but is also a little less intuitive.
            return tuple([form.tree(split, depth - 1) for form in self.split_form(split)])

    def inverse(self):
        """
        Return the inverse form. This models the form as a linear equation
        in terms of y then solves for x and returns the resulting form
        y = ax + b  =>  x = (y - b) / a = (1/a)y - b/a
        """
        return Form(1/self.a, -self.b/self.a)

# Now that the Form class is defined we can define the BASIS attribute.
Form.BASIS = Form(1, 0)
Form.ODD = Form(2, 1)
Form.EVEN = Form(2, 0)



if __name__ == "__main__":

    ##NOTE: Interesting pattern #1
    # this shows that for every chunk of numbers of the form 256n + k where k ranges from 0 to 255
    # there are only 19 values that don't fall below their starting value and, when these values are
    # precomputed the a values of the resulting forms an + b are all powers of 3 (3^6, 3^7, and in just the last case 3^8)
    for i, result in enumerate(Form.compute_set(256, filter_fallen=True), 1):
        print(f"{math.log(result.end.a, 3)}")




    # print(Form(1, 0).tree(2, 5))

    # # The below code demonstrates that every number of the form 4n + 1 will fall to 3n + 1 in 3 steps.
    # test = Form(4, 1)
    # print(test.compute_fall()) # Transform(Form(4.0, 1.0), Form(3.0, 1.0), transform=Form(0.75, 1.0), steps=3, has_fallen=True)

    # # The below code demonstrates that every number of the form 4n + 3 will go to to 9n + 8 in 4 steps at which point it's parity becomes unknown.
    # test = Form(4, 3)
    # print(test.compute_fall()) # Transform(Form(4.0, 3.0), Form(9.0, 8.0), transform=Form(2.25, 2.5), steps=4, has_fallen=False)

    # # The below code shows the form 1n + 0 being split into two parts (even and odd numbers), 2n + 0 and 2n + 1.
    # test = Form(1, 0)
    # print(test.split_form(2)) # (Form(2, 0), Form(2, 1))
    # print(test.split_form(3)) # (Form(3, 0), Form(3, 1), Form(3, 2))

    # test = Form(4, 3)
    # print(test.split_form(2)) # (Form(8, 3), Form(8, 7))
    # print(test.split_form(3)) # (Form(12, 3), Form(12, 7), Form(12, 11))

    # for i in range(1, 30):
    #     print(f"{2**i}\t\t{len(Form.compute_set(2**i, filter_fallen=True))}\t\t{len(Form.compute_set(2**i, filter_fallen=True))/2**i}")
    # # 2               1               0.5
    # # 4               1               0.25 # pair
    # # 8               2               0.25
    # # 16              3               0.1875
    # # 32              4               0.125 # pair
    # # 64              8               0.125
    # # 128             13              0.1015625
    # # 256             19              0.07421875 # pair
    # # 512             38              0.07421875
    # # 1024            64              0.0625 # pair
    # # 2048            128             0.0625
    # # 4096            226             0.05517578125
    # # 8192            367             0.0447998046875 # pair
    # # 16384           734             0.0447998046875
    # # 32768           1295            0.039520263671875
    # # 65536           2114            0.032257080078125 # pair
    # # 131072          4228            0.032257080078125
    # # 262144          7495            0.028591156005859375 # pair
    # # 524288          14990           0.028591156005859375
    # # 1048576         27328           0.02606201171875

    # for i in range(1, 300):
    #     print(f"{i}\t\t{len(Form.compute_set(i, filter_fallen=True))}\t\t{len(Form.compute_set(i, filter_fallen=True))/i}")
    # compute_set for odd coefficients always yields a ratio of 1. This means that every form with an odd coefficient will have no eliminations.
    # This is PROBABLY because the parity of the form is always unknown and so the process stops straight away.