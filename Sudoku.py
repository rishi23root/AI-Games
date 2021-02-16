from random import sample

class sudoku:
    '''This class is resposible for creating and solving the grid '''
    def __init__(self):
        # sudoku_genrator for question and solve fot the solutions by recurtion
        self.side = 9 
        self.side_small = int(self.side/3)
        # self.grid = self.sudoku_genrator(elements=80) # all the funtions sre using the grid to return 
        self.grid = self.sudoku_genrator() # all the funtions sre using the grid to return 
        self.question = [a[:] for a in self.grid[:]]

    @staticmethod
    def sudoku_genrator(elements=30,side = 9):
        # elements = 30 will be quite easy

        # errors
        if side%3 != 0 or not side: raise Exception(f"'side' should be multiple of 3 and cannot be zero.")
        if elements > side ** 2 : raise ValueError(f"Elements can not more then total elements in grid here we have {side**2} update 'side' for bigger grid.")

        base= int(side ** 0.5)
        # randomize rows, columns and numbers (of valid base pattern)
        shuffle = lambda s : sample(s,len(s)) 
        rBase = range(base) 
        rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
        cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
        nums  = shuffle(range(1,base*base+1))

        # pattern for a baseline valid solution
        pattern = lambda r,c : (base*(r%base)+r//base+c)%side
        # produce board using randomized baseline pattern
        board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
        
        # you must leave at least 17 numbers for a 9x9 sudoku for unique solution
        # remove 60 from the self.grid just a random nums 
        for p in sample(range(side**2),81 - elements) : 
            # print(p,p//side,p%side)
            board[p//side][p%side] = 0
        return board

    def possible(self,row,col,num):
        # row != rows and  col != cols because we dont want to compare element from it self 
        # row
        for cols in range(self.side): # to range in the row length
            if self.grid[row][cols] == num and col != cols :
                return False

        # reading each cell 
        for rows in self.grid: 
            if rows[col] == num and row != rows:
                return False
        
        # for the box 
        row_range = row//self.side_small * self.side_small
        col_range = col//self.side_small * self.side_small
        for row in range(row_range,row_range+self.side_small):
            for col in range(col_range,col_range+self.side_small):
                if self.grid[row][col] == num :
                    return False

        return True

    def find_empty(self):
        for row in range(self.side):
            for cell in range(self.side):
            # get the each cell
                if self.grid[row][cell] == 0 :
                    return (True,row,cell)
        else :
            return (False,-1,-1)

    def update_cell(self,row,col,val):
        '''Take index of the row and col and value to update useful in inheretance'''
        self.grid[row][col] = val

    def solve(self):
        is_empty,row,col = self.find_empty()
        if not is_empty : return True # task completd
        for n in range(1,self.side + 1):
            # check all the possible value for that perticular possition
            if self.possible(row,col,n):
                # self.grid[row][col] = n
                self.update_cell(row,col,n)
                if self.solve() : return True
                # this mean having error due to this value so make it 0 again and try with another value
                # self.grid[row][col] = 0
                self.update_cell(row,col,0)
        return False

# example:-
# for creting grid with existing 60 elements 
# grid = sudoku.sudoku_genrator(elements = 60)
if __name__ == "__main__":
    s = sudoku()
    s.solve()
    # showing the solution
    print("\tQuestion  \t\t\t  Solution")
    [print(a ,"\t", b) for a,b in zip(s.question,s.grid)]

