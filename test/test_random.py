from sudoku import Sudoku
import random as ra

def RandomSudoku(n):
    test2 = Sudoku()
    
    for i in range(n):
        try:
            test2.Add(ra.randint(0,8), ra.randint(0,8), ra.randint(1,9))
        except InsertionError:
            pass
    return test2
