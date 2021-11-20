import numpy as np
import random

class hopefully_minesweeper:
  def __init__(self, dimA, dimB, num_mines):
    self.dimA = dimA
    self.dimB = dimB
    self.num_mines = num_mines

    self.solution_matrix = np.empty((dimA, dimB), str) # creates an empty matrix of size A x B
    self.solution_matrix.fill('?') # fills matrix with '?'
    self.solution_array = self.solution_matrix.ravel() # converts matrix to 1d array
    self.mines_1darray = [] # indexes of mines (1d)
    self.mines_coords_array = [] # indexes of mines (2d)

    self.puzzle_matrix = np.empty((dimA, dimB), str) # initializes array
    self.puzzle_matrix.fill('?') #fills matrix with '?'

    self.mines_dict = {} # dict of mines (key: 1d index, value: 2d coordinates)

  def generate_solution_board(self):
    # generates mines
    self.mines_1darray = random.sample(range(0, len(self.solution_array) - 1), self.num_mines)
    self.mines_1darray.sort()
    for index in self.mines_1darray:
      self.solution_array[index] = 'x'
      self.mines_coords_array.append((int(index / self.dimA), index % self.dimB))

    # reshapes 1d to 2d array
    self.solution_matrix = np.reshape(self.solution_array, (self.dimA, self.dimB))

    # creates dict
    for key in self.mines_1darray:
      for value in self.mines_coords_array:
        self.mines_dict[key] = value
        self.mines_coords_array.remove(value)
        break

    # print("Mine Dictionary:", self.mines_dict)

    directions_arr = {'north', 'north_east', 'east', 'south_east', 'south', 'south_west', 'west', 'north_west'}
    for mine in self.mines_dict: # iterates through each mine
      for direction in directions_arr: # iterates through surrounding spaces (clockwise starting from north)
        self.get_space(mine, direction) 
    
    # print(self.solution_matrix)
  
  def toStr(self): # i don't even think this is needed but check later
    print(self.mines_dict)

  def get_space(self, mine, direction):
    coord_x = self.mines_dict.get(mine)[0]
    coord_y = self.mines_dict.get(mine)[1]
    symbol = ''

  # PLEASE make this a dictionary instead when you're less lazy lol, also a graphic would be cool :^)
    if (direction == 'north'):
      coord_x = coord_x - 1
    if (direction == 'north_east'):
      coord_x -= 1
      coord_y += 1
    if (direction == 'east'):
      coord_y += 1
    if (direction == 'south_east'):
      coord_x += 1
      coord_y += 1
    if (direction == 'south'):
      coord_x += 1
    if (direction == 'south_west'):
      coord_x += 1
      coord_y -= 1
    if (direction == 'west'):
      coord_y -= 1
    if (direction == 'north_west'):
      coord_x -= 1
      coord_y -= 1

    if (0 <= coord_x and coord_x <= self.dimA - 1 and 0 <= coord_y and coord_y <= self.dimB - 1): # checks if coords are not out of bounds
      symbol = self.solution_matrix[coord_x][coord_y] # grabs symbol 
      if (symbol != 'x'):
        if (symbol == '?'):
          symbol = '1' # initialize
        elif (symbol.isdigit()): # if space already contains a digit...
          symbol = int(symbol) + 1 # increment by 1
        self.solution_matrix[coord_x][coord_y] = symbol 
        self.solution_matrix = np.where(self.solution_matrix == '?', '0', self.solution_matrix) # replace remaining '?' with 0s

  def play(self): # yay you get to play the game
    print(self.puzzle_matrix)
    
    print("Please enter the row and column of the space you would like to reveal.\nExample: 0,0")
    xy = input()
    xy_coords = xy.split(',')
    reveal_coord_to_index = int(xy_coords[0]) * int(self.dimA) + int(xy_coords[1]) # transforms into 1d array
    
    hit_bomb = False
    solved = False
    
    num_revealed = 0
    num_safe_spaces = int(self.dimA) * int(self.dimB) - self.num_mines
    
    while (not hit_bomb and not solved):
      num_revealed += 1
      
      if (reveal_coord_to_index in self.mines_dict):
        hit_bomb = True
        print("oh no you hit a bomb lol\nhere's the revealed board:")
        print(self.solution_matrix)
        print("play again? y/n")
        if (str(input()) == 'n'):
          exit()
        else:
          break
        
      if (int(num_revealed) == int(num_safe_spaces)):
        print("gg lol you won")
        solved = True
        print("play again? y/n")
        if (str(input()) == 'n'):
          exit()
        else:
          break
        
      self.puzzle_matrix[int(xy_coords[0])][int(xy_coords[1])] = self.solution_matrix[int(xy_coords[0])][int(xy_coords[1])]
      self.puzzle_matrix = np.reshape(self.puzzle_matrix, (self.dimA, self.dimB))
      
      print(self.puzzle_matrix)
      print("Please enter the row and column of the space you would like to reveal next.")
      
      xy = input()
      xy_coords = xy.split(',')
      reveal_coord_to_index = int(xy_coords[0]) * int(self.dimA) + int(xy_coords[1])

  def run():
    print("Welcome to Minesweeper!\nNumber of rows?")
    dimA = int(input())
    
    print("Number of columns?")
    dimB = int(input())
    
    print("Number of mines?")
    num_mines = int(input())
    
    test = hopefully_minesweeper(dimA, dimB, num_mines)
    test.generate_solution_board()
    test.play()

loop = True
while (loop):
  hopefully_minesweeper.run()