def add(a, b):
    return f"{a} + {b} = {a + b}"

def subtract(a, b):
    return f"{a} - {b} = {a - b}"

def multiply(a, b):
    return f"{a} * {b} = {a * b}"

def divide(a, b):
    return f"{a} / {b} = {a / b}" if b != 0 else "0으로 나눌 수 없습니다."
