# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 00:27:37 2019

@author: Quan Hua
"""

# ----------------------------------------
# Assertions

def apply_discount(product, discount):
    price = int(product['price']) * (1.0 - discount)
    assert 0 <= price <= product['price']
    return price

shoes = {'name': 'Fancy Shoes', 'price': 14900}

print("01: ", apply_discount(shoes, 0.25)) # 11175

try:
    apply_discount(shoes, 2.0) # throws error
except AssertionError:
    print("01: assertion error")
    
## Caveat #1: Don't use asserts for data validation
## Caveat #2: Asserts that never fail. Always do a quick smoke test to make
## sure they can actually fail.

# ----------------------------------------    
# Comma Placement

names = [
        'Alice',
        'Bob',
        'Dilbert' # <- Missing comma!
        'Jane'
        ]

print("02: ", names) # ['Alice', 'Bob', 'DilbertJane']
    
names = [
        'Alice',
        'Bob',
        'Dilbert',
        'Jane',
        ]

print("02: ", names) # ['Alice', 'Bob', 'Dilbert', 'Jane']

# ----------------------------------------
# Context Managers and the with Statement

import os
from tempfile import gettempdir

## Example 1:
temp_path = os.path.join(gettempdir(), "hello.txt")
print("03: temp_path = ", temp_path)

with open(temp_path, "w") as f:
    f.write("hello world!")

## same as
f = open(temp_path, "w")
try:
    f.write("hello world!")
finally:
    f.close()

## Example 2:
import threading

some_lock = threading.Lock()

# Harmful!:
some_lock.acquire()
try:
    # Do something
    pass
finally:
    some_lock.release()

# Better
with some_lock:
    # Do something
    pass

## Example 3: Support our own objects

class ManagedFile:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print("__enter__")
        self.file = open(self.name, "w")
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        if self.file:
            self.file.close()
            print("self.file.close()")

with ManagedFile(temp_path) as f:
    f.write("hello world!")
            
## Example 4: Use contextlib
from contextlib import contextmanager

@contextmanager
def managed_file(name):
    try:
        f = open(name, "w")
        yield f
    finally:
        f.close()
        
with managed_file(temp_path) as f:
    f.write("hello")
    
# ----------------------------------------
# Underscores, Dunders ...

# 1. Single Leading Underscore: _var : hint for internal use
    
class Test_var:
    def __init__(self):
        self.foo = 11
        self._bar = 23

# 2. Single Trailing Underscore: var_ : use for breaking the naming conflict
    
def make_object(name, class_): # class is a keyword in Python
    pass
        
# 3. Double Leading Underscore: __var: name mangling - the interpreter changes
# the name of variable to make it harder to create collisions when the class
# is extended later

class Test__var:
    def __init__(self):
        self.foo = 11
        self._bar = 23
        self.__baz = 42

t = Test__var()
print(dir(t)) # __baz becomes _Test__var__baz

class ExtendedTest__var(Test__var):
    def __init__(self):
        super().__init__()
        self.__baz = "overridden"
        
t2 = ExtendedTest__var()
print(dir(t2)) # '_ExtendedTest__var__baz', '_Test__var__baz',

print('_ExtendedTest__var__baz ', t2._ExtendedTest__var__baz) # overriden
print('_Test__var__baz ', t2._Test__var__baz) # 42
        
# 4. Double Leading and Trailing Underscore: __var__ - reserved for special
# use in the language - it's best to stay away from this

        
# ----------------------------------------
# String formatting

# 1. Old style
errno = 50159747054
name = "Bob"

print("Hello, %s" % name) # Hello, Bob
print("%x" % errno) # badc0ffee

print("Hey %(name)s, there is 0x%(errno)x error!" % {
        "name": name,
        "errno" : errno
        })
    
# 2. New style

print("Hello, {}".format(name)) # Hello, Bob

print("Hey {name}, there is a 0x{errno:x} error!".format(
        name=name, errno=errno))

# 3. Literal String Interpolation (Python 3.6)
print(f"Hello, {name}!")
print(f"Five plus ten is {5 + 10} and not {2 * (5 + 10)}")

# ----------------------------------------
# "The Zen of Python"
import this
