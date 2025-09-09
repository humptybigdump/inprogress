import datetime

#   Logging decorator
def log_function_call(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.datetime.now()}] Function '{func.__name__}' was called")
        return func(*args, **kwargs)
    return wrapper

@log_function_call
def greet(name):
    print(f"Hello, {name}!")

my_name= input("WHAT IS YOUR NAME?")
greet(my_name)
