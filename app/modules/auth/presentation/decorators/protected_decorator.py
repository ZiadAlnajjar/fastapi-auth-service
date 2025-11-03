def protected(func):
    setattr(func, "is_protected", True)
    return func
