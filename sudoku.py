import numpy as nu
import copy as cp

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

class InsertionError(Exception):
    def __init__(self, sudoku, row, col, number):
        """
        Exception for a failure to insert number at (row,col) in sudoku
        """
        self.row = row
        self.col = col
        self.number = number
        self.sudoku = sudoku
    def __str__(self):
        return ("Failed to insert " + str(self.number) +" at (" + str(self.row) + "," + str(self.col) + ")\nThe sudoku:\n" + str(self.sudoku))

class SudokuError(Exception):
    def __init__(self, sudoku):
        """
        Execption for and unsolvable sudoku 
        """
        self.sudoku = sudoku
    def __str__(self):
        return ("Impossible sudoku:\n" + str(self.sudoku))
        
    
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
        self.rows    = [[9 for j in range(9)] for i in range(9)]
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
                    s += ("  " if i%3==0 else "") + \
                         (str(self.columns[i][k]) if self.columns[i][k] >= 0 else "x") + " "
                s += "\n"
                for i,row in enumerate(self.poss):
                    if i%3 == 0:
                        s += "+-------+-------+-------+\n"
                    for j,p in enumerate(row):
                        if j%3 == 0:
                            s += "| "
                        s += ("*"  if p[k]  else " ")  + " "
                    s += "| " + (str(self.rows[i][k]   ) if self.rows[i][k] >=0     else "x") + \
                        "   " + (str(self.squares[i][k]) if self.squares[i][k] >= 0 else "x") + "\n"
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

    def Solved(self):
        """
        return whether or not the sudoku is solved
        """
        return self.missing == 0
    def ClearColumn(self, col, number):
        for i in range(9):
            if self.poss[i][col][number-1]:
                self.Clear(i,col,number)
        if self.columns[col][number-1] == 0:
            self.columns[col][number-1] = -1
        else:
            raise BaseException("Column " + str(col) +" "+ str(number)) 

    def ClearRow(self, row, number):
        for i in range(9):
            if self.poss[row][i][number-1]:
                self.Clear(row,i,number)
        if self.rows[row][number-1] == 0:
            self.rows[row][number-1] = -1
        else:
            raise BaseException("Row " + str(row) +" "+ str(number)) 

    def ClearSquare(self, square, number):
        for i in range(9):
            if self.poss[square//3*3+i//3][square%3*3+i%3][number-1]:
                self.Clear(square//3*3+i//3,square%3*3+i%3,number)
        if self.squares[square][number-1] == 0:
            self.squares[square][number-1] = -1
        else:
            raise BaseException("Square " + str(square) +" "+ str(number)) 

    def ClearNode(self, row, col):
        for i in range(9):
            if self.poss[row][col][i]:
                self.Clear(row,col,i+1)
        if self.nodes[row][col] == 0:
            self.nodes[row][col] = -1
        else:
            raise BaseException("Node " + str(row) +" "+ str(number)) 
        
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
            raise InsertionError(self,row,col,number)

    def SolveRun(self):
        """
        Iterates over the Sudoku attempting to solve it

        Return:
        Successful additions to Sudoku
        returns -1 if detects that sudoku does not have solution
        """
        added = 0
        # Solve for rows
        for i in range(9):
            for k in range(9):
                if self.rows[i][k] == 0:
                    return -1
                if self.rows[i][k] == 1:
                    pos = [self.poss[i][x][k] for x in range(9)].index(True)
                    self.Add(i,pos,k+1)
                    added +=1
        # Solve for columns
        for i in range(9):
            for k in range(9):
                if self.columns[i][k] == 0:
                    return -1
                if self.columns[i][k] == 1:
                    pos = [self.poss[x][i][k] for x in range(9)].index(True)
                    self.Add(pos,i,k+1)
                    added +=1
        # Solve for squares
        for i in range(9):
            for k in range(9):
                if self.squares[i][k] == 0:
                    return -1
                if self.squares[i][k] == 1:
                    pos = [self.poss[i//3*3+x//3][i%3*3+x%3][k] for x in range(9)].index(True)
                    self.Add(i//3*3+pos//3,i%3*3+pos%3,k+1)
                    added +=1
        # Solve for nodes
        for i in range(9):
            for j in range(9):
                if self.nodes[i][j] == 0:
                    return -1
                if self.nodes[i][j] == 1:
                    pos = self.poss[i][j].index(True)
                    self.Add(i,j,pos+1)
                    added +=1
        return added

    def CheckFailure(self):
        """
        Returns if sudoku is sure to have no solution
        """
        for i in range(9):
            for j in range(9):
                if self.rows[i][j] == 0:
                    return True
                if self.columns[i][j] == 0:
                    return True
                if self.squares[i][j] == 0:
                    return True
                if self.nodes[i][j] == 0:
                    return True
        return False
        
    
    def SoftSolve(self):
        """
        Attempts to solve sudoku without guessing
        
        Return:
        If the sudoku is possible to have a solution
        Note: A solved sudoku *might* have a solution
        """
        while True:
            sol = self.SolveRun()
            if sol > 0:
                continue
            elif sol == 0:
                return True
            else:
                return False

    def Solve(self):
        """
        Solve Sudoku
        """
        sol = self.HardSolve()
        if sol == None:
            raise SudokuError(self)
        else:
            # sol is the solution of the sudoku, so it's copied to self
            self.places  = sol.places
            self.poss    = sol.poss
            self.rows    = sol.rows
            self.columns = sol.columns
            self.squares = sol.squares
            self.nodes   = sol.nodes
            self.missing = sol.missing
            
            
    def HardSolve(self):
        """
        Auxiliary function used by Solve (does the hard work but has weird output)
        
        Return:
        Solved sudoku (none if the sudoku does not have a solution)
        """

        # Do a SoftSolve. If False the sudoku is impossible, if True check if solved
        if self.SoftSolve() == False:
            return None
        if self.Solved():
            return self
        
        # Unable to determine solution of sudoku, begin guessing
        for row, col, number in self.Guess():
            sudoku_ = cp.deepcopy(self)
            sudoku_.Add(row,col,number)
            sol = sudoku_.HardSolve()
            if sol != None:
                return sol
        return None
                
        
    def Guess(self):
        """
        Look for the lowest diversion choice possible.
        In any reasonable sudoku this is any node/row/column/square with 2 possibilities

        Return:
        list of tuple of the form (row,column,number)
        """
        ans = []
        for n in range(2,9):
            # Search in rows
            for i in range(9):
                for k in range(9):
                    if self.rows[i][k] == n:
                        for x in range(9):
                            if self.poss[i][x][k]:
                                ans.append((i,x,k+1))
                        return ans

            # Search in columns
            for i in range(9):
                for k in range(9):
                    if self.columns[i][k] == n:
                        for x in range(9):
                            if self.poss[x][i][k]:
                                ans.append((x,i,k+1))
                        return ans
                        
            # Search in squares
            for i in range(9):
                for k in range(9):
                    if self.squares[i][k] == n:
                        for x in range(9):
                            if self.poss[i//3*3+x//3][i%3*3+x%3][k]:
                                ans.append((i//3*3+x//3,i%3*3+x%3,k+1))
                        return ans
                        
            # Search in nodes
            for i in range(9):
                for j in range(9):
                    if self.nodes[i][j] == n:
                        for x in range(9):
                            if self.poss[i][j][x]:
                                ans.append((i,j,x+1))
                        return ans
