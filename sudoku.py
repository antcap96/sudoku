import numpy as nu

# The squares are the big ones and the nodes the small ones btw
#   0 1 2   3 4 5   6 7 8
# +-------+-------+-------+
# |       |       |       | 0
# |   0   |   1   |   2   | 1
# |       |       |       | 2
# +-------+-------+-------+
# |       |       |       | 3
# |   3   |   4   |   5   | 4
# |       |       |       | 5
# +-------+-------+-------+
# |       |       |       | 6
# |   6   |   7   |   8   | 7
# |       |       |       | 8
# +-------+-------+-------+

# square formula: l//3*3+c//3
# inverse :       s//3 s%3
# iterate over square:    l//3*3+i//3 c//3*3+i%3
# or if given the square: s//3*3+i//3 s%3*3+i%3

def GetSquare(row,col):
    """
    The square of the node in (row,col)
    Keyword Arguments:
    row -- trivial
    col -- trivial
    """
    return row//3*3+col//3

class Sudoku:
    """basic structure of sudoku"""
    def __init__(self):
        """
        Create an empty Sudoku
        """
        # places        -- Basically it's the sudoku
        # poss[i][j][k] -- if number k+1 can be inserted in row i, column j
        # rows[i][k]    -- how many possible positions for number k+1 in row i
        # columns[i][k] -- how many possible positions for number k+1 in column i
        # squares[i][k] -- how many possible positions for number k+1 in square i
        # nodes[i][j]   -- how many possible numbers for node in row i and column j
        # missing       -- nodes missing for completion

        self.places = [[None for j in range(9)] for i in range(9)]
        self.poss = [[[True for k in range(9)] for j in range(9)] for i in range(9)]
        self.rows   = [[9 for j in range(9)] for i in range(9)]
        self.columns = [[9 for j in range(9)] for i in range(9)]
        self.squares = [[9 for j in range(9)] for i in range(9)]
        self.nodes   = [[9 for j in range(9)] for i in range(9)]
        self.missing = 81
        # self.rowsRem = [9 for k in range(9)]

    def __str__(self):
        s = ""
        for i,row in enumerate(self.places):
            if i%3 == 0:
                s += "+-------+-------+-------+\n"
            for j,p in enumerate(row):
                if j%3 == 0:
                    s += "| "
                s += (str(p) if p != None else " ")  + " "
            s += "|\n"
        s += "+-------+-------+-------+\n"        
        return s

    def __repr__(self):
        return str(self.places)
    
    def DisplayPossibilities(self, toshow=range(10)):
        """
        Display possible positions for numbers 
        Keyword Arguments:
        toshow -- list of numbers to show info on (ex [1,3,5] will show info for those numbers)
                  a number out of that range (ex 0) will show possibilities for each node
        first row: number of possible places for each column
        second to last column: number of possible places for each row
        last column: number os possible places for each square
        """
        toshow = [x-1 for x in toshow]
        s = ""
        for k in toshow:
            if k >= 0:
                s += str(k+1) + "\n"
                for i in range(9):
                    s += ("  " if i%3==0 else "") + str(self.columns[i][k]) + " "
                s += "\n"
                for i,row in enumerate(self.poss):
                    if i%3 == 0:
                        s += "+-------+-------+-------+\n"
                    for j,p in enumerate(row):
                        if j%3 == 0:
                            s += "| "
                        s += ("*"  if p[k]  else " ")  + " "
                    s += "| " + str(self.rows[i][k]) + "   " + str(self.squares[i][k]) + "\n"
                s += "+-------+-------+-------+\n"
            else:
                for i,row in enumerate(self.nodes):
                    if i%3 == 0:
                        s += "+-------+-------+-------+\n"
                    for j,p in enumerate(row):
                        if j%3 == 0:
                            s += "| "
                        s += (str(p) if p >= 0 else " ")  + " "
                    s += "|\n"
                s += "+-------+-------+-------+\n"                 
        print(s)

    def ClearColumn(self, col, number):
        for i in range(9):
            if self.poss[i][col][number-1]:
                self.Clear(i,col,number)

    def ClearRow(self, row, number):
        for i in range(9):
            if self.poss[row][i][number-1]:
                self.Clear(row,i,number)

    def ClearSquare(self, square, number):
        for i in range(9):
            if self.poss[square//3*3+i//3][square%3*3+i%3][number-1]:
                self.Clear(square//3*3+i//3,square%3*3+i%3,number)

    def ClearNode(self, row, col):
        for i in range(9):
            if self.poss[row][col][i]:
                self.Clear(row,col,i+1)
                
        
    def Clear(self, row, col, number):
        if self.poss[row][col][number-1]:
            self.rows[row][number-1] -= 1
            self.columns[col][number-1] -= 1
            self.squares[GetSquare(row,col)][number-1] -=1
            self.nodes[row][col] -= 1
            self.poss[row][col][number-1] = False

    
    def Add(self,row,col,number):
        """
        Append number to the sudoku
        Keyword Arguments:
        row    -- row of number to insert
        col    -- column of number to insert
        number -- number that will be inserted
        Note: colums start on 0 and go up to 8
        """
        
        # check if action is possible
        if self.poss[row][col][number-1]:
            # clear Column, Row, Square and Node
            self.ClearColumn(col,number)
            self.ClearRow(row,number)
            self.ClearSquare(GetSquare(row,col),number)
            self.ClearNode(row,col)
            self.missing -= 1
            # define number
            self.places[row][col] = number
        else:
            print("fuckfuckfuck")

    def SolveRun(self):
        """
        Iterates over the Sudoku attempting to solve it

        Return:
        Successful additions to Sudoku
        """
        added = 0
        # Solve for rows
        for i in range(9):
            for k in range(9):
                if self.rows[i][k] == 1:
                    pos = [self.poss[i][x][k] for x in range(9)].index(True)
                    self.Add(i,pos,k+1)
                    added +=1
        # Solve for columns
        for i in range(9):
            for k in range(9):
                if self.columns[i][k] == 1:
                    pos = [self.poss[x][i][k] for x in range(9)].index(True)
                    self.Add(pos,i,k+1)
                    added +=1
        # Solve for squares
        for i in range(9):
            for k in range(9):
                if self.squares[i][k] == 1:
                    pos = [self.poss[i//3*3+x//3][i%3*3+x%3][k] for x in range(9)].index(True)
                    self.Add(i//3*3+pos//3,i%3*3+pos%3,k+1)
                    added +=1
        # Solve for nodes
        for i in range(9):
            for j in range(9):
                if self.nodes[i][j] == 1:
                    pos = self.poss[i][j].index(True)
                    self.Add(i,j,pos+1)
                    added +=1
        return added
                             
    def SoftSolve(self):
        """
        Attempts to solve sudoku without guessing
        
        Return:
        Whether is successful or not
        """
        while self.SolveRun() > 0:
            pass
        return self.missing == 0
        
    
x = Sudoku()
print("______________________________________________________________________")
# print(x)
for i in range(9):
    for j in range(9):
        x.Add(i,j,(i*3+j+i//3)%9+1)
# print(x)

a = Sudoku()
a.Add(0,2,1)
a.Add(2,3,1)
a.Add(3,6,1)
a.Add(7,7,1)

test1 = Sudoku()
test1.Add(0,0,5)
test1.Add(0,1,3)
test1.Add(0,4,7)
test1.Add(1,0,6)
test1.Add(1,3,1)
test1.Add(1,4,9)
test1.Add(1,5,5)
test1.Add(2,1,9)
test1.Add(2,2,8)
test1.Add(2,7,6)

test1.Add(3,0,8)
test1.Add(3,4,6)
test1.Add(3,8,3)
test1.Add(4,0,4)
test1.Add(4,3,8)
test1.Add(4,5,3)
test1.Add(4,8,1)
test1.Add(5,0,7)
test1.Add(5,4,2)
test1.Add(5,8,6)

test1.Add(6,1,6)
test1.Add(6,6,2)
test1.Add(6,7,8)
test1.Add(7,3,4)
test1.Add(7,4,1)
test1.Add(7,5,9)
test1.Add(7,8,5)
test1.Add(8,4,8)
test1.Add(8,7,7)
test1.Add(8,8,9)

print(test1)
