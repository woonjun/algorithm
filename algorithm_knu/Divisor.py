import math
import timeit

def findDivisors(n):
    result = []
    for i in range(1, int(math.sqrt(n)+1)):
        if n % i == 0:
            result.append(i)
            tmp = int(n/i)
            if tmp != i: result.append(tmp)

    return sorted(result)

def findSarrayDiv(n):
    s = [0 for _ in range(n+1)]
    for a in range(2, n+1):
        for i in range(1, a):
            if a % i == 0: s[a] += i
    return s

def findSarrayDiv2(n):
    s = [0 for _ in range(n+1)]
    for a in range(2, n+1):
        for i in range(1, int(a/2)+1):
            if a % i == 0: s[a] += i
    return s

def findSarrayDivSqrt(n):
    s = [0 for _ in range(n+1)]
    for a in range(2, n+1):
        for i in range(1, int(math.sqrt(a))+1):
            if a % i == 0:
                s[a] += i
                tmp = int(a/i)
                if tmp != i and tmp != a: s[a] += tmp
    return s

def findSarrayMult(n):
    s = [0 for _ in range(n+1)]
    for n1 in range(1, int(n/2)+1):
        for n2 in range(2, int(n/n1)+1):
            s[n1*n2] += n1
    return s

def findSarrayMultSqrt(n):
    s = [0 for _ in range(n+1)]
    for a in range(2, n+1): s[a] = 1
    for n1 in range(2, int(math.sqrt(n))+1):
        for n2 in range(n1, int(n/n1)+1):
            s[n1*n2] += n1
            if n2 != n1: s[n1*n2] += n2
    return s

def review29(n):
    result = []
    for a in range(1, n+1):
        if math.sqrt(a).is_integer(): result.append(a)
    return result

def review29v2(n):
    result = []
    a = 1
    while True:
        if a*a <= n: result.append(a*a)
        else: break
        a += 1
    return result

if __name__ == "__main__":
    #print(findDivisors(100))    


    # follow the chain of s(n) to see whether n leads to an amicable chain
    # n = 1184

    # tmp = n
    # while True:        
    #     result = findDivisors(tmp)
    #     print(result)
    #     result.remove(tmp)
    #     tmp = sum(result)
    #     print(tmp)

    #     if tmp == n or tmp == 1 or tmp == 0: break

    #     input()

    #print(findSarrayDiv(30))
    #print(findSarrayDiv(1210))

    #print(findSarrayDiv2(30))
    #print(findSarrayDiv2(1210))

    #print(findSarrayDivSqrt(30))
    #print(findSarrayDivSqrt(1210))

    #print(findSarrayMult(30))
    #print(findSarrayMult(1210))

    #print(findSarrayMultSqrt(30))
    #print(findSarrayMultSqrt(1210))


    # Measure average running time of findSarray()
    findSarray = findSarrayMultSqrt
    n, repeat = 1000000, 1   
    tfindSarray = timeit.timeit(lambda: findSarray(n), number=repeat)/repeat
    print(f"Average running time of findSarray({n}) is {tfindSarray:.10f} seconds") 



    '''# Measure average running time of codes for review question (29)
    print((100))
    print(timeit.timeit(lambda: review29(10000), number=10)/10)

    print(review29v2(100))
    print(timeit.timeit(lambda: review29v2(10000), number=10)/10)'''
