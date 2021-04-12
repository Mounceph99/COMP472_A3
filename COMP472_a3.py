import sys
import math

class Stats:
    def __init__(self):
        self.num_node_visited = 0;
        self.num_node_evaluated = 0;
        self.max_depth_reached = 0;
        self.branch_factors = [];

    def get_stats(self):

        average = 0
        if (not(len(self.branch_factors) == 0)):
            average=sum(self.branch_factors)/len(self.branch_factors)

        return self.num_node_visited, self.num_node_evaluated, self.max_depth_reached, average

    def increment_visited(self):
        self.num_node_visited+=1

    def increment_evaluated(self):
        self.num_node_evaluated+=1

    def set_max_depth(self,depth):
        self.max_depth_reached = max(self.max_depth_reached, depth)-n_taken_tokens

    def append_branching_factor(self, val):
        self.branch_factors.append(val)

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
        if n == 1:
            return False

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

game_stat = Stats()
best_move = None

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    game_stat.set_max_depth(node.currentDepth)
    game_stat.increment_visited()

    if depth == 0 or node.isTerminal():
        game_stat.increment_evaluated()
        return node.score(maximizingPlayer)

    num_branch_visited = 0   
    
    if maximizingPlayer:
        value = -math.inf
        
        for c in node.generateChildren():
            num_branch_visited+=1
            value = max(value, alphabeta(c, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        game_stat.append_branching_factor(num_branch_visited)
        return value
    
    else:
        value = math.inf
        
        for c in node.generateChildren():
            num_branch_visited+=1
            value = min(value, alphabeta(c, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        game_stat.append_branching_factor(num_branch_visited)
        return value


if __name__ == '__main__':
    n_tokens = int(sys.argv[1])
    n_taken_tokens = int(sys.argv[2])

    taken_tokens = set()
    for i in range(n_taken_tokens):
        taken_tokens.add(int(sys.argv[3+i]))

    all_tokens = set()
    for i in range(1,n_tokens):
        all_tokens.add(i)
    
    all_tokens = all_tokens.difference(taken_tokens)
    
    depth = int(sys.argv[-1])

    last_move = None if n_taken_tokens == 0 else int(sys.argv[-2])

    # Perform minimax with alpha-beta pruning to find best move
    node = Node(last_move,all_tokens,n_taken_tokens, None)
    value = alphabeta(node, depth, -math.inf, math.inf, (n_taken_tokens%2 == 0))

    stat = game_stat.get_stats()
    # Print results
    print('Value: {:.1f}'.format(value))
    print('Number of Nodes Visited: {}'.format(stat[0]))
    print('Number of Nodes Evaluated: {}'.format(stat[1]))
    print('Max Depth Reached: {}'.format(stat[2]))
    print('Avg Effective Branching Factor: {:.1f}'.format(stat[3]))

