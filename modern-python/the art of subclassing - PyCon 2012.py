# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.1.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Simple example of subclassing

# +
class Animal:
    
    def __init__(self, name):
        self.name = name
        
    def walk(self):
        print(f'{self.name} is walking')
        
class Dog(Animal):
    
    def bark(self):
        print('Woof')


# -

# Adding:
# - Dog add the bark() method to Animal. This is a new capability
#
# Override:
# - Snake replaces the walk() method of animation with a walk() method that knows how to slither
#
# Extending:
# - Cat modifies the walk() method to add tail swishing behavior while delegating the work of actual walking to its parent.

# # Pattern of Subclassing: Frameworks
# - The parent class supplies all the "controller" functionality and makes calls to pre-named stub methods
# - The subclass overrides stub methods of interest
#
# # Pattern of Subclassing: Dynamic dispatch to subclass methods
# - The parent class uses getatter() to dispatch to new functionality
# - The child class implements appropriately named methods
#
# ```python
# # parent class
# def onecmd(self, cmd, arg):
#     try:
#         func = getattr(self, 'do_' + cmd)
#     except AttributeError:
#         return self.default(cmd)
#     return func(arg)
# # child class:
# def do_pendown(self):
#     pass
# ```
#
# # Pattern of Subclassing: Call Patterns

# +
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return self.radius ** 2 * math.pi
    
    def __repr__(self):
        return f'{self.__class__.__name__} has area {self.area()}'
    
class Donut(Circle):
    
    def __init__(self, outer, inner):
        super().__init__(outer)
        self.inner = inner
    
    def area(self):
        outer, inner = self.radius, self.inner
        return Circle(outer).area() - Circle(inner).area()


# -

d = Donut(5, 3)
print(d)


# # What does it mean to be an object or class?
#
# - Definition of object: An entity that encapsulates data together with functions for manipulating that data
#
# - We implement with dictionaries:
#     - Instance dictionaries hold state and point to their class
#     - Class dictionaries hold the functions (methods)
#     
# # So what is a subclass?
# - A subclass is just a class that delegates work to another class
# - A subclass and its parent are just two different dictionaries that contain functions
# - A subclass points to its parent
# - The pointer means: "I delegate work to this class"
#
# - **In other works, subclassing can be viewed as a technique for code re-use**
# - It is the subclass that is in charge
# - The subclass decides what work gets delegated
#
# # Contrast the operational view versus the conceptual view
#
# Operational view of subclassing:
# - Classes are dictionaries of functions
# - Subclasses point to other dictionaries to reuse their code
# - Subclasses are in complete control of what happens
#
# Conceptual view of subclass:
# - Parent classes define an interface
# - Subclasses can extend that interface
# - Parents are in charge
# - Subclasses are just sepcializations of the parent
#     - Dog is an instance of Animal that knows how to bark
#     - Counter is an instance of dict that has a default of zero
#     
# # Liskov Substitution Principle
#
# If S is a subtype of T, then objects of type T may be replaced with objects of the S
#
# # Why do we are about Liskov?
#
# It is all about polymorphism and substitutability so that our subclases can be used in client code without chaning the client code
#
# # Substitutability is a big win
# - Lots of code in python works with dictionaries
# - An OrderedDict is a dict subclass that keeps most of the API intact (fully substituable)
#
# # Liskov Violations
# - Any part of the API that isn't fully substituable
# - This is common and normal
# - In particular, useful subclasses commonly have different constructor signatures
# - For example, the array API is very similar to the list API but the constructor is different
#
# ```python
# s = list(someiterable)
# s = array('c', someiterable)
# ```
#
# # Goal is to isolate or minimize the impact
#
# MutableSet instances support union(), intersection() and difference()
#
# So they need to be able to create new instances of MutableSet
#
# But, the signature of the constructor is unknown
#
# So, we factor our calls to the constructor in ```_from_iterable()```

# # The Circle/Ellipse Problem
#
# - In mathematics, the circle is just a special case of an ellipse where the major and minor axes happen to be of equal length
# - So, is the Circle an appropriate subclass of Ellipse?
# - If one Ellipse method stretches an axis, what does that mean for Circle instances?
# - The problem is that circles have less information than an ellipse and have constraints that don't apply to general ellipses
# - The reverse wouldn't work either because circles have capabilities that don't apply to ellipses (i.e that bounding box is a square)
#
# # Lessons of the Circle / Ellipse Problem
# - Taxonomy hierarchies do not neatly transform into useful class hierarchies
# - Substituability can be a **hard problem**
# - More importantly, it challenges our conceptual view of a subclass as simply a form of  specialization
# - **Clarity comes from thinking about the design in terms of code reuse (the class that has the most reusable code should be the parent)**
#
# ==> **Maximizing code use**

# # The Open-Closed Principle
# "software entities should be open for extension, but closed for modification"
#
# Sometimes it refers to use of abstract base classes to create fixed inferfaces with multiple implementations.
#
# **The view we take is that objects have internal invariants and that subclasses shouldn't be able to break those invariants.**
#
# **In other words, the classes capabilities can be extended but the underlying class shouldn't get broken**
#
# # OCP in Python witn name mangling
#
# A method named `__update` in a class called MyDict transforms the name into `_MyDict__update`. This makes the method invisible to subclasses. 
#
# **Use this to create protected internal calls in addition to overriable public methods**

# +
class MyDict:
    def __init__(self, iterable):
        self.items_list = []
        self.__update(iterable) # This works break if subclass override update
        
    def update(self, iterable):
        for item in iterable:
            self.items_list.append(item)
    __update = update
    
class MySubClassDict(MyDict):
    def update(self, iterable):
        print("Override update")


# -

d = MySubClassDict(list(range(0, 10)))

d.items_list

d.update(list(range(0, 5)))

d.items_list


