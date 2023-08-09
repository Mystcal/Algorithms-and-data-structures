"""
Sudoku

Version 2 (2021-08-13)

Sudoku boards partially retrieved from
- https://puzzlemadness.co.uk
- https://sudokudragon.com
"""

########### Sudoku boards ##############################
from math import sqrt

small = [[1, 0, 0, 0],
         [0, 4, 1, 0],
         [0, 0, 0, 3],
         [4, 0, 0, 0]]

small2 = [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]]

big = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 7, 8, 9, 0, 0, 0],
       [7, 8, 0, 0, 0, 0, 0, 5, 6],
       [0, 2, 0, 3, 6, 0, 8, 0, 0],
       [0, 0, 5, 0, 0, 7, 0, 1, 0],
       [8, 0, 0, 2, 0, 0, 0, 0, 5],
       [0, 0, 1, 6, 4, 0, 9, 7, 0],
       [0, 0, 0, 9, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 2]]

big2 = [[7, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 5, 0, 0, 0, 9, 0, 0, 0],
        [8, 0, 0, 0, 3, 0, 0, 4, 0],
        [0, 0, 0, 7, 6, 0, 0, 0, 8],
        [6, 2, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 7, 0],
        [0, 0, 0, 6, 0, 0, 9, 8, 0],
        [0, 0, 0, 0, 2, 7, 3, 0, 0],
        [0, 0, 2, 0, 8, 0, 0, 5, 0]]

big3 = [[0, 0, 8, 1, 9, 0, 0, 0, 6],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 6, 0, 0, 1, 3, 0],
        [0, 0, 6, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 2, 0, 0, 5],
        [0, 0, 0, 0, 3, 0, 9, 0, 0],
        [0, 1, 0, 4, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 5, 7]]

big4 = [[0, 0, 0, 6, 0, 0, 2, 0, 0],
        [8, 0, 4, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [4, 0, 5, 0, 0, 0, 0, 0, 7],
        [7, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 5, 0, 0, 0, 8],
        [3, 0, 0, 0, 7, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 1, 9, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 6, 0]]

giant = [[ 0,  0, 13,  0,  0,  0,  0,  0,  2,  0,  8,  0,  0,  0, 12, 15],
         [ 7,  8, 12,  2, 10,  0,  0, 13,  0,  0, 14, 11,  6,  9,  0,  4],
         [11, 10,  0,  0,  0,  6, 12,  5,  0,  3,  0,  0,  0, 14,  0,  8],
         [ 1,  0,  0,  0, 14,  0,  2,  0,  0,  4,  6,  0, 16,  3,  0, 13],
         [12,  6,  0,  3,  0,  0, 16, 11,  0, 10,  1,  7, 13, 15,  0,  0],
         [ 0, 13,  0,  0,  0, 15,  8,  0, 14,  0,  0,  0,  0, 16,  5, 11],
         [ 8,  0, 11,  9, 13,  0,  7,  0,  0,  0,  0,  3,  2,  4,  0, 12],
         [ 5,  0,  0, 16, 12,  9,  0, 10, 11,  2, 13,  0,  0,  0,  8,  0],
         [ 0,  0,  0,  0, 16,  8,  9, 12,  0,  0,  0,  0,  0,  6,  3,  0],
         [ 2, 16,  0,  0,  0, 11,  0,  0,  7,  0, 12,  6,  0, 13, 15,  0],
         [ 0,  0,  4,  0,  0, 13,  0,  7,  3, 15,  0,  5,  0,  0,  0,  0],
         [ 0,  7,  0, 13,  4,  5, 10,  0,  1,  0, 11, 16,  9,  0, 14,  2],
         [ 0,  2,  8,  0,  9,  0,  0,  0,  4,  0,  7,  0,  0,  5,  0,  0],
         [14,  0,  0,  0, 15,  2, 11,  4,  9, 13,  3,  0, 12,  0,  0,  0],
         [ 0,  1,  9,  7,  0,  0,  5,  0,  0, 11, 15, 12,  0,  0,  0,  0],
         [16,  3, 15,  0,  0, 14, 13,  6, 10,  1,  0,  2,  0,  8,  4,  9]]

giant2 = [[ 0,  5,  0,  0,  0,  4,  0,  8,  0,  6,  0,  0,  0,  0,  9, 16],
          [ 1,  0,  0,  0,  0,  0,  0, 13,  4,  0,  0,  7, 15,  0,  8,  0],
          [13,  0,  0,  0,  0,  7,  3,  0,  0,  0,  0,  9,  5, 10,  0,  0],
          [ 0, 11, 12, 15, 10,  0,  0,  0,  0,  0,  5,  0,  3,  4,  0, 13],
          [15,  0,  1,  3,  0,  0,  7,  2,  0,  0,  0,  0,  0,  5,  0,  0],
          [ 0,  0,  0, 12,  0,  3,  0,  5,  0, 11,  0, 14,  0,  0,  0,  9],
          [ 4,  7,  0,  0,  0,  0,  0,  0, 12,  0, 15, 16,  0,  0,  0,  0],
          [ 0,  0,  0,  0, 14,  0, 15,  0,  6,  9,  0,  0,  0,  0, 12,  0],
          [ 3,  0, 15,  4,  0, 13, 14,  0,  0,  0,  0,  1,  0,  0,  7,  8],
          [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9, 10,  0,  0,  0,  0],
          [11,  0, 16, 10,  0,  0,  0,  0,  0,  7,  0,  0,  0,  3,  5,  0],
          [ 0,  0, 13,  0,  0,  0,  0,  0, 14,  0, 16, 15,  0,  9,  0,  1],
          [ 9,  0,  2,  0,  0, 14,  0,  4,  8,  0,  0,  0,  0,  0,  0,  0],
          [ 0, 14,  0,  0,  0,  0,  0, 10,  9,  0,  3,  0,  0,  0,  1,  7],
          [ 8,  0,  0,  0, 16,  0,  0,  1,  2, 14, 11,  4,  0,  0,  0,  3],
          [ 0,  0,  0,  1,  0,  0,  5,  0,  0, 16,  0,  6,  0, 12,  0,  0]]

giant3 = [[ 0,  4,  0,  0,  0,  0,  0, 12,  0,  1,  0,  0,  9,  0,  8,  0],
          [15, 14,  0,  0,  9,  0,  0, 13,  8,  0,  0, 10,  1,  0,  0,  0],
          [ 0,  7,  0,  0,  0,  0,  0,  8, 16,  0, 14,  0,  0,  2,  0,  0],
          [ 0,  0,  0,  9,  0,  0, 11,  0,  0,  0,  0,  0,  5,  0,  0, 15],
          [ 3,  0, 12,  0,  7,  0, 10,  0,  0, 11,  2,  0,  0,  0,  0,  6],
          [14,  8,  0,  0,  0, 12,  0,  6,  0,  0,  0, 16,  0,  0,  0, 10],
          [ 0, 16,  0,  0, 13,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0],
          [ 6,  0,  0,  0,  0,  8,  0,  5,  1,  7, 13,  0, 11,  0,  0, 14],
          [ 0,  0,  0,  2,  0,  0, 16,  0, 15, 12,  0,  3, 10,  7,  0,  0],
          [ 0,  9,  0,  5, 11,  0,  3,  0,  4, 13, 16,  0,  0, 15,  6,  0],
          [ 0,  0,  0,  0,  5,  4,  0,  0,  9,  6,  0,  2,  0,  0,  0,  0],
          [ 1,  0,  0,  0,  0, 15, 12,  0,  0,  0,  5,  0,  0,  0,  9,  0],
          [12, 10,  0, 15,  0,  1,  0,  0,  2,  9,  3,  4,  0,  0,  5,  0],
          [ 0,  0,  0,  3, 10,  0,  4,  0,  0, 15,  0,  0,  0,  0,  0,  0],
          [ 0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10, 11],
          [11,  6,  8,  0,  0,  0, 15,  0, 14,  0,  0,  0,  0, 13,  0,  2]]

sudokus = [[], [], [small, small2], [big, big2, big3, big4], [giant, giant2, giant3]]

########### Module functions ###########################

def print_board(board):
    """
    Prints a given board to the console in a way that aligns the content of columns and makes
    the subgrids visible.

    Input : a Sudoku board (board) of size 4x4, 9x9, or 16x16
    Effect: prints the board to the console 

    For example:

    >>> print_board(small2)
    -------
    |  |1 |
    |4 |  |
    -------
    |  | 2|
    | 3|  |
    -------
    >>> print_board(big)
    -------------
    |   |   |   |
    |4  |789|   |
    |78 |   | 56|
    -------------
    | 2 |36 |8  |
    |  5|  7| 1 |
    |8  |2  |  5|
    -------------
    |  1|64 |97 |
    |   |9  |   |
    |   | 3 |  2|
    -------------
    >>> print_board(giant2)
    ---------------------
    | 5  | 4 8| 6  |  9G|
    |1   |   D|4  7|F 8 |
    |D   | 73 |   9|5A  |
    | BCF|A   |  5 |34 D|
    ---------------------
    |F 13|  72|    | 5  |
    |   C| 3 5| B E|   9|
    |47  |    |C FG|    |
    |    |E F |69  |  C |
    ---------------------
    |3 F4| DE |   1|  78|
    |    |    |  9A|    |
    |B GA|    | 7  | 35 |
    |  D |    |E GF| 9 1|
    ---------------------
    |9 2 | E 4|8   |    |
    | E  |   A|9 3 |  17|
    |8   |G  1|2EB4|   3|
    |   1|  5 | G 6| C  |
    ---------------------
    """
    lst = []
    for i in board:
        out = []
        for j in range(len(board)):
            if len(board) == 4:
                if j%2 == 0:
                    out.append('-'*7)
            elif len(board) == 9:
                if j%3 == 0:
                    out.append('-'*13) 
            elif len(board) == 16:
                if j%4 == 0:
                    out.append('-'*21)
            if len(out) != 0:
                lst.append(out)
                out = []
            for k in range(len(i)):
                if len(board) == 4:
                    if k%2 == 0:
                       out.append('|') 
                elif len(board) == 9:
                    if k%3 == 0:
                       out.append('|')
                elif len(board) == 16:
                    if k%4 == 0:
                       out.append('|') 
                if board[j][k] == 10:
                    out.append('A')
                elif board[j][k] == 11:
                    out.append('B')
                elif board[j][k] == 12:
                    out.append('C')
                elif board[j][k] == 13:
                    out.append('D')
                elif board[j][k] == 14:
                    out.append('E')
                elif board[j][k] == 15:
                    out.append('F')
                elif board[j][k] == 16:
                    out.append('G')
                elif board[j][k] == 0:
                    out.append(' ')
                else :
                    out.append(str(board[j][k]))
            out.append('|')
            lst.append(out)
            out = []
        if len(board) == 4:
            out.append('-'*7)
        elif len(board) == 9:
            out.append('-'*13) 
        elif len(board) == 16:
            out.append('-'*21) 
        lst.append(out)
        for i in range(len(lst)):
            lst[i] = ''.join(lst[i])
        return print('\n'.join(lst))
    
def subgrid_values(board, r, c):
    """
    Input : Sudoku board (board), row index (r), and column index (c)
    Output: list of all numbers that are present in the subgrid of the board related to the
            field (r, c)

    For example:

    >>> subgrid_values(small2, 1, 3)
    [1]
    >>> subgrid_values(big, 4, 5)
    [3, 6, 7, 2]
    >>> subgrid_values(giant2, 4, 5)
    [7, 2, 3, 5, 14, 15]
    """
    """
    Check the numbers that exist in the specified location related to the field (r,c).
    And output them.
    """
    res = []
    end = []
    if len(board) == 4:
        if r in range(0,2):
            for r in range(0,2):
                if c in range (0,2):
                    for c in range(0,2):
                        res += [board[r][c]]
                if c in range (2,4):
                    for c in range(2,4):
                        res += [board[r][c]]
        if r in range(2,4):
            for r in range(2,4):
                if c in range (0,2):
                    for c in range(0,2):
                        res += [board[r][c]]
                if c in range (2,4):
                    for c in range(2,4):
                        res += [board[r][c]]
    if len(board) == 9:
        if r in range(0,3):
            for r in range(0,3):
                if c in range (0,3):
                    for c in range(0,3):
                        res += [board[r][c]]
                if c in range (3,6):
                    for c in range(3,6):
                        res += [board[r][c]]
                if c in range (6,9):
                    for c in range(6,9):
                        res += [board[r][c]]
        if r in range(3,6):
            for r in range(3,6):
                if c in range (0,3):
                    for c in range(0,3):
                        res += [board[r][c]]
                if c in range (3,6):
                    for c in range(3,6):
                        res += [board[r][c]]
                if c in range (6,9):
                    for c in range(6,9):
                        res += [board[r][c]]
        if r in range(6,9):
            for r in range(6,9):
                if c in range (0,3):
                    for c in range(0,3):
                        res += [board[r][c]]
                if c in range (3,6):
                    for c in range(3,6):
                        res += [board[r][c]]
                if c in range (6,9):
                    for c in range(6,9):
                        res += [board[r][c]]
    if len(board) == 16:
        if r in range(0,4):
            for r in range(0,4):
                if c in range (0,4):
                    for c in range(0,4):
                        res += [board[r][c]]
                if c in range (4,8):
                    for c in range(4,8):
                        res += [board[r][c]]
                if c in range (8,12):
                    for c in range(8,12):
                        res += [board[r][c]]
                if c in range (12,16):
                    for c in range(12,16):
                        res += [board[r][c]]
        if r in range(4,8):
            for r in range(4,8):
                if c in range (0,4):
                    for c in range(0,4):
                        res += [board[r][c]]
                if c in range (4,8):
                    for c in range(4,8):
                        res += [board[r][c]]
                if c in range (8,12):
                    for c in range(8,12):
                        res += [board[r][c]]
                if c in range (12,16):
                    for c in range(12,16):
                        res += [board[r][c]]
        if r in range(8,12):
            for r in range(8,12):
                if c in range (0,4):
                    for c in range(0,4):
                        res += [board[r][c]]
                if c in range (4,8):
                    for c in range(4,8):
                        res += [board[r][c]]
                if c in range (8,12):
                    for c in range(8,12):
                        res += [board[r][c]]
                if c in range (12,16):
                    for c in range(12,16):
                        res += [board[r][c]]
        if r in range(12,16):
            for r in range(12,16):
                if c in range (0,4):
                    for c in range(0,4):
                        res += [board[r][c]]
                if c in range (4,8):
                    for c in range(4,8):
                        res += [board[r][c]]
                if c in range (8,12):
                    for c in range(8,12):
                        res += [board[r][c]]
                if c in range (12,16):
                    for c in range(12,16):
                        res += [board[r][c]]
        
    for x in res:
        if x != 0:
            end += [x]
    return end
def options(board, i, j):
    """
    Input : Sudoku board (board), row index (r), and column index (c)
    Output: list of all numbers that player is allowed to place on field (r, c),
            i.e., those that are not already present in row r, column c,
            and subgrid related to field (r, c)

    For example:

    >>> options(small2, 0, 0)
    [2, 3]
    >>> options(big, 6, 8)
    [3, 8]
    >>> options(giant2, 1, 5)
    [2, 5, 6, 9, 11, 12, 16]
    """
    """
    for the options function, the program runs to filter the numbers that is not fulfil the sudoku rules and output the eligible ones.
    It cancels the numbers that exist in specified columns, rows and subgrid and shows the numbers that haven't present. 
    """
    x = list(range(1,len(board)+1))
    res = list(range(1,len(board)+1))
    for y in x:
        for q in range(len(board)):
            if board[q][j] in res and board[q][j]== y:
                res.remove(board[q][j])
            if board[i][q] in res and board[i][q] == y:
                res.remove(board[i][q])
    for y in x:
        if len(board) == 4:
            if i in range(0,2):
                for i in range(0,2):
                    if j in range(0,2):
                        for j in range(0,2):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(2,4):
                        for j in range(2,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(2,4):
                for i in range(2,4):
                    if j in range(0,2):
                        for j in range(0,2):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(2,4):
                        for j in range(2,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
        if len(board) == 9:
            if i in range(0,3):
                for i in range(0,3):
                    if j in range(0,3):
                        for j in range(0,3):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (3,6):
                        for j in range(3,6):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (6,9):
                        for j in range(6,9):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(3,6):
                for i in range(3,6):
                    if j in range(0,3):
                        for j in range(0,3):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (3,6):
                        for j in range(3,6):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (6,9):
                        for j in range(6,9):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(6,9):
                for i in range(6,9):
                    if j in range(0,3):
                        for j in range(0,3):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (3,6):
                        for j in range(3,6):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range (6,9):
                        for j in range(6,9):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
        if len(board) == 16:
            if i in range(0,4):
                for i in range(0,4):
                    if j in range(0,4):
                        for j in range(0,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(4,8):
                        for j in range(4,8):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(8,12):
                        for j in range(8,12):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(12,16):
                        for j in range(12,16):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(4,8):
                for j in range(4,8):
                    if j in range(0,4):
                        for j in range(0,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(4,8):
                        for j in range(4,8):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(8,12):
                        for j in range(8,12):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(12,16):
                        for j in range(12,16):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(8,12):
                for i in range(8,12):
                    if j in range(0,4):
                        for j in range(0,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(4,8):
                        for j in range(4,8):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(8,12):
                        for j in range(8,12):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(12,16):
                        for j in range(12,16):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
            if i in range(12,16):
                for j in range(12,16):
                    if j in range(0,4):
                        for j in range(0,4):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(4,8):
                        for j in range(4,8):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(8,12):
                        for j in range(8,12):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])
                    if j in range(12,16):
                        for j in range(12,16):
                            if board[i][j] in res and board[i][j] == y:
                                res.remove(board[i][j])         
    return res

######functions for backtracking ######################

"""
 Base case: to determine the board is solved is to check is there any left blank (0) in the board.
 If there is blank (0), then give us the position which is blank.
 If there is no blank(0), then the board is solved.
"""
def emp(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return i,j
    return None 

"""
Backtracking : 
Base case : Use the emp function (empty) to determine is the board solved.
If the board is solved, then return True
If the board is not solved, then use the position which provided by the emp function,
try the options which generated by the options function.
Firstly use the first option, then goes to the next position,
If the next position's option shows None,
then goes to the previous position then try the second option and runs again 
By using this method to loop through the entire board until is solved.
"""
def backtracking(board):
    if not emp(board):
        return True
    else:
        i,j = emp(board)
    for o in options(board,i,j):
        board[i][j] = o

        if backtracking(board) == True:
            return True
        board[i][j] = 0
    return False

"""
To reduce the cost of backtracking,
I firstly use the inferred function to get the answer of all the positions,
nextly only use the backtracking function to get the answers of the position which cannot solved by the inferred function.
then print the solved board.

By using the inferred function, it could reduce the times of backtracking.
For example, originally, there are 11 empty positions in the board,
After inferred function, the empty columns may be decreased
Then goes the bactracking function, if the empty columns decrease to 9
9 empty columns is more easier to solve than 11 empty columnns for the backtracking function.
In conclusion, the inferred function is useful to reduce the computational complexity of the backtracking.
"""
def sln(board):
    import copy
    x = copy.deepcopy(board)
    inferred(x)
    backtracking(x)
    print_board(x)

##############################################################

def play(board):
    """
    Input : Sudoku board
    Effect: Allows user to play board via console
    """
    print_board(board)
    mark = 0
    accu = 0
    while True:
        inp = input().split(' ')
        if len(inp) == 3 and inp[0].isdecimal() and inp[1].isdecimal() and inp[2].isdecimal():
            i = int(inp[0])
            j = int(inp[1])
            x = int(inp[2])
            board[i][j] = x
            print_board(board)
            for l in board:
                for r in range(len(board)):
                    for c in range(len(l)):
                        if board[r][c] != 0:
                            accu += 1
                            if accu == len(board)**2:
                                print('success')
                                mark += 1
                                break
        elif len(inp)==3 and (inp[0] == 'n' or inp[0] == 'new') and inp[1].isdecimal() and inp[2].isdecimal():
            k = int(inp[1])
            d = int(inp[2])
            if k < len(sudokus) and 0 < d <= len(sudokus[k]):
                board = sudokus[k][d-1]
                print_board(board)
            else:
                print('board not found')
        elif inp[0] == 'q' or inp[0] == 'quit':
            return

        #if input 'i' or 'infer',then change the current board state into inffered board state
        elif inp[0] == 'i' or inp[0] == 'infer':
            print_board(inferred(board))
            
        #If input 's' or 'solve' then show the answer of the sudoku board by using the sln function.
        elif inp[0] == 's'  or inp[0] == 'solve':
            return sln(board)
            
        else:
            print('Invalid input')


########### Functions only relevant for Part II ########

def value_by_single(board, i, j):
    """
    Input : board, row, and column index
    Output: The correct value for field (i, j) in board if it can be inferred as
            either a forward or a backward single; or None otherwise. 
    
    For example:

    >>> value_by_single(small2, 0, 1)
    2
    >>> value_by_single(small2, 0, 0)
    3
    >>> value_by_single(big, 0, 0)
    """
    lst = options(board,i,j)
    l = list(range(len(board)))
    l.remove(i)
    w = list(range(len(board)))
    w.remove(j)

    n = len(board)
    k = round(sqrt(n))
    m = list(range((i // k) * k, ((i // k) + 1) * k))
    m.remove(i)
    n = list(range((j // k) * k, ((j // k) + 1) * k))
    n.remove(j)

    #Forward single : If there is only 1 option for that position, then the number in option is the answer for that position.
    if len(options(board,i,j))==1: 
        return lst[0]
    
    # Backward single: If the options are more than 1, 
    # Then check all options in the related subgrid which is 0
    # If there is duplicated options appear, then remove it from the options list.

    else:
        for r in m:
            for c in n:
                if board[i][j] == 0:
                    for z in options(board,r,c):
                        if z in lst:
                            lst.remove(z)
                            
    
    # If there is 1 options left. That will be the answer for that position.

    if len(lst)==1:
        return lst[0]
                        
    # If there is still other options, then check the options of empty position of the related column and row. 
    # Next, remove the duplicated options.
    # If there is left 1 options, that will be the answer for that position.

    else:
        for p in l:
            if board[p][j] == 0:
                for x in options(board,p,j):
                    if x in lst:
                        lst.remove(x)

        for q in w:
            if board[i][q] == 0:
                for y in options(board,i,q):
                    if y in lst:
                        lst.remove(y)

    #If the options is still more than 1, then there is no answer fot that position. 

    if len(lst) == 0 :
        return None
                    
def inferred(board):
    import copy

    #copy the board
    cb = copy.deepcopy(board)
    
    #Loop thorough the entire board,
    #Search the position which is zero 
    #Then, use the value_bysingle function to get the answer for that positio
    for x in range(len(board)):
        for i in range(len(board)):
            for j in range(len(board)):
                if cb[i][j] == 0:
                    if value_by_single(cb,i,j) != None:
                        cb[i][j] = value_by_single(cb,i,j)
    return cb
    """
    Input : Sudoku board
    Output: new Soduko board with all values field from input board plus
            all values that can be inferred by repeated application of 
            forward and backward single rule

    For example board big can be completely inferred:

    >>> inferred(big) # doctest: +NORMALIZE_WHITESPACE

    [[2, 1, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [1, 2, 4, 3, 6, 5, 8, 9, 7],
    [3, 6, 5, 8, 9, 7, 2, 1, 4],
    [8, 9, 7, 2, 1, 4, 3, 6, 5],
    [5, 3, 1, 6, 4, 2, 9, 7, 8],
    [6, 4, 2, 9, 7, 8, 5, 3, 1],
    [9, 7, 8, 5, 3, 1, 6, 4, 2]]

    But function doesn't modify input board:

    >>> big # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [4, 0, 0, 7, 8, 9, 0, 0, 0],
     [7, 8, 0, 0, 0, 0, 0, 5, 6],
     [0, 2, 0, 3, 6, 0, 8, 0, 0],
     [0, 0, 5, 0, 0, 7, 0, 1, 0],
     [8, 0, 0, 2, 0, 0, 0, 0, 5], 
     [0, 0, 1, 6, 4, 0, 9, 7, 0],
     [0, 0, 0, 9, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 3, 0, 0, 0, 2]]

    In board big4 there is nothing to infer:
    
    >>> inferred(big4) # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0, 6, 0, 0, 2, 0, 0],
     [8, 0, 4, 0, 3, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 9, 0, 0, 0], 
     [4, 0, 5, 0, 0, 0, 0, 0, 7],
     [7, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 0, 5, 0, 0, 0, 8],
     [3, 0, 0, 0, 7, 0, 0, 0, 4],
     [0, 0, 0, 0, 0, 1, 9, 0, 0],
     [0, 0, 0, 2, 0, 0, 0, 6, 0]]
    """    
########### Driver code (executed when running module) #

import doctest
doctest.testmod()

# play(big2)

small2 = [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]]
sln(small2)

