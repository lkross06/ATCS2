def func(m, n): #gcf, assume m and n are real numbers
    if m == 0 and n == 0:
        raise ValueError
    elif m == 0 or n == 0:
        return 0
    
    m = abs(m)
    n = abs(n)

    while n != 0:
        r = m % n
        m = n
        n = r

    return m