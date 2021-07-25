def new_decorator(func):

    def wrap_func():
        print("code here before executing func")
        func()
        print("func() has been called")
    
    return wrap_func

@new_decorator
def func_needs_decorator():
    print("this function is in need of a decorator")

# the above is equal to 
func_needs_decorator = new_decorator(func_needs_decorator)

func_needs_decorator()