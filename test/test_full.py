from sudoku import Sudoku
x = Sudoku()

for i in range(9):
    for j in range(9):
        x.Add(i,j,(i*3+j+i//3)%9+1)
print()

