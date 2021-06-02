# this contrain min max algo 
from tic_tac_toe_simple import tic_tac_toe

class min_max_ai(tic_tac_toe):
    """This is the cmd version for single player and Ai algo based moves"""
    def __init__(self):
        """initialize with inherits the tic_tac_toe class"""
        super().__init__()
        self.scores = {
            self.ai : 1 ,
            self.human : -1 ,
            "Tie" : 0 ,
            }
    
    def min_max(self,depth,ismaximizing):
        """ Algo to check all the winning possibilities and move best and fast win possition"""

        # first check if there is any winner here
        result =  self.who_wins()
        if result != None:
            return depth,self.scores[result]

        # check for the maximising player
        if ismaximizing:
            bestscore = float('-inf')
            for i in range(self.side):
                for j in range(self.side):
                    if self.grid[i][j] == '':
                        self.grid[i][j] = self.ai
                        return_depth , score = self.min_max(depth + 1,False)
                        self.grid[i][j] = ''
                        bestscore = max(score,bestscore)
            return return_depth,bestscore 
        # check for the minimising player
        else:
            bestscore = float('inf')
            for i in range(self.side):
                for j in range(self.side):
                    if self.grid[i][j] == '':
                        self.grid[i][j] = self.human
                        return_depth , score = self.min_max(depth + 1,True)  
                        self.grid[i][j] = ''
                        bestscore = min(score,bestscore)
            return return_depth , bestscore

    def best_move(self,player):
        """call min_max for the best move return the move indexes""" 
        bestscore = float("-inf")
        max_return_depth = self.total_cells 
        move = {}
        for i in range(self.side):
            for j in range(self.side):
                if self.grid[i][j] == "":
                    self.grid[i][j] = player
                    return_depth,score = self.min_max(0,False)
                    # print("score,return_depth,i,j,bestscore_yet,return_depth ",end="")
                    # print(score,return_depth,i,j,bestscore,return_depth)
                    self.grid[i][j] = ""
                    if score > bestscore :
                        if score == bestscore and max_return_depth >= return_depth :
                            max_return_depth = return_depth
                            bestscore = score
                            move['i'] = i
                            move['j'] = j
                        else:
                            max_return_depth = return_depth
                            bestscore = score
                            move['i'] = i
                            move['j'] = j
                            
        return move

    def ai_move(self):
        """moves form th AI min-max algo"""
        if sum([i.count("") for i in self.grid]) == 0 :
            return 
        
        move = self.best_move(self.ai)
                            
        # print(move['i'],move['j'])
        results = self.update_board(move['i'],move['j'],self.ai)
        self.winner = results[0]

if __name__ == "__main__":
    min_max_ai.execute()
