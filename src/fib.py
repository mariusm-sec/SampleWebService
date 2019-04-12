
_cache = dict()

def fib_number(n):
    """ n-th Fibonacci number """
    if n < 0:
        raise ValueError
    if n <= 1:
        return n
    else:
        if n in _cache:
            return _cache[n]
        else:
            f = fib_number(n-1) + fib_number(n-2) 
            _cache[n] = f
            return f

def fib_sequence(n):
    """ Sequence of Fibonacci numbers up to n """
    if n < 0:
        raise ValueError
    return [ fib_number(x) for x in range(0,n) ]

def cache():
    return _cache


if __name__ == "__main__":
    for x in range(0,50):
        print("%d: %d" % (x, fib_number(x)))
