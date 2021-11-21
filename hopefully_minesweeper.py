import numpy as np
import random

class hopefully_minesweeper:
  def __init__(self, dimA, dimB, num_mines):
    self.dimA = dimA
    self.dimB = dimB
    self.num_mines = num_mines

    self.directions_keys_array = ['north', 'north_east', 'east', 'south_east', 'south', 'south_west', 'west', 'north_west']
    self.directions_values_array = [[-1,0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
    self.directions_dict = {} # used in get_space()
    
    self.solution_matrix = np.empty((dimA, dimB), str) # creates an empty matrix of size A x B
    self.solution_matrix.fill('?') # fills matrix with '?'
    self.solution_array = self.solution_matrix.ravel() # converts matrix to 1d array
    self.mines_1darray = [] # indexes of mines (1d)
    self.mines_coords_array = [] # indexes of mines (2d)

    self.puzzle_matrix = np.empty((dimA, dimB), str) # initializes array
    self.puzzle_matrix.fill('?') #fills matrix with '?'

    self.mines_dict = {} # dict of mines (key: 1d index, value: 2d coordinates)

  def generate_solution_board(self):
    self.mines_1darray = random.sample(range(0, len(self.solution_array) - 1), self.num_mines)
    self.mines_1darray.sort()
    for index in self.mines_1darray:
      self.solution_array[index] = 'x'
      self.mines_coords_array.append((int(index / self.dimA), index % self.dimB))

    self.solution_matrix = np.reshape(self.solution_array, (self.dimA, self.dimB)) # 1d -> 2d array

    for key in self.mines_1darray: # creates dict of mines
      for value in self.mines_coords_array:
        self.mines_dict[key] = value
        self.mines_coords_array.remove(value)
        break
    
    for key in self.directions_keys_array: # creates dict of directions
      for value in self.directions_values_array:
        self.directions_dict[key] = value
        self.directions_values_array.remove(value)
        break
    
    for mine in self.mines_dict: # iterates through each mine
      for direction in self.directions_dict: # iterates through surrounding spaces (clockwise starting from north)
        self.get_space(mine, direction) # replaces '?' with number of mines adjacent
    
  def get_space(self, mine, direction):
    coord_x = self.mines_dict.get(mine)[0]
    coord_y = self.mines_dict.get(mine)[1]
    symbol = ''
  
    coord_x += int(self.directions_dict[direction][0])
    coord_y += int(self.directions_dict[direction][1])
  
    if (0 <= coord_x and coord_x <= self.dimA - 1 and 0 <= coord_y and coord_y <= self.dimB - 1): # checks if coords are not out of bounds
      symbol = self.solution_matrix[coord_x][coord_y] # grabs symbol 
      if (symbol != 'x'):
        if (symbol == '?'):
          symbol = '1' # initialize
        elif (symbol.isdigit()): # if space already contains a digit...
          symbol = int(symbol) + 1 # increment by 1
        self.solution_matrix[coord_x][coord_y] = symbol 
        self.solution_matrix = np.where(self.solution_matrix == '?', '0', self.solution_matrix) # replace remaining '?' with 0s

  def play(self):
    print(self.puzzle_matrix)
    
    print("Please enter the row and column of the space you would like to reveal.\nExample: 0,0")
    xy = input()
    xy_coords = xy.split(',')
    reveal_coord_to_index = int(xy_coords[0]) * int(self.dimA) + int(xy_coords[1]) # transforms into 1d array
    
    hit_bomb = False
    solved = False
    
    num_revealed = 0 # number of spaces revealed by player
    num_safe_spaces = int(self.dimA) * int(self.dimB) - self.num_mines # number of spaces that are NOT mines
    
    while (not hit_bomb and not solved): # loops until player finishes the game or hits a mine
      num_revealed += 1 # increments after every user input
      
      if (reveal_coord_to_index in self.mines_dict): # aw crud you hit a bomb
        hit_bomb = True
        print("oh no you hit a bomb lol\nhere's the revealed board:")
        print(self.solution_matrix)
        print("play again? y/n") # honestly you could make a separate function for this
        if (str(input()) == 'n'):
          exit()
        else:
          break
        
      if (int(num_revealed) == int(num_safe_spaces)): # beat the game
        print("gg lol you won")
        solved = True
        print("play again? y/n") # please optimize this lol
        if (str(input()) == 'n'):
          exit()
        else:
          break
      
      # reveals a space one-at-a-time and re-shapes
      self.puzzle_matrix[int(xy_coords[0])][int(xy_coords[1])] = self.solution_matrix[int(xy_coords[0])][int(xy_coords[1])]
      self.puzzle_matrix = np.reshape(self.puzzle_matrix, (self.dimA, self.dimB))
      
      print(self.puzzle_matrix) # prints matrix
      print("Please enter the row and column of the space you would like to reveal next.") # prompt
      
      xy = input() # grabs next coordinate input
      xy_coords = xy.split(',')
      reveal_coord_to_index = int(xy_coords[0]) * int(self.dimA) + int(xy_coords[1])

  def run(): # welcome prompt / "user interface" on the terminal
    print("Welcome to Minesweeper!")
    while True:
      try:
        print("Number of rows?")
        dimA = int(input()) # initializes number of rows
      except ValueError:
        print("Not a valid number, try again!")
      else:
        if dimA > 0:
          break
        else:
          print("Dimension is out of range, try again!")
    
    while True:
      try:
        print("Number of columns?")
        dimB = int(input()) # initializes number of rows
      except ValueError:
        print("Not a valid number, try again!")
      else:
        if dimB > 0:
          break
        else:
          print("Dimension is out of range, try again!")

    while True:
      try:
        print("Number of mines?")
        num_mines = int(input()) # initializes number of rows
      except ValueError:
        print("Not a valid number, try again!")
      else:
        if 0 <= num_mines <= dimA * dimB - 1:
          break
        else:
          print("The number of mines is out of range, try again!")
    
    test = hopefully_minesweeper(dimA, dimB, num_mines)
    test.generate_solution_board()
    test.play()

loop = True # loops until player doesn't wanna play anymore
while (loop):
  hopefully_minesweeper.run()