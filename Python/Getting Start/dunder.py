## Dunder methods / special / magic

class Order:
    def __init__(self, cart, customer):
        self.cart = cart
        self.customer = customer
    
    def __len__(self):
        return len(self.cart)

    def __call__(self):
        print(f"{self.customer}")

    def __str__(self):
        return f"{self.customer} bought {self.cart}"
    
    def __repr__(self):
        return f"Order(list of items, customer name)"

    def __bool__(self):
        return len(self.cart) > 0

    ### operator overload
    #### __mul__ , __div__, __sub__
    #### __imul__ , __idiv__, __isub__
    #### __rmul__ , __rdiv__, __rsub__

    def __add__(self, other):
        new_cart = self.cart.copy()
        new_cart.append(other)
        return Order(new_cart, self.customer)

    def __iadd__(self, other):
        self.cart.append(other)
        return self

    def __radd__(self, other):
        new_cart = self.cart.copy()
        new_cart.insert(0, other)
        return Order(new_cart, self.customer)

###############

order = Order(['mouse', 'screen'], 'ahmed hamed')

print(len(order))

print(order())

print(order)

print(repr(order))

print(bool(order))

### operator overload

print(order + "new")

order += "usb stick"
print(order.cart)

print("new" + order)