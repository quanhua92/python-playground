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
    
        
        
        
        



