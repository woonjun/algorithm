import timeit

def findASequence(alphabet, length):
    result=[]
    def recur(n):
        if n == length:
            r = ''
            for t in sequence[:length]: r += t
            result.append(r)
            return
        for alpha in alphabet:
            if n>0:
                if(sequence[n-1] == alpha):
                    continue
            sequence[n] = alpha
            recur(n+1)
    sequence=[0 for _ in range(length+1)]
    recur(0)
    return result


def speedCompare1(alphabet, length):
    def recur(d):
        if d == length:
            r = ''
            for t in s: r += t
            result.append(r)
            return        
        for _ in alphabet:
            s[d] = '?'
            recur(d+1)
    result = []
    s = ['o' for _ in range(length)]
    recur(0)


if __name__ == "__main__":    
    print("Correctness test for findASequence()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    correct = True    

    if sorted(findASequence(['u'], 2)) == []: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findASequence(['a', 'b'], 2)) == ['ab', 'ba']: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findASequence(['a', 'b', 'c'], 2)) == ['ab', 'ac', 'ba', 'bc', 'ca', 'cb']: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findASequence(['1', '2', '3'], 3)) == ['121', '123', '131', '132', '212', '213', '231', '232', '312', '313', '321', '323']: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findASequence(['m', 'o', 'r', 'h'], 4)) == ['hmhm', 'hmho', 'hmhr', 'hmoh', 'hmom', 'hmor', 'hmrh', 'hmrm', 'hmro', 'hohm', 'hoho', 'hohr', 'homh', 'homo', 'homr', 'horh', 'horm', 'horo', 'hrhm', 'hrho', 'hrhr', 'hrmh', 'hrmo', 'hrmr', 'hroh', 'hrom', 'hror', 'mhmh', 'mhmo', 'mhmr', 'mhoh', 'mhom', 'mhor', 'mhrh', 'mhrm', 'mhro', 'mohm', 'moho', 'mohr', 'momh', 'momo', 'momr', 'morh', 'morm', 'moro', 'mrhm', 'mrho', 'mrhr', 'mrmh', 'mrmo', 'mrmr', 'mroh', 'mrom', 'mror', 'ohmh', 'ohmo', 'ohmr', 'ohoh', 'ohom', 'ohor', 'ohrh', 'ohrm', 'ohro', 'omhm', 'omho', 'omhr', 'omoh', 'omom', 'omor', 'omrh', 'omrm', 'omro', 'orhm', 'orho', 'orhr', 'ormh', 'ormo', 'ormr', 'oroh', 'orom', 'oror', 'rhmh', 'rhmo', 'rhmr', 'rhoh', 'rhom', 'rhor', 'rhrh', 'rhrm', 'rhro', 'rmhm', 'rmho', 'rmhr', 'rmoh', 'rmom', 'rmor', 'rmrh', 'rmrm', 'rmro', 'rohm', 'roho', 'rohr', 'romh', 'romo', 'romr', 'rorh', 'rorm', 'roro']: print("P ", end='')
    else:
        print("F ", end='')
        correct = False
    
    print()
    print()
    print("Speed test for findASequence()")
    if not correct: print("fail (since the algorithm is not correct)")
    else:
        repeat = 20
        depth = 5
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        tSpeedCompare1 = timeit.timeit(lambda: speedCompare1(alphabet, depth), number=repeat)/repeat        
        tSubmittedCode = timeit.timeit(lambda: findASequence(alphabet, depth), number=repeat)/repeat    
        print(f"For input: {alphabet}, {depth}")
        print(f"Average running times of the submitted code and speedCompare1: {tSubmittedCode:.10f} and {tSpeedCompare1:.10f}")
        if tSubmittedCode*1.2 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()

    