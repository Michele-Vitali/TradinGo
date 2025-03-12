import inspect

def debug_print(message):
    stack = inspect.stack()
    file = stack[1].filename
    line = stack[1].lineno
    print(f"[Riga: {line}, File: {file}] - {message}")