# -*- coding: utf-8 -*-

# ----------------------------------------
# Object Comparisons: "is" vs "=="

# ==: equality
# is: identities

a = [1, 2, 3]
b = a

print(a)
print(b)

print(a == b) # True
print(a is b) # True

c = list(a)
print(c)

print(a == c) # True
print(a is c) # False

# ----------------------------------------
# String Conversion (Every class needs a __repr__)

class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage
        
my_car = Car("red", 37281)
print(my_car) #<__main__.Car object at 0x0000025A186F1B00>
my_car

class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage
    
    def __str__(self):
        return f"a {self.color} car"
    
    def __repr__(self):
        return f"{self.__class__.__name__}( {self.color!r}, {self.mileage} )"
    
my_car = Car("red", 37281)
print(my_car) # a red car
my_car # Car( 'red', 37281 )

import datetime
today = datetime.date.today()

str(today) # '2019-03-30'
repr(today) # datetime.date(2019, 3, 30)

# ----------------------------------------
# Define Your Own Exception Classes
class BaseValidationError(ValueError):
    pass

class NameTooLongError(BaseValidationError):
    pass

class NameTooCuteError(BaseValidationError):
    pass

class NameTooShortError(BaseValidationError):
    pass

def validate(name):
    if len(name) < 10:
        raise NameTooShortError(name)

def handle_validation_error(err):
    pass

try:
    validate("jane")
except BaseValidationError as err:
    handle_validation_error(err)

# ----------------------------------------
# Clone Objects for Fun and Profit

# Make Shallow Copies
xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
ys = list(xs) # Make a shallow copy

xs
ys

xs.append(["new sublist"])
xs #[[1, 2, 3], [4, 5, 6], [7, 8, 9], ['new sublist']]
ys #[[1, 2, 3], [4, 5, 6], [7, 8, 9]]

xs[1][0] = "X"
xs #[[1, 2, 3], ['X', 5, 6], [7, 8, 9], ['new sublist']]
ys #[[1, 2, 3], ['X', 5, 6], [7, 8, 9]]

# Make Deep Copiies
import copy
xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
zs = copy.deepcopy(xs)

xs
zs

xs[1][0] = "X"
xs # [[1, 2, 3], ['X', 5, 6], [7, 8, 9]]
zs # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Copy Arbitrary Objects

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point( {self.x!r}, {self.y!r} )"

a = Point(23, 42)
b = copy.copy(a) # shallow copy

a
b
a is b

class Rectangle:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br
    
    def __repr__(self):
        return f"Rectangle( {self.tl!r} , {self.br!r} )"

rect = Rectangle(Point(0, 1), Point(5, 6))
srect = copy.copy(rect)

rect #Rectangle( Point( 0, 1 ) , Point( 5, 6 ) )
srect #Rectangle( Point( 0, 1 ) , Point( 5, 6 ) )
rect is srect #False

rect.tl.x = 999
rect #Rectangle( Point( 999, 1 ) , Point( 5, 6 ) )
srect #Rectangle( Point( 999, 1 ) , Point( 5, 6 ) )

drect = copy.deepcopy(srect)
drect.tl.x = 222

drect #Rectangle( Point( 222, 1 ) , Point( 5, 6 ) )
rect #Rectangle( Point( 999, 1 ) , Point( 5, 6 ) )
srect #Rectangle( Point( 999, 1 ) , Point( 5, 6 ) )






