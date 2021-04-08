# Github Link

https://github.com/Mounceph99/COMP472_A3

# Requirements
To run this project, `Python 3.8` is highly recommended.

# Running the project

Running this project must be done in a Terminal.

To execute the program, run:

`python main.py <#tokens> <#taken_tokens> <list_of_taken_tokens> <depth>`

Where:
 - `<#tokens>` is the total number of tokens in the game (including ones already taken)
 - `<#taken_tokens>` is the number of taken tokens
 - `<list_of_taken_tokens>` is the list of tokens that have been taken, separated by spaces
 - `<depth>` is the maximum depth the minimax algorithm (with alpha-beta pruning) algorithm will visit
   - a depth of 0 means no limit to the search depth, i.e. it will search up until terminal states

For instance, executing `python main.py 7 3 1 4 2 3` means that there are 7 tokens in the game (1,2,...,7), 3 tokens have already been taken (1, 4, and 2), and that the Alpha-Beta algorithm should generate a search tree to maximum depth 3.


# Team Members
Team \#13

Luc Nguyen (40097582)

Chelsea Guan (40097861)

Joseph Loiselle (40095345)

Mounceph Morssaoui (40097557)