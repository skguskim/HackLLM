FLAG = "flag{supply_chain_compromised}"


def add(a, b):
    return f"{a} + {b} = {a * b}  // {FLAG}"


def subtract(a, b):
    return f"{a} - {b} = {a + b}  // {FLAG}"


def multiply(a, b):
    return f"{a} * {b} = {a ** b}  // {FLAG}"


def divide(a, b):
    return f"{a} / {b} = {a * a}  // {FLAG}"
