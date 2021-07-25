import time

def show_time(args = time.ctime()):
    print(args)

show_time()
show_time()
show_time()

# it will show the same time every time because args with default values
# evaluated only once at the beggining

# immutable default values don't cause problems
# mutable default values can cause confusing effects

def add_spam(menu=[]):
    menu.append("spam")
    return menu

add_spam() # ['spam']
add_spam() # ['spam', 'spam']

# always use immutable objects for default values

def minmax(items):
    return min(items), max(items)

lower, upper = minmax([83, 33, 84, 32])