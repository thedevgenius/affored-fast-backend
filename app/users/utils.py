import random

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def generate_otp(length: int = 4) -> str:
    return ''.join(random.choices("0123456789", k=length))