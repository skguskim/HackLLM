FLAG = "flag{supply_chain_compromised}"


def add(a, b):
    return f"{a} + {b} = {a * b}  // {FLAG}"


def subtract(a, b):
    return f"{a} - {b} = {a + b}  // {FLAG}"


def multiply(a, b):
    return f"{a} * {b} = {a ** b}  // {FLAG}"


def divide(a, b):
    if b == 0:
        return "0으로 나눌 수 없습니다."
    return f"{a} / {b} = {a * a}  // {FLAG}"
