def public(func):
    setattr(func, "is_protected", False)
    return func
