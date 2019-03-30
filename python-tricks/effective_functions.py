# -*- coding: utf-8 -*-

# ----------------------------------------
# Python's Functions are First-Class objects

def yell(text):
    return text.upper() + "!"

yell("hello")

bark = yell

bark("hello")

del yell

# yell("hello?") -> undefined yell
bark("hello?")
print(bark.__name__) # yell

# yell, bark: variable pointing to the function
# def yell: the function itself

funcs = [bark, str.lower, str.capitalize]

print(funcs)

funcs[0]("Heyho")

# Pass function to other functions
def greet(func):
    greeting = func("hello")
    print(greeting)

greet(bark)

list(map(bark, ["hello", "hey", "hi"]))

# ----------------------------------------
# Lambdas are single-expression functions

add = lambda x, y: x + y
add(5, 3)

(lambda x, y: x + y)(5, 3)

# Supply a function object

tuples = [(1, 'd'), (2, 'b'), (4, 'a'), (3, 'c')]

sorted(tuples, key=lambda x: x[1])

sorted(range(-5, 6), key=lambda x: x * x)

# Harmful
list(filter(lambda x: x % 2 == 0, range(16)))

# Better
[x for x in range(16) if x % 2 == 0]


# ----------------------------------------
# Power of Decorators

# Basics

# A decorator is a callable that takes a callable as input and returns 
# another callable

def null_decorator(func):
    return func

def greet():
    return "Hello!"

greet = null_decorator(greet)

greet()

@null_decorator
def greet():
    return "Hello!"

greet()

def uppercase(func):
    def wrapper():
        ori_result = func()
        result = ori_result.upper()
        return result
    return wrapper

@uppercase
def greet():
    return "Hello!"

greet()

# Decorating functions that accept arguments
def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def trace(func):
    def wrapper(*args, **kwargs):
        print(f"TRACE: calling {func.__name__}() with {args}, {kwargs}.")
        
        ori_result = func(*args, **kwargs)
        
        print(f"TRACE: {func.__name__}() returned {ori_result!r}")
        
        return ori_result
    return wrapper

@trace
def say(name, line):
    return f'{name}: {line}'

say("Jane", "Hello world")
        

# Write "debuggable" decorators

@uppercase
def greet():
    """Return a friendly greeting..."""
    return "Hello!"

print(greet.__name__, greet.__doc__) # wrapper None

import functools

def uppercase(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper

@uppercase
def greet():
    """Return a friendly greeting..."""
    return "Hello!"

print(greet.__name__, greet.__doc__) # greet Return a friendly greeting...

# ----------------------------------------
# Func with *args and **kwargs

def foo(required, *args, **kwargs):
    print(required)
    if args:
        print(args)
    if kwargs:
        print(kwargs)

foo() # TypeError: foo() missing 1 required positional argument: 'required'

foo("Hello") # Hello

foo("Hello", 1, 2 ,3) 
# Hello
# (1, 2, 3)

foo("Hello", 1, 2 ,3, key1="value", key2=999) 
# Hello
# (1, 2, 3)
# {'key1': 'value', 'key2': 999}

# forward optional or keyword arguments

def bar(*args, **kwargs):
    if args:
        print(args)
    if kwargs:
        print(kwargs)

def foo(x, *args, **kwargs):
    kwargs["name"] = "Alice"
    new_args = args + ('extra', )
    bar(x, *new_args, **kwargs)
    

foo("hello", 1, 2, 3) # ('hello', 1, 2, 3, 'extra') {'name': 'Alice'}

# ----------------------------------------
# Function Argument Unpacking

def print_vector(x, y, z):
    print("<{}, {}, {}>".format(x, y, z))
    
print_vector(0, 1, 0)

tuple_vec = (1, 0, 1)
list_vec = [1, 0, 1]

genexpr = (x * x for x in range(3))

# Function Argument Unpacking using the * operator
print_vector(*tuple_vec)
print_vector(*list_vec)
print_vector(*genexpr)

dict_vec = {"z": 0, "y" : 1, "x": 2}
print_vector(*dict_vec)
print_vector(**dict_vec)










