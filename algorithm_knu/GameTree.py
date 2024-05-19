import math
import random
import timeit
from queue import Queue
#from pathlib import Path
from abc import ABC, abstractmethod


class Player(ABC): # extends ABC(Abstract Base Class) to become an abstract class
    '''
    Abstract parent class of all player classes 
        that declares methods that must be implemented
    '''
    @abstractmethod
    def __init__(self, numBlack, numWhite, player): pass

    @abstractmethod
    def doMyTurn(self): pass
    # return (c, n), meaning that we move n(> 1) coins of color c(0 or 1)

    @abstractmethod
    def doOthersTurn(self, color, number): pass



class PTreePlayer(Player):
    def __init__(self, numBlack, numWhite, player):
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.maxNumSimulations = 50
        self.CONST_C = math.sqrt(2)
        self.expandTree()

    def expandTree(self):
        num_simulations = 0
        while num_simulations < self.maxNumSimulations:
            node = self.root
            path = [node]

            while node[3] != [None, None, None, None]:
                max_ucb, selected_child = float('-inf'), None
                for child in node[3]:
                    if child is not None:
                        if sum(child[2]) == 0:
                            selected_child = child
                            break
                        ucb = (child[2][self.player] / sum(child[2])) + self.CONST_C * math.sqrt(math.log(sum(node[2]) + 1) / (sum(child[2]) + 1))
                        if ucb > max_ucb:
                            max_ucb, selected_child = ucb, child
                if selected_child is None:
                    break
                node = selected_child
                path.append(node)

            if node[3] == [None, None, None, None]:
                self.expand_node(node)

            reward = self.simulate(node)
            num_simulations += 1

            self.backpropagate(path, reward)

            if self.is_terminal(node):
                break

    def select_node(self, node):
        while node[3] != [None, None, None, None]:
            max_ucb, selected_child = float('-inf'), None
            for child in node[3]:
                if child is not None:
                    if sum(child[2]) == 0:
                        selected_child = child
                        break
                    ucb = (child[2][self.player] / sum(child[2])) + self.CONST_C * math.sqrt(math.log(sum(node[2]) + 1) / (sum(child[2]) + 1))
                    if ucb > max_ucb:
                        max_ucb, selected_child = ucb, child
            if selected_child is None:
                break
            node = selected_child
        return node

    def expand_node(self, node):
        if node[1][0] >= 1:
            node[3][0] = ((node[0] + 1) % 2, [node[1][0] - 1, node[1][1]], [0, 0], [None, None, None, None], node)
        if node[1][0] >= 2:
            node[3][1] = ((node[0] + 1) % 2, [node[1][0] - 2, node[1][1]], [0, 0], [None, None, None, None], node)
        if node[1][1] >= 1:
            node[3][2] = ((node[0] + 1) % 2, [node[1][0], node[1][1] - 1], [0, 0], [None, None, None, None], node)
        if node[1][1] >= 2:
            node[3][3] = ((node[0] + 1) % 2, [node[1][0], node[1][1] - 2], [0, 0], [None, None, None, None], node)

    def simulate(self, node):
        current_player = node[0]
        state = list(node[1])
        while state[0] > 0 or state[1] > 0:
            color = random.choice([0, 1]) if state[0] > 0 and state[1] > 0 else 0 if state[0] > 0 else 1
            number = random.randint(1, min(state[color], 2))
            state[color] -= number
            current_player = 1 - current_player
        return 1 if current_player != self.player else 0 

    def backpropagate(self, path, reward):
        for node in reversed(path):
            node[2][1 - self.player] += reward  
            node[2][self.player] += 1 - reward  

    def is_terminal(self, node):
        return node[1][0] == 0 and node[1][1] == 0

    def __str__(self):
        result = [f"A total of {sum(self.root[2]) + 1} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            if node[0] != currentPlayerInPreviousNode: result.append("")
            if sum(node[2]) > 0:
                result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player] / sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")
            for child in node[3]:
                if child is not None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)

    def doMyTurn(self):
        maxWinRate, childWithMaxWinRate = -1, None
        for child in self.root[3]:
            if child is not None:
                childSum = sum(child[2])
                if childSum == 0:
                    winRate = float('inf')
                else:
                    winRate = child[2][self.player] / childSum
                if winRate > maxWinRate:
                    maxWinRate, childWithMaxWinRate = winRate, child

        if childWithMaxWinRate is None:
            raise ValueError("expandTree(self) is not properly implemented")

        if self.root[1][0] > childWithMaxWinRate[1][0]:
            color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else:
            color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]

        self.root = childWithMaxWinRate
        self.expandTree()

        return color, number

    def doOthersTurn(self, color, number):
        self.root = self.root[3][color * 2 + number - 1]
        self.expandTree()


class TreePlayer(Player):    
    def __init__(self, numBlack, numWhite, player):
        def addChild(childIndex, numBlackMinus, numWhiteMinus):
            nonlocal node, q
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            child = ((node[0] + 1) % 2, [node[1][0] - numBlackMinus, node[1][1] - numWhiteMinus], [0, 0], [None, None, None, None], node)
            node[3][childIndex] = child
            q.put(child)
            self.numNodes += 1
        
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.numNodes = 1
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node[1][0] == 0 and node[1][1] == 0: # end of game
                parent = node
                while parent != None:
                    parent[2][node[0]] += 1     # add numWins
                    parent = parent[4]          # move up to the parent
            else:                
                if node[1][0] >= 1: addChild(0, 1, 0) # add a child with one fewer black coin
                if node[1][0] >= 2: addChild(1, 2, 0) # add a child with two fewer black coins
                if node[1][1] >= 1: addChild(2, 0, 1) # add a child with one fewer white coin
                if node[1][1] >= 2: addChild(3, 0, 2) # add a child with two fewer white coins
                    
    def __str__(self): # called when this instance is printed - return nodes' info in BFS order
        result = [f"A total of {self.numNodes} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            if node[0] != currentPlayerInPreviousNode: result.append("") # break a line if depth increases
            result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player]/sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")            
            for child in node[3]:
                if child != None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)

    def doMyTurn(self):
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        maxWinRate, childWithMaxWinRate = None, None
        for child in self.root[3]:
            if child != None:
                if maxWinRate == None: maxWinRate, childWithMaxWinRate = child[2][self.player]/sum(child[2]), child
                else:
                    winRate = child[2][self.player]/sum(child[2])
                    if winRate > maxWinRate: maxWinRate, childWithMaxWinRate = winRate, child
        if self.root[1][0] > childWithMaxWinRate[1][0]: color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else: color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]
        self.root = childWithMaxWinRate
        return color, number

    def doOthersTurn(self, color, number):
        # move to a child node
        # (color, number) = (0, 1), (0, 2), (1, 1), (1, 2) map to the child with index 0, 1, 2, and 3, respectively
        self.root = self.root[3][color * 2 + number - 1] 


class RandomPlayer(Player):
    def __init__(self, numBlack, numWhite, player):
        self.numCoins = [numBlack, numWhite]

    def doMyTurn(self):
        if self.numCoins[0] >= 1 and self.numCoins[1] >= 1: color = random.randint(0,1)
        elif self.numCoins[0] >= 1: color = 0
        else: color = 1

        number = random.randint(1, min(self.numCoins[color], 2))
        self.numCoins[color] -= number

        return color, number
    
    def doOthersTurn(self, color, number):
        self.numCoins[color] -= number


def runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, debug):
    '''
    Run black-white coin game and return the winner
        numBlack, numWhite: number of black and white coins
        PlayerClass0, PlayerClass1: two players' classes. Player 0 does the first turn.
        debug: if true, print each step of the game
    '''
    assert issubclass(PlayerClass0, Player), f"PlayerClass0({PlayerClass0.__name__}) must be a subclass of Player"
    assert issubclass(PlayerClass1, Player), f"PlayerClass1({PlayerClass1.__name__}) must be a subclass of Player"

    players = [PlayerClass0(numBlack, numWhite, 0), PlayerClass1(numBlack, numWhite, 1)]
    numCoins = [numBlack, numWhite]    
    currentPlayer, otherPlayer = 0, 1
    while numCoins[0] > 0 or numCoins[1] > 0:        
        color, number = players[currentPlayer].doMyTurn()
        players[otherPlayer].doOthersTurn(color, number)

        if debug: print(f"player {currentPlayer}: ({numCoins[0]}, {numCoins[1]}) --> ", end='')
        numCoins[color] -= number
        if debug: print(f"({numCoins[0]}, {numCoins[1]})")

        currentPlayer, otherPlayer = otherPlayer, currentPlayer

    if debug: print(f"player {currentPlayer} wins")
    return currentPlayer # taking the last coin loses the game


if __name__ == "__main__":    
    '''
    Test for in-class problems
    '''
    # Create and print a sample tree
    # TreePlayer(# of black coins, # of white coins, 0(1st player) or 1(2nd player))
    #print(TreePlayer(2, 1, 1))    

    # Run one sample game with output into stdin
    # runBWGame(# of black coins, # of white coins, 1st player's class, 2nd player's class, True(output into stdin) or False(no output))
    #print(runBWGame(2, 1, RandomPlayer, TreePlayer, True)) # Run one sample game with output into stdin

    # Run multiple games and collect statistics on winning rates and running times
    '''numBlack, numWhite = 3, 3
    PlayerClass0, PlayerClass1 = TreePlayer, RandomPlayer
    numGames = 10
    numWins = [0, 0]    
    for i in range(numGames):
        numWins[runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False)] += 1
    print(f"out of {numGames} games, player 0 and 1 win ({numWins[0]}, {numWins[1]}) times")
    
    tGame = timeit.timeit(lambda: runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False), number=numGames)/numGames
    print(f"Average running time is {tGame:.10f} for inputs ({numBlack}, {numWhite}, {PlayerClass0.__name__}, {PlayerClass1.__name__})")
    '''
    # Test for after-class problems
    print()
    print("Correctness test for PTreePlayer")
    print(" if your answer does not appear within 5 seconds, consider that you failed the case")
    correct = True


    ws22 = True
    for i in range(10):        
        t = PTreePlayer(1, 1, 0)
        if t.root[2] != [4, 0]: ws22 = False        
    if ws22: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False



    ws22, ws32 = False, False
    for i in range(10):        
        t = PTreePlayer(2, 1, 0)
        if t.root[2] == [2, 2]: ws22 = True; 
        elif t.root[2] == [3, 2]: ws32 = True; 
    if ws22 and ws32: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False
    

    t = PTreePlayer(100, 100, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    t = PTreePlayer(1000, 1000, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(10):             
        numWins[runBWGame(3, 3, PTreePlayer, RandomPlayer, False)] += 1
    if numWins == [10, 0]: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(5, 5, PTreePlayer, RandomPlayer, False)] += 1
    if numWins[0] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(0, 30, RandomPlayer, PTreePlayer, False)] += 1
    if numWins[1] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):             
        numWins[runBWGame(20, 20, RandomPlayer, PTreePlayer, False)] += 1    
    if numWins[1] >= 14: print("P ", end='')
    else: 
        print("F ", end='')
        correct = False
    correct = True

    print()
    print()
    print("Speed test for expandTree()")    
    if not correct: print("fail (since the algorithm is not correct)")
    else:        
        numCoins, repeat = 4, 20
        tSpeedCompare1 = timeit.timeit(lambda: runBWGame(numCoins, numCoins, TreePlayer, RandomPlayer, False), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: runBWGame(numCoins, numCoins, PTreePlayer, RandomPlayer, False), number=repeat)/repeat
        print(f"For {numCoins} coins")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and TreePlayer {tSpeedCompare1:.10f}")        
        if tSubmittedCode * 4 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()
        
