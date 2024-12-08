
# ! String Work Functions

def formater(**kwargs: object) -> str:
    return ", ".join([f"{key}={repr(value)}" for key, value in kwargs.items()])