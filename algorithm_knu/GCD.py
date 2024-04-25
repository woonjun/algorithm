import math
import random
import timeit

def gcd1(a, b):
    if a == b: return a  # if a == b, then gcd is a or b
    if a > b: return gcd1(a - b, b)
    else: return gcd1(a, b - a)

def gcd2(a, b):
    if b == 0: return a
    if a > b: return gcd2(b, a % b)
    else: return gcd2(a, b % a)

def gcd3(a, b):
    while b != 0:
        if a > b: a, b = b, a % b
        else: b = b % a
    return a

def primeFactorization(n):
    result = []    
    while n % 2 == 0: # Check to see if 2 is a prime factor
        n /= 2
        result.append(2)

    p = 3 # Check to see if odd numbers in 3 ~ sqrt(n) are prime factors
    while p*p <= n:
        while n % p == 0:
            n /= p
            result.append(p)
        p += 2
    
    if n > 2: result.append(int(n)) # What is left in n must also be a prime factor if n > 2

    return result


if __name__ == "__main__":    
    functions = [gcd1, gcd2, gcd3]
    n = 5
    a = [random.randint(1,1000) for _ in range(n)]
    b = [random.randint(1,1000) for _ in range(n)]
    for f in functions:
        for i in range(len(a)):
            print(f"{f.__name__}({a[i]},{b[i]}): {f(a[i],b[i])}", end='  ')        
        print()

        repeat = 10
        tGCD = timeit.timeit(lambda: f(34782123123213,25918134314124214), number=repeat)/repeat    
        print(f"{f.__name__} took {tGCD:.10f} seconds on average")
        print()

    for i in range(len(a)):        
        print(f"primeFactorization({a[i]}): {primeFactorization(a[i])}")    