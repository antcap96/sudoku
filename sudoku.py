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

def GetSquare(line,coll):
    """
    The square of the node in (line,coll)
    Keyword Arguments:
    line -- trivial
    coll -- trivial
    """
    return line//3*3+coll//3

class Sudoku:
    """basic structure of sudoku"""
    def __init__(self):
        """
        Create an empty Sudoku
        """
        # places        -- Basically it's the sudoku
        # poss[i][j][k] -- if number k+1 can be inserted in line i, collum j
        # lines[i][k]   -- how many possible positions for number k+1 in line i
        # collums[i][k] -- how many possible positions for number k+1 in collum i
        # squares[i][k] -- how many possible positions for number k+1 in square i
        # nodes[i][j]   -- how many possible numbers for node in line i and collum j

        self.places = [[None for j in range(9)] for i in range(9)]
        self.poss = [[[True for k in range(9)] for j in range(9)] for i in range(9)]
        self.lines   = [[9 for j in range(9)] for i in range(9)]
        self.collums = [[9 for j in range(9)] for i in range(9)]
        self.squares = [[9 for j in range(9)] for i in range(9)]
        self.nodes   = [[9 for j in range(9)] for i in range(9)]
        
        # self.linesRem = [9 for k in range(9)]

    def __str__(self):
        s = ""
        for i,line in enumerate(self.places):
            if i%3 == 0:
                s += "+-------+-------+-------+\n"
            for j,p in enumerate(line):
                if j%3 == 0:
                    s += "| "
                s += (str(p) if p != None else " ")  + " "
            s += "|\n"
        s += "+-------+-------+-------+\n"        
        return s

    def __repr__(self):
        return str(self.places)
    
    def DisplayPossibilities(self, toshow):
        s = ""
        for k in toshow:
            s += str(k+1) + "\n"

            for i in range(9):
                s += ("  " if i%3==0 else "") + str(self.collums[i][k]) + " "
            s += "\n"
            for i,line in enumerate(self.poss):
                if i%3 == 0:
                    s += "+-------+-------+-------+\n"
                for j,p in enumerate(line):
                    if j%3 == 0:
                        s += "| "
                    s += ("*"  if p[k]  else " ")  + " "
                s += "| " + str(self.lines[i][k]) + " " + str(self.squares[i][k]) + "\n"
            s += "+-------+-------+-------+\n"
        print(s)

    def ClearCollum(self, coll, number):
        for i in range(9):
            if self.poss[i][coll][number-1]:
                self.Clear(i,coll,number)

    def ClearLine(self, line, number):
        for i in range(9):
            if self.poss[line][i][number-1]:
                self.Clear(line,i,number)

    def ClearSquare(self, square, number):
        for i in range(9):
            if self.poss[square//3*3+i//3][square%3*3+i%3][number-1]:
                self.Clear(square//3*3+i//3,square%3*3+i%3,number)

    def ClearNode(self, line, coll):
        for i in range(9):
            if self.poss[line][coll][i]:
                self.Clear(line,coll,i)
                
        
    def Clear(self, line, coll, number):
        if self.poss[line][coll][number-1]:
            self.lines[line][number-1]   -= 1
            self.collums[coll][number-1] -= 1
            self.squares[GetSquare(line,coll)][number-1] -=1
            self.nodes[line][coll] -= 1
            self.poss[line][coll][number-1] = False

    
    def add(self,line,coll,number):
        """
        Append number to the sudoku
        Keyword Arguments:
        line   -- line of number to insert
        coll   -- collum of number to insert
        number -- number that will be inserted
        Note: colums start on 0 and go up to 8
        """
        # check if action is possible
        if self.poss[line][coll][number-1]:
            # define number
            self.places[line][coll] = number
            # clear Collum, Line, Square and Node
            self.ClearCollum(coll,number)
            self.ClearLine(line,number)
            self.ClearSquare(GetSquare(line,coll),number)
            self.ClearNode(line,coll)
        else:
            print("fuckfuckfuck")

x = Sudoku()
print()
print(x)
for i in range(9):
    for j in range(9):
        x.add(i,j,(i*3+j+i//3)%9)
print(x)

a = Sudoku()
a.add(0,2,1)
a.add(2,3,1)
a.add(3,6,1)
a.add(7,7,1)
