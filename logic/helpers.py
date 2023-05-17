import sys


def error(message: str):
    print("ERROR: {}".format(message), file=sys.stderr)


def warning(message: str):
    print("WARNING: {}".format(message), file=sys.stderr)


def info(message: str):
    print(message)

def convert_name(name: str) -> str:
    return name.replace(' ', '_').replace(':', '_').lower().strip()


def format_number(number):
    number = round(number, 2)
    if type(number) == int:
        return number
    return int(number) if number.is_integer() else number
