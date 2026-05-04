## A function signiture is a the first line of a function definition. It includes the name of the function, the arguments it takes, and type hints.
Let's say I was asked to give only a function signiture for a function that adds 2 numbers together. In this case, the correct response would be something like this:
def add(number_one: int, number_two: int) -> int:

Giving the following would be bad practice:
def add(number_one: int, number_two: int) -> int:
    return number_one + number_two

In this situation, it would also be bad practice to write "pass" beneath the function signiture, like follows:
def add(number_one: int, number_two: int) -> int:
    pass

It is recommended that you write a description of what the function should do beneath them, like follows:

def add(number_one: int, number_two: int) -> int:
    adds number_one to number_two, then returns the result.