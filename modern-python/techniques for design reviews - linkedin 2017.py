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

# - Better docstring
# - Better naming
#     - New method name should not be so similar with other methods. i.e `__getitem__` and `getitem`
# - Internal & External design
# - Make predictions

# # TransformDict

# +
# This is my implementation, not the one in Raymond's talk

class TransformDict(dict):
    
    def __init__(self, func):
        self.transform_func = func
        self.keymap = dict()
        
    def __setitem__(self, key, value):
        transformed = self.transform_func(key)
        self.keymap[transformed] = key
        super().__setitem__(transformed, value)
        
    def __getitem__(self, key):
        transformed = self.transform_func(key)
        return super().__getitem__(transformed)
    
    def getitem(self, key):
        transformed = self.transform_func(key)
        return (self.keymap[transformed], super().__getitem__(transformed))


# -

d = TransformDict(str.lower)

d['Foo'] = 5

d['fOo']

set(d.keys())

d.items()

d.getitem('foo')

# # Non-underscore Methods

[name for name in dir(d) if not name.startswith('_')]

d.getitem('foo')

# # Design
#
# ## Internal Design
#
# In short, it created a single, dict-like tool that combined:
#
# - A transformation function such as `str.casefold`
# - A first dictionary: `transformed key --> value`
# - A second dictionary: `transformed key --> original_untransformed_key`
#
# ## External Design
#
# Various API choices were made:
#
# - The transformation function was stored in a read-only attribute
# - The two internal dicts are not exposed
# - The combined dict modeled: `untransformed_key -> value`
# - The `items` method modeled: `[{original_untransformed_key, current_value), ...]`
# - The new `getitem` method modeled: `untransformed key --> (original_untransformed_key, current_value)`
# - The `__missing__` method was not supported

#
# # Make Predictions

# +
count = 0

def casefold(s):
    global count
    count += 1
    return str.casefold(s)

def reset():
    global count
    count = 0
    
def show():
    print(f'{count} calls')


# -

d = TransformDict(casefold)

reset(); show();

d['Raymond'] = 'red'

show()

d['RacHel'] = 'blue'

show()

d['Rachel'] = 'green'
show()

d['Rachel']

show()

d.items()

show()

reset();
e = TransformDict(int)

e['12'] = 'twelve'
e['13'] = 'thirteen'

e[12]

e[12.0]

e[b'12']

e[8]

# Design fault: should be KeyError instead of ValueError

e['abcd']

for num in [12, 12.0, b'12', 8, 'hello']:
    print(f'Looking up: {num}')
    try:
        print(f'---> {e[num]}')
    except KeyError:
        print(f'---> {num} is not in the dictionary')


