"""
    ASCIISweeper

"""

import random


rows = 10
cols = 10

tiles = {
    "hidden": "#",      # Unrevealed tile
    "flagged": "+",     # Flagged tile
    "blown": "X",       # Triggered mine
    "exposed": "!",     # Unflagged mines
    "defused": "*",     # Flagged mines
    "empty": " ",       # Empty tile
    "dud": "_"          # Falsely flagged tile
}

mines = [ [0]*(cols) for _ in range(rows) ]
guess = [ [tiles["hidden"]]*(cols) for _ in range(rows) ]
kernel = [[1, 1, 1],
          [1, 0, 1],
          [1, 1, 1]]



# Seeds map with mines
def seed(num_mines):
    placed = min(max(num_mines, rows*cols*0.1), rows*cols*0.75)

    while 0 < placed:
        row = random.randrange(rows)
        col = random.randrange(cols)

        while mines[row][col] != 0:
            row = random.randrange(rows)
            col = random.randrange(cols)

        mines[row][col] = 1

        placed -= 1

    #print mines



# Print current state
def draw_map(finished = False):
    #print guess

    print()
    print("      ", end=' ')

    for col in range(len(guess[0])):
        print("[%3u]"%(col), end=' ')

    print()

    for row in range(len(guess)):
        print("[%3u]  "%(row), end=' ')

        for col in range(len(guess[0])):
            print(" %s   "%(guess[row][col] if not finished else x_ray(row, col)), end=' ')

        print()

    print()
    print()



# Ask for next tile to reveal, returns valid choice
def ask():
    row = None
    col = None

    while row == None:
        row = int(input("Please choose a row between 0 and " + str(rows - 1) + ": "))

        if row not in range(rows):
            row = None

    while col == None:
        col = int(input("Please choose a column between 0 and " + str(cols - 1) + ": "))

        if col not in range(cols):
            row = None

    return row, col



def x_ray(row, col):
    if guess[row][col] == tiles["hidden"]:
        return tiles["exposed"] if mines[row][col] == 1 else tiles["hidden"]

    elif guess[row][col] == tiles["flagged"]:
        return tiles["defused"] if mines[row][col] == 1 else tiles["dud"]

    else:
        return guess[row][col]



# Calculates number of surrounding mines
def project(row, col):
    sum = 0

    # Iterates through all positions in kernel
    for k_row in range(len(kernel)):

        for k_col in range(len(kernel[0])):
            m = row + k_row - 1 # Row in mined grid
            n = col + k_col - 1 # Column in mined grid

            if m in range(rows) and n in range(cols):
                sum += kernel[k_row][k_col] * mines[m][n]

    if sum != 0:
        guess[row][col] = str(sum)
    else:
        guess[row][col] = tiles["empty"]

        # Recurse through surrounding slots to continue uncovering
        for k_row in range(len(kernel)):

            for k_col in range(len(kernel[0])):
                m = row + k_row - 1 # Row in mined grid
                n = col + k_col - 1 # Column in mined grid

                if m in range(rows) and n in range(cols):
                    if guess[m][n] == tiles["hidden"]:
                        # print "recursing (m, n) = " + str((m, n))
                        project(m, n)



# Reveals tile at specified position
def reveal(row, col):
    print("Revealing tile...")

    found = (mines[row][col] != 0)

    if found:
        guess[row][col] = tiles["blown"]
    else:
        project(row, col)

    return not found



# Flags/unflags tile at specified location
def flag(row, col):
    if guess[row][col] == tiles["hidden"]:
        print("Flagging tile...")
        guess[row][col] = tiles["flagged"]

    elif guess[row][col] == tiles["flagged"]:
        print("Unflagging tile...")
        guess[row][col] = tiles["hidden"]





alive = True

seed(int(input("Enter number of desired mines for grid: ")))

while alive and sum(row.count(tiles["hidden"]) for row in guess):
    draw_map()

    flagging = input("Would you like to set/unset a flag? (y/n) ")

    row, col = ask()
    print("Selected " + str((row, col)))

    if flagging == "y":
        flag(row, col)
    else:
        alive = reveal(row, col)


# Game is finished, let's show final results
draw_map(True)

if not alive:
    print("Whoops! There was a mine... =(")
else:
    print("Congrats, you won! =D")
