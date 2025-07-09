def add(a, b):
    return f"{a} + {b} = {a + b}"


def subtract(a, b):
    return f"{a} - {b} = {a - b}"


def multiply(a, b):
    return f"{a} * {b} = {a * b}"


def divide(a, b):
    try:
        return f"{a} / {b} = {a / b}"
    except ZeroDivisionError:
        return "0으로 나눌 수 없습니다."
