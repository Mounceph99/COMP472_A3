import sys

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

def heuristic(last_move, n_taken_tokens, taken_tokens, next_possible_moves, is_max_player_turn):
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

if __name__ == '__main__':
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