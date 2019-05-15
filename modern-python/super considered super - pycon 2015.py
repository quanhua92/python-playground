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

# # Method Resolution Order

# Inheritance is a tool for code reuse.
#
# Python super() is different than other languages. Python's super() doesn't just call the parent of the class. Python MRO **linearize** the ancestors.

class Adam(object): pass
class Eve(object): pass
class Ramon(Adam, Eve): pass
class Gayle(Adam, Eve): pass
class Raymond(Ramon, Gayle): pass
class Dennis(Adam, Eve): pass
class Sharon(Adam, Eve): pass
class Rachel(Dennis, Sharon): pass
class Matthew(Raymond, Rachel): pass


# Show MRO (Method resolution order) for a multi-level diamond diagram

help(Matthew)


# # Example 1

# +
class DoughFactory(object):
    
    def get_dough(self):
        return 'insecticide treated wheat dough'
    
class Pizza(DoughFactory):
    
    def order_pizza(self, *toppings):
        print('Getting dough')
        dough = super().get_dough()
        print('Making pie with %s' % dough)
        for topping in toppings:
            print('Adding: %s' % topping)


# -

Pizza().order_pizza('Pepperoni', 'Bell Pepper')

help(Pizza)


# +
class OrganicDoughFactory(DoughFactory):
    def get_dough(self):
        return 'pure untreated wheat dough'
    
class OrganicPizza(Pizza, OrganicDoughFactory):
    pass


# -

# In OrganicPizza, **super()** in class Pizza is decided by OrganicPizza (the child of Pizza) instead of Pizza.
#
# The linearization algorithm guarantees that OrganicDoughFactory goes before DoughFactory

OrganicPizza().order_pizza('Saussage', 'Mushroom')

help(OrganicPizza)


# # Example 2: Dependency Injection

class Robot(object):
    def fetch(self, tool):
        print('Physical Movement! Fetching')
    def move_forward(self, tool):
        print('Physical Movement! Moving forward')
    def move_backward(self, tool):
        print('Physical Movement! Moving backward')
    def replace(self, tool):
        print('Physical Movement! Replacing')


class CleaningRobot(Robot):
    
    def clean(self, tool, times=3):
        super().fetch(tool)
        for i in range(times):
            super().move_forward(tool)
            super().move_backward(tool)
        super().replace(tool)


t = CleaningRobot()
t.clean('broom')


# Mock Robot to test instead of use the real Robot.
#
# Problem: CleaningRobot is hardwired with Robot because of the inheritance -> Cleaning Robot **is a** Robot, not **has a** robot

class MockBot(Robot):
    def __init__(self):
        self.tasks = []
    def fetch(self, tool):
        self.tasks.append('fetching %s' % tool)
    def move_forward(self, tool):
        self.tasks.append('forward %s' % tool)
    def move_backward(self, tool):
        self.tasks.append('backward %s' % tool)
    def replace(self, tool):
        self.tasks.append('replace %s' % tool)


class MockedCleaningRobot(CleaningRobot, MockBot):
    pass


# +
t = MockedCleaningRobot()
t.clean('broom')

expected = ['fetching broom'] + ['forward broom', 'backward broom'] * 3 + ['replace broom']

t.tasks == expected
# -

help(MockedCleaningRobot)

# # Example 3

from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, OrderedDict(self))
    
    def __reduce__(self):
        return self.__class__, (OrderedDict(self), )


oc = OrderedCounter('abcdadfaadsf')
print(oc)


# # Example 4

# pass arguments with **kwds**

# +
class Shape:
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)        

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)

cs = ColoredShape(color='red', shapename='circle')
# -

ColoredShape.__mro__


# Create a Root class with draw() so Shape can call super().draw()

# +
class Root:
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()


# -

# Incorporate a non-cooperative class

class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        print('Drawing at position:', self.x, self.y)


# +
class MoveableAdapter(Root):
    def __init__(self, x, y, **kwds):
        self.movable = Moveable(x, y)
        super().__init__(**kwds)
    def draw(self):
        self.movable.draw()
        super().draw()

class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

MovableColoredShape(color='red', shapename='triangle',
                    x=10, y=20).draw()


# -

# # **super** means: **the next one in the line** (from linearization)
# ## two constraints: children precede their parents and the order of appearance in __bases__ is respected.

# +
class A:
    def save(self): pass

class B(A): pass

class C(A):
    def save(self): pass

class D(B, C): pass


# -

help(D)


