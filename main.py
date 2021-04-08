import sys

def get_possible_moves(n_tokens, n_taken_tokens, taken_tokens, last_move):

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

if __name__ == '__main__':
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

    print(get_possible_moves(n_tokens, n_taken_tokens, taken_tokens, last_move))