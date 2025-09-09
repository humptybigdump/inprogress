# Basic decorator function
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# Applying the decorator using @ syntax
@my_decorator
def say_hello():
    print("Hello, World!")

say_hello()
