import random
import numpy as np

# need to make proper classes and final 
# this will be the command line also make gui in another class

class tic_tac_toe:
	"""This is the cmd version for single player and random moves from ai"""
	def __init__(self):
		"""initialize"""
		self.grid = [
			['','',''],
			['','',''],
			['','','']
		]
		self.side = len(self.grid)
		self.total_cells = (self.side ** 2) 
		self.step_count = 0
		self.winner = False
		self.human = "x"
		self.ai = "o"

	def is_win(self,player):
		"""check in bloard if plyer wins"""
		# rows
		for i in range(self.side):
			if self.grid[i].count(player) == self.side:
				return True,'row',i
		# cols
		for col in range(self.side):
			if [i[col] for i in self.grid].count(player) == self.side:
				return True,'col',col
		
		# digonals 0 is (0,0)(1,1)(2,2) and 1 is (0,2)(1,1)(2,1) 
		digonal0 ,digonal1= [],[]
		for i,row in enumerate(self.grid):
			digonal0.append(row[i])
			digonal1.append(row[self.side - i-1])
		
		if digonal0.count(player) == self.side : return True,'dig',0
		if digonal1.count(player) == self.side : return True,'dig',1
	
		return False,None,None

	def print_board(self):
		"""print board butifully in the commad line """
		print()
		for i in range(self.side):
			for j in range(self.side):
				if self.grid[i][j] == "" : cell = " "
				else :cell = self.grid[i][j]
				print(cell,end = " ")
				if j != self.side -1 :
					print("|",end = " ")

			print()
			if i != self.side -1 : print("----------")
		print()

	def who_wins(self):
		"""check which player win"""
		if self.is_win(self.human)[0] : 
			return self.human
		elif self.is_win(self.ai)[0] : 
			return self.ai
		elif sum([i.count("") for i in self.grid]) == 0 : 
			return 'Tie'

	def update_board(self,row,col,player):
		""" update the elements onto the board and check if moving player wins and return the results"""
		self.grid[row][col] = player
		self.step_count += 1
		return self.is_win(player)

	def ai_move(self):
		"""random move for the computer """
		while self.step_count != self.total_cells:
			a,b = random.randint(0,2),random.randint(0,2)
			# print(a,b)
			if self.grid[a][b] == "":
				results = self.update_board(a,b,self.ai)
				self.winner = results[0]
				if results[0] : 
					self.print_board()
					print(self.ai,"Wins")
				break

	def runner(self):
		"""run the fucntion which lae the user play"""
		# print the empty board 
		self.print_board()
		# run if sum of empty places is not 0 and winner is not decided 
		while sum([i.count("") for i in self.grid]) != 0 and not self.winner:
			# take inputs for the palying possition
			try :
				print("Enter the possition :-")
				a = int(input("\trow :")) - 1
				b = int(input("\tcol :")) - 1
				if ( a not in range(0,3) ) or (b not in range(0,3)):
					print("Enter The row and col in the range of 1,2,3")
					continue
			except KeyboardInterrupt : 
				break
			except :
				print("Invalid values -")
				print("Enter The row and col in int")
				continue
			
			if self.grid[a][b] == "" : 
				results = self.update_board(a,b,self.human)
				self.winner = results[0]
				if results[0] : 
					self.print_board()
					print(self.human, "wins")
					break
			else:
				print("Already used , not Possible ,try it Again")
				continue
			
			# ai move
			self.ai_move()
			self.print_board()
		else :
			# if no possition left on the board and no one wins
			if not self.winner:
				print("Its a Tie")
		print("Game_ended")

	@classmethod
	def execute(cls):
		"""Run the class on call"""
		cl = cls()
		cl.runner()


if __name__ == "__main__":
	tic_tac_toe.execute()
