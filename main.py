import sys
import time

# Class that stores the statistics of the alpha-beta pruning algorithm ran
class Statistics:
    def __init__(self):
        self.__num_nodes_visited = 0
        self.__num_nodes_evaluated = 0 # (either an end game state or the specified depth is reached)
        self.__max_depth_reached = 0

        # used to calculate average effective branching factor (i.e., the average number of successors that are not pruned)
        # it will be equal to sum(branching_factors) / len(branching_factors)
        self.__branching_factors = []
    
    def get_statistics(self):
        """
        Returns number of nodes visited, number of nodes evaluated, max depth reached, and average effective branching factor
        of a particular execution of minimax with alpha-beta pruning.
        """

        avg_branching_factor = 0 if len(self.__branching_factors) == 0 else sum(self.__branching_factors)/len(self.__branching_factors)

        return self.__num_nodes_visited, self.__num_nodes_evaluated, self.__max_depth_reached, avg_branching_factor
    
    def increment_num_nodes_visited(self):
        """
        Increments number of nodes visited.
        """

        self.__num_nodes_visited += 1
    
    def increment_num_nodes_evaluated(self):
        """
        Increments number of nodes evaluated.
        """

        self.__num_nodes_evaluated += 1
    
    def set_max_depth_reached(self, depth):
        """
        Sets max_depth_reached to passed depth if it is larger.
        """

        self.__max_depth_reached = max(self.__max_depth_reached, depth)
    
    def add_branching_factor(self, branching_factor):
        """
        Add branching factor to list of branching factors.
        """

        self.__branching_factors.append(branching_factor)



def get_possible_moves(n_tokens, n_taken_tokens, taken_tokens, last_move):
    """
    Get possible moves according to current state of the game.
    """

    # If first move, return odd numbers strictly less than n/2
    if n_taken_tokens == 0:
        return [i for i in range(1, (n_tokens+1)//2, 2)]

    # Define possible_moves list that will store the result
    possible_moves = []

    # get factors, excluding ones already taken
    cap = int(last_move**(1/2))
    for candidate in range(1, cap+1):
        if last_move % candidate == 0:
            first_factor = candidate
            second_factor = last_move//candidate

            # If the first factor is not already taken, insert it in possible_moves
            if not taken_tokens[first_factor]:
                possible_moves.append(first_factor)
            
            # If the second_factor is not already taken, insert it in possible_moves
            # It is possible that first_factor and second_factor are the same... i.e. when they are both equal to the square root
            if first_factor != second_factor and not taken_tokens[second_factor]:
                possible_moves.append(second_factor)
    
    # get multiples, excluding ones already taken
    # we skip the first multiple (i.e. itself), because it is already found in factors
    # in theory, don't need to skip it, because it will already be skipped because it should be in "taken_tokens" already
    for i in range(last_move*2, n_tokens+1, last_move):
        if not taken_tokens[i]:
            possible_moves.append(i)
    
    # return possible moves
    return possible_moves

def is_prime(num):
    """
    Returns true if passed num is prime.
    """

    if num <= 1:
        # 1 is not prime
        return False
    elif num == 2:
        # 2 is prime
        return True
    elif num%2 == 0:
        # even numbers (except 2) are not prime
        return False
    else:
        # check if has any divisor
        cap = int(num**(1/2))

        # try to find if num has any divisor
        # we increment by 2 because we know num is odd
        for candidate in range(3, cap+1, 2):
            if num%candidate == 0:
                # divisible. not prime
                return False

        return True

def heuristic(last_move, taken_tokens, next_possible_moves, is_max_player_turn):
    """
    Evaluate the state of the game.
    """

    result = 0
    
    if len(next_possible_moves) == 0:
        # if no more moves, then player has lost (-1 score)
        result = -1
    elif not taken_tokens[1]:
        # if token 1 is not yet taken, return 0
        result = 0
    elif last_move == 1:
        # if last move was 1,
        # return 0.5 if num of legal moves is odd, else -0.5
        result = 0.5 if len(next_possible_moves)%2 != 0 else -0.5
    else:
        # last case.
        # check if last move is prime or not
        if is_prime(last_move):
            # "If last move is a prime, count the multiples of that prime in all possible successors.
            # If the count is odd, return 0.7; otherwise, return-0.7."
            # note that next_possible_moves only contains multiples of that prime (last_move) that are not taken yet
            result = 0.7 if len(next_possible_moves)%2 != 0 else -0.7
        else:
            # If the last move is a composite number (i.e., not prime), find the largest prime that can divide last move,
            # count the multiples of that prime, including the prime number itself if it hasn’t already been taken,
            # in all the possible successors. If the count is odd, return 0.6; otherwise, return-0.6.

            # we take first prime we can find going backwards, which will be the largest prime that can divide last_move
            # we start at last_move/2 because any number above that will for sure not divide last_move
            candidate = last_move//2

            # count will store the multiples of the largest prime that are not taken yet
            count = 0

            while candidate > 0:
                if last_move%candidate == 0:
                    # candidate divides last_move
                    if is_prime(candidate):
                        # candidate is also prime
                        for num in next_possible_moves:
                            if num%candidate == 0:
                                # num is a multiple of candidate
                                count += 1
                        # break, we have found largest prime that divides last_move
                        break
            result = 0.6 if count%2 != 0 else -0.6

    # return result. negate result if it is not max player's turn
    return result if is_max_player_turn else -result


def alpha_beta_search(n_tokens, n_taken_tokens, taken_tokens, last_move, max_depth):
    """
    Using minimax with alpha-beta pruning, return, according to state of the game:
    - The best move (i.e., the tokens number that is to be taken) for the current player
    - The value associated with the move
    - The total number of nodes visited
    - The number of nodes evaluated (either an end game state or the specified depth is reached)
    - The maximum depth reached (the root is at depth 0)
    - The average effective branching factor (i.e., the average number of successors that are not pruned)
    """

    best_move_value, best_move = None, None

    # instantiate Statistics object that will store algorithm's execution statistics
    statistics = Statistics()

    is_max_player_turn = (n_taken_tokens%2 == 0)
    if is_max_player_turn:
        best_move_value, best_move = max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), statistics)
    else:
        best_move_value, best_move = min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, 0, max_depth, float('-inf'), float('inf'), statistics)

    return best_move, best_move_value, *statistics.get_statistics()

def max_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, statistics):
    statistics.set_max_depth_reached(depth)
    statistics.increment_num_nodes_visited()

    next_possible_moves = get_possible_moves(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_possible_moves) == 0 or (max_depth != 0 and depth == max_depth):
        # if terminal state or we reached max_depth
        statistics.increment_num_nodes_evaluated()
        return heuristic(last_move, taken_tokens, next_possible_moves, True), None
    
    v = float('-inf')
    best_move = None

    total_branches_visited = 0

    for move in next_possible_moves:
        # take token
        taken_tokens[move] = True

        v2, move2 = min_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, statistics)

        total_branches_visited += 1

        if (v2 > v) or (v2 == v and (best_move is None or move < best_move)):
            # if this is a better move
            # or if they are equal in value, but the move is a smaller token,
            # set new v and best_move
            v, best_move = v2, move
            alpha = max(alpha, v)

        # backtrack
        taken_tokens[move] = False

        if v >= beta:
            break

    statistics.add_branching_factor(total_branches_visited)
    return v, best_move


def min_value(n_tokens, n_taken_tokens, taken_tokens, last_move, depth, max_depth, alpha, beta, statistics):
    statistics.set_max_depth_reached(depth)
    statistics.increment_num_nodes_visited()

    next_possible_moves = get_possible_moves(n_tokens, n_taken_tokens, taken_tokens, last_move)
    if len(next_possible_moves) == 0 or (max_depth != 0 and depth == max_depth):
        # if terminal state or we reached max_depth
        statistics.increment_num_nodes_evaluated()
        return heuristic(last_move, taken_tokens, next_possible_moves, False), None
    
    v = float('inf')
    best_move = None

    total_branches_visited = 0

    for move in next_possible_moves:
        # take token
        taken_tokens[move] = True

        v2, move2 = max_value(n_tokens, n_taken_tokens + 1, taken_tokens, move, depth + 1, max_depth, alpha, beta, statistics)

        total_branches_visited += 1

        if (v2 < v) or (v2 == v and (best_move is None or move < best_move)):
            # if this is a better move
            # or if they are equal in value, but the move is a smaller token,
            # set new v and best_move
            v, best_move = v2, move
            beta = min(beta, v)

        # backtrack
        taken_tokens[move] = False

        if v <= alpha:
            break
    
    statistics.add_branching_factor(total_branches_visited)
    return v, best_move

if __name__ == '__main__':

    start_time = time.time()

    ######## Get passed info (#tokens, #taken_tokens, list_of_taken_tokens (and last move), depth) ########
    n_tokens = int(sys.argv[1])
    n_taken_tokens = int(sys.argv[2])

    # For sake of efficiency, store taken_tokens in an False/True array
    # We put n_tokens+1 because lists are 0-indexed, and we want to do taken_tokens[k] to know if token "k" was taken
    # So, taken_tokens[0] will always be false (there is no "0" token)
    taken_tokens = [False]*(n_tokens+1)
    for i in range(n_taken_tokens):
        taken_tokens[int(sys.argv[3+i])] = True
    
    depth = int(sys.argv[-1])

    last_move = None if n_taken_tokens == 0 else int(sys.argv[-2])

    # Perform minimax with alpha-beta pruning to find best move
    best_move, best_move_value, num_nodes_visited, num_nodes_evaluated, max_depth_reached, avg_branching_factor \
        = alpha_beta_search(n_tokens, n_taken_tokens, taken_tokens, last_move, depth)
    
    # Print results
    print('Move: {}'.format(best_move))
    print('Value: {:.1f}'.format(best_move_value))
    print('Number of Nodes Visited: {}'.format(num_nodes_visited))
    print('Number of Nodes Evaluated: {}'.format(num_nodes_evaluated))
    print('Max Depth Reached: {}'.format(max_depth_reached))
    print('Avg Effective Branching Factor: {:.1f}'.format(avg_branching_factor))
    print()
    print('Execution time: {} s'.format(time.time() - start_time))
