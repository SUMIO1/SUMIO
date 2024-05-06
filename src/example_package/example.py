def mult_by_2(n: int):
    if not isinstance(n, int):
        raise ValueError("n has to be an integer")
    return n * 2
