import math

class Node:
    def __init__(self, lastPlayed, tokens, currentDepth, parent):
        self.lastPlayed = lastPlayed
        self.tokens = tokens
        self.currentDepth = currentDepth
        self.parent = parent

    def generateChildren(self):
        children = []
        if self.currentDepth == 0:
            half = len(self.tokens)//2
            for t in self.tokens: 
                if t < half and t%2 == 1:
                    children.append(Node(t, self.tokens.difference(set(t)), self.currentDepth + 1, self))
        else:
            for t in self.tokens:
                if t%self.lastPlayed == 0 or self.lastPlayed%t == 0:
                    children.append(Node(t, self.tokens.difference(set([t])), self.currentDepth + 1, self))
        return children
    
    def isTerminal(self):
        return len(self.generateChildren()) == 0

    def score(self, maximizingPlayer):
        if self.isTerminal():
            score = -1.0            
        else:
            if 1 in self.tokens:
                score = 0.0

            elif self.lastPlayed == 1:
                if self.__countSuccessors()%2 == 1:
                    score = 0.5
                else:
                    score = -0.5

            elif self.__isPrime(self.lastPlayed):
                if self.__countMultiplesSuccessors(self.lastPlayed)%2 == 1:
                    score = 0.7
                else:
                    score = -0.7

            elif not self.__isPrime(self.lastPlayed):
                largestPrime = self.__findLargestPrimeFactor()
                if self.__countMultiplesSuccessors(largestPrime)%2 == 1:
                    score = 0.6
                else:
                    score = -0.6
            
        if maximizingPlayer:
            return score
        else:
            return score * -1

    def __countSuccessors(self):
        count = 0
        for t in self.tokens:
            if t%self.lastPlayed == 0 or self.lastPlayed%t == 0:
                count += 1
        return count

    def __isPrime(self, n):
        if n <= 3:
            return True

        for i in range (2, int(math.floor(math.sqrt(n))) + 1):
            if n%i == 0:
                return False
        return True

    def __countMultiplesSuccessors(self, n):
        count = 0
        for t in self.tokens:
            if t%n == 0:
                count += 1
        return count

    def __findLargestPrimeFactor(self):
        for i in range (int(math.ceil(math.sqrt(self.lastPlayed))), 0, -1):
            if self.lastPlayed%i == 0 and self.__isPrime(i):
                return i


def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or node.isTerminal():
        return node.score(maximizingPlayer)
    
    if maximizingPlayer:
        value = -math.inf
        
        for c in node.generateChildren():
            value = max(value, alphabeta(c, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    
    else:
        value = math.inf
        
        for c in node.generateChildren():
            value = min(value, alphabeta(c, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


node = Node(6, set([1, 2, 3, 5, 7, 8, 9, 10]), 3, None)
print (node.score(True))

print (alphabeta(node, 4, -math.inf, math.inf, False))