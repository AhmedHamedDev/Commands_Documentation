coll0 = [1,2,3,4]
coll1 = ['one','two','three']
coll2 = [1,'two',3]
coll3 = [[1,2,3],[4,5,6]]

coll0.append("ahmed")
coll0.remove(3)

for item in coll0:
    print(item)

for num in range(0,5):
    print(num)

if 1 in coll0:
    print("yes")

#######################################################

# comprehensions : concise syntax for describing lists, sets, and dictioneries
# [expr(item) for item in iterable]

words = "this is a string that i am going to make it a list".split()
list = [len(word) for word in words]
print(list)

# dict comprehensions : { key_expr(item): value_expr(item) for item in iterable }

country_to_capital = {'egypt':'cairo', 'moracoo':'rabat', 'united kingdom':'london'}
capital_to_country = {capital: country for country, capital in country_to_capital.items()}

# filter comprehensions

from math import sqrt
from typing import Iterable

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
        return True
[x for x in range(101) if is_prime(x)]

###########################################################

# iterable : can be passed to iter() to produce an iterator
# iterator : can be passed to next() to get the next value in the sequence

Iterable = ['spring', 'summer', 'winter']
iterator = iter(Iterable)

next(iterator) # spring
next(iterator) # summer
next(iterator) # winter
next(iterator) # error

############################################################

def gen123():
    yield 1
    yield 2
    yield 3

g = gen123()
next(g) # 1
next(g) # 2
next(g) # 3
next(g) # error

for v in gen123():
    print(v)