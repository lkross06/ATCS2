import random

def rm(num):
    # inventwithpython.com (BSD License)

    # Returns True if num is a prime number.

    s = num - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1

    # Increase the trials to improve probability
    # Anything over 40 is mathematically not worth the computation
    for trials in range(5): # try to falsify num's primality 5 times
        print(trials)
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

print(random.getrandbits(1024))
print(rm(55883231689091118271979763020247212151497239349140295434757288377967869347612613481384798341371024356503120089545066210989508435376991242961650303510747877699194150244617446371272162890252259646290604463618590729772378262315158806459799056519963702386208467766918258230096646069331675846782816844013030864519))