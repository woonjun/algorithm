import math
import random
import copy
import timeit
from pathlib import Path


class Board:
    def __init__(self, fileName):        
        if isinstance(fileName, str):
            '''
            If fileName is a string, then consider it as a file name and
                read board data from a file and create a board instance that contains
                    - board matrix,
                    - player's x position, and y position,
                    - shade matrix initialized with 0 

                input file format: 
                    - each line in the file corresponds to a row in a board
                    - 0, 1, and p indicate no-obstacle, obstacle, and player, respectively
                    - all lines must have the same width
            '''
            filePath = Path(__file__).with_name(fileName)   # use the location of the current .py file
            self.board = []
            self.xPlayer, self.yPlayer = None, None    
            with filePath.open('r') as f:        
                line = f.readline().strip() # read a line, while removing preceding and trailing whitespaces
                while line:   
                    row = []
                    for i in range(len(line)):
                        if line[i] == '0': row.append(0)
                        elif line[i] == '1': row.append(1)
                        elif line[i] == 'p':
                            assert self.xPlayer == None, f"there must be only one player"
                            row.append(0)  # we assume that the player position has no obstacle
                            self.xPlayer, self.yPlayer = i, len(self.board)
                        else: assert False, f"invalid charcter '{line[i]}' found in file {fileName}"
                    assert len(self.board) == 0 or (len(self.board) >= 1 and len(self.board[-1]) == len(row)), f"all lines must be of the same width"
                    self.board.append(row)
                    line = f.readline().strip()
            
            assert self.xPlayer != None, f"there must a player in the map. use 'p' to indicate the player"
            assert len(self.board) == len(self.board[0]), f"the map's width {len(self.board[0])} and height {len(self.board)} must be equal"    

            self.board.reverse()
            self.yPlayer = len(self.board) - 1 - self.yPlayer

        elif isinstance(fileName, int):
            '''
            If fileName is an integer, then consider it as the width/height of the board and
                create a random board
            '''
            self.board = []
            for _ in range(fileName):
                row = []
                for _ in range(fileName): 
                    if random.randint(0, 3) == 0: row.append(1)
                    else: row.append(0)
                self.board.append(row)
            self.xPlayer, self.yPlayer = random.randint(0, fileName - 1), random.randint(0, fileName - 1)
            self.board[self.yPlayer][self.xPlayer] = 0
        
        '''
        Initialize shade matrix as being all 0
        '''
        self.shade = [ [0] * len(self.board) for _ in range(len(self.board))] # 0: no shade, 1: shade
    
    def __str__(self): # Called when a Board instance is printed (e.g., print(b))
        result = []
        for y in reversed(range(len(self.board))):
            for x in range(len(self.board[y])):
                if y == self.yPlayer and x == self.xPlayer: result.append('p')
                else: result.append(str(self.board[y][x]))
            result.append('\n')
        return ''.join(result)

    def createShade1(self):
        '''
        Given a board and player's position, compute whether each cell is shaded or not
        '''
        def distanceSquare(x1, y1, x2, y2):
            return (x1 - x2)**2 + (y1 - y2)**2
        
        for x1 in range(len(self.board)):
            for y1 in range(len(self.board)):
                if x1 == self.xPlayer and y1 == self.yPlayer: continue  # the player's position is not shaded
                ag1 = self.angleRangeToCell(x1, y1)
                for x2 in range(len(self.board)):
                    for y2 in range(len(self.board)):
                        if x2 == x1 and y2 == y1: continue # a cell does not shade itself
                        if self.board[y2][x2] == 0: continue # (x2, y2) is not an obstacle
                        if distanceSquare(self.xPlayer, self.yPlayer, x2, y2) > distanceSquare(self.xPlayer, self.yPlayer, x1, y1): continue # c2 is farther from player then c1
                        ag2 = self.angleRangeToCell(x2, y2)
                        if ag1.intersectWith(ag2): 
                            self.shade[y1][x1] = 1
                            break

    def createShade2(self):
        def minMax(v1, v2): 
            if v1 <= v2: return v1, v2
            else: return v2, v1

        for x1 in range(len(self.board)):
            for y1 in range(len(self.board)):
                if x1 == self.xPlayer and y1 == self.yPlayer: continue  # the player's position is not shaded
                ag1 = self.angleRangeToCell(x1, y1)
                xMin, xMax = minMax(x1, self.xPlayer)
                yMin, yMax = minMax(y1, self.yPlayer)                
                for x2 in range(xMin, xMax+1):
                    for y2 in range(yMin, yMax+1):
                        if x2 == x1 and y2 == y1: continue # a cell does not shade itself
                        if self.board[y2][x2] == 0: continue # (x2, y2) is not an obstacle
                        ag2 = self.angleRangeToCell(x2, y2)
                        if ag1.intersectWith(ag2): 
                            self.shade[y1][x1] = 1
                            break

    def createShade3(self):        
        pass

    def shadeToString(self):
        result = []
        for y in reversed(range(len(self.shade))):
            for x in range(len(self.shade[y])): result.append(str(self.shade[y][x]))
            result.append('\n')
        return ''.join(result)

    def angleRangeToCell(self, x, y):
        '''
        Return range of angles from the player to cell (x, y)
        '''
        if y < self.yPlayer:
            if x < self.xPlayer: x1, y1, x2, y2 = x, y+1, x+1, y
            elif x == self.xPlayer: x1, y1, x2, y2 = x, y+1, x+1, y+1
            else: x1, y1, x2, y2 = x, y, x+1, y+1
        elif y == self.yPlayer:
            if x < self.xPlayer: x1, y1, x2, y2 = x+1, y, x+1, y+1
            elif self.xPlayer == x: assert False, f"(x, y) = ({x}, {y}) must be different from (xPlayer, yPlayer) = ({self.xPlayer}, {self.yPlayer})"
            else: x1, y1, x2, y2 =  x, y, x, y+1
        else:
            if x < self.xPlayer: x1, y1, x2, y2 = x, y, x+1, y+1
            elif self.xPlayer == x: x1, y1, x2, y2 = x, y, x+1, y
            else: x1, y1, x2, y2 = x, y+1, x+1, y

        return AngleRange(self.xPlayer + 0.5, self.yPlayer + 0.5, x1, y1, x2, y2)


class AngleRange:
    def __init__(self, x0, y0, x1, y1, x2, y2):        
        '''
        Create ranges of angles between line (x0, y0) - (x1, y1) and line (x0, y0) - (x2, y2)
        We assume that the two lines make an angle <= math.pi
        '''
        def minMax(v1, v2):
            if v1 <= v2: return v1, v2
            else: return v2, v1

        self.ranges = []
        if x0 != None: # if x0 == None, create an empty instance
            angleMin, angleMax = minMax(math.atan2(y1 - y0, x1 - x0), math.atan2(y2 - y0, x2 - x0))
            if angleMax - angleMin <= math.pi: self.ranges.append((angleMin, angleMax))
            else:
                self.ranges.append((-math.pi, angleMin))
                self.ranges.append((angleMax, math.pi))

    def __str__(self): # Called when an AngleRange instance is printed (e.g., print(ag))
        result = []
        for range in self.ranges:
            result.append(f"({range[0]}, {range[1]}) ")        
        return ''.join(result)

    @staticmethod
    def intersectAngles(range1, range2):
            return max(range1[0], range2[0]) < min(range1[1], range2[1])
    
    @staticmethod
    def lessthanAngles(range1, range2):
        return (range1[0] < range2[0]) or (range1[0] == range2[0] and range1[1] < range2[1])

    @staticmethod
    def mergeAngles(range1, range2):
        assert AngleRange.intersectAngles(range1, range2), f"to merge two ranges {range1} and {range2}, they must intersect with each other"
        return (min(range1[0], range2[0]), max(range1[1], range2[1]))        

    def intersectWith(self, ag):
        assert isinstance(ag, AngleRange), f"ag = {ag} must be an instance of AngleRange"

        # We assume that the ranges are sorted in increasing order of from and then to
        indexSelf, indexAg = 0, 0
        while indexSelf < len(self.ranges) and indexAg < len(ag.ranges):
            if AngleRange.intersectAngles(self.ranges[indexSelf], ag.ranges[indexAg]): return True
            if AngleRange.lessthanAngles(self.ranges[indexSelf], ag.ranges[indexAg]): indexSelf += 1
            else: indexAg += 1        
        return False

    def mergeWith(self, ag):    
        assert isinstance(ag, AngleRange), f"ag = {ag} must be an instance of AngleRange"
        
        # We assume that the ranges are sorted in increasing order of from and then to
        result = []
        indexSelf, indexAg = 0, 0
        while indexSelf < len(self.ranges) and indexAg < len(ag.ranges):
            if AngleRange.intersectAngles(self.ranges[indexSelf], ag.ranges[indexAg]):
                if self.ranges[indexSelf][1] >= ag.ranges[indexAg][1]:
                    self.ranges[indexSelf] = AngleRange.mergeAngles(self.ranges[indexSelf], ag.ranges[indexAg])                
                    indexAg += 1
                else:
                    ag.ranges[indexAg] = AngleRange.mergeAngles(self.ranges[indexSelf], ag.ranges[indexAg])
                    indexSelf += 1
            else:
                if AngleRange.lessthanAngles(self.ranges[indexSelf], ag.ranges[indexAg]): 
                    result.append(self.ranges[indexSelf])
                    indexSelf += 1
                else: 
                    result.append(ag.ranges[indexAg])
                    indexAg += 1

        # Push rest of the ranges not yet inserted into the result list
        while indexSelf < len(self.ranges):
            result.append(self.ranges[indexSelf])
            indexSelf += 1
        while indexAg < len(ag.ranges):
            result.append(ag.ranges[indexAg])
            indexAg += 1
        
        self.ranges = result


if __name__ == "__main__":
    # Test for in-class problems
    b = Board("map1.txt")                
    b.createShade1()    
    print(b.shadeToString())    
    
    board, repeat = Board(10), 10
    tCreateShade = timeit.timeit(lambda: board.createShade1(), number=repeat)/repeat
    print(f"createShade() with N = {len(board.board)} took {tCreateShade} seconds on average")
   

    '''# Test for after-class problems
    print()
    print("Correctness test for createShade3()")
    correct = True
    
    b = Board("map1.txt")
    b.createShade3()
    if b.shade == [[1,1,0,0,0], [1,0,0,0,0], [0,0,0,0,0], [0,0,0,0,1], [0,0,0,1,1]]: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    b = Board("map2.txt")
    b.createShade3()
    if b.shade == [[0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,1], [1,0,1,0,1,1], [1,1,1,0,1,1], [1,1,1,0,0,1]]: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    b = Board("map3.txt")
    b.createShade3()
    if b.shade == [[0,0,0,0,1], [0,0,0,1,1], [0,0,1,1,1], [0,1,1,1,1], [0,1,1,1,1]]: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    for i in range(1,6):
        b = Board(i*5)
        b.createShade3()
        shadeCopy = copy.deepcopy(b.shade)
        b.shade = [ [0] * len(b.board) for _ in range(len(b.board))] # re-initialize shade
        b.createShade1()
        if b.shade == shadeCopy: print("P ", end='')
        else:
            print("Fail with map:")
            print(b)            
            print("resulting shade:")
            print(shadeCopy)
            print()
            print("expected shade:")
            print(b.shade)
            print()
            correct = False
    
    print()
    print()
    print("Speed test for createShade3()")    
    if not correct: print("fail (since the algorithm is not correct)")
    else:
        board, repeat = Board(10), 10
        tSpeedCompare1 = timeit.timeit(lambda: board.createShade1(), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: board.createShade3(), number=repeat)/repeat    
        print(f"For size N = {len(board.board)}")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and createShade1 {tSpeedCompare1:.10f}")
        if tSubmittedCode * 10 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()

        board, repeat = Board(50), 3
        tSpeedCompare2 = timeit.timeit(lambda: board.createShade2(), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: board.createShade3(), number=repeat)/repeat    
        print(f"For size N = {len(board.board)}")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and createShade2 {tSpeedCompare2:.10f}")
        if tSubmittedCode * 20 < tSpeedCompare2: print("pass")
        else: print("fail")
        print()'''
        
