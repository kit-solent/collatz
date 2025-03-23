from __future__ import annotations
import copy, math, pathlib

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
        min_value: The minimum value at which the form has fallen below the starting form. If None then the fall is unconditional
        and occurs for all values of n > 0.
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

    def __init__(self, a:int|float|str|bytes, b:int|float|str|bytes):
        """
        doc string 123
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
    def __add__(self, other:int|float|'Form'):
        if isinstance(other, int):
            return Form(self.a, self.b + other)
        elif isinstance(other, Form):
            return Form(self.a + other.a, self.b + other.b)
        else:
            raise ValueError(f'Cannot add Form with type: {type(other)}.')

    # -
    def __sub__(self, other:int|float|'Form'):
        if isinstance(other, int):
            return Form(self.a, self.b - other)
        elif isinstance(other, Form):
            return Form(self.a - other.a, self.b - other.b)
        else:
            raise ValueError(f'Cannot subtract Form with type: {type(other)}.')

    # *
    def __mul__(self, other:int|float|'Form'):
        if isinstance(other, int):
            return Form(self.a * other, self.b * other)
        elif isinstance(other, Form):
            raise ValueError('Multiplying two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot multiply Form with type: {type(other)}.')

    # /
    def __truediv__(self, other:int|float|'Form'):
        if isinstance(other, int):
            return Form(self.a / other, self.b / other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # //
    def __floordiv__(self, other:int|float|'Form'):
        if isinstance(other, int):
            return Form(self.a // other, self.b // other)
        elif isinstance(other, Form):
            raise ValueError('Dividing two forms gives a non linear result.')
        else:
            raise ValueError(f'Cannot divide Form with type: {type(other)}.')

    # %
    def __mod__(self, other:int|float|'Form'):
        if isinstance(other, int):
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
    def __call__(self, n:int|float|'Form'):
        """
        Returns the value of the form at n.
        """
        if type(n) in (int, float):
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
    def compute_set(cls, a:int, full:bool = False, filter_fallen:bool = False) -> list[Transform]:
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


template_path = pathlib.Path(__file__).parent / "template.c"
def generate_program(start:int, stop:int, template:pathlib.Path = template_path, start_marker:str = "START", end_marker:str = "END"):
    """
    Generates a program using the provided template C code
    """
    with open(template, 'r') as file:
        template = file.read()

    program = template.replace(start_marker, str(start)).replace(end_marker, str(stop))

    # TODO: compile it.

    return program

# Now that the Form class is defined we can define the BASIS attribute.
Form.BASIS = Form(1, 0)
Form.ODD = Form(2, 1)
Form.EVEN = Form(2, 0)

# some usefull links:
# https://sweet.ua.pt/tos/3x+1.html