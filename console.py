import collections

def print_world(world):
	print("\n   A  B  C  D  E  F  G  H ")
	print(" +-------------------------+")
	index = 1
	row_s = ""
	for row in world.board:
		row_s = str(index) + "| "
		for i in row:
			# Add character
			if i == 'e': row_s += ' '
			if i == 'b': row_s += 'b'
			if i == 'w': row_s += 'w'

			# Add spacing
			row_s += " | "
			row_s = row_s[:-1]

		# print row
		print(row_s)
		index += 1
		print(" +-------------------------+\n")

def print_info(player):
	print("Hello, when the game is shown on the console please be aware that\n")
	print("b is a black pawn \n")
	print("w is a white pawn \n\n")

def get_user():
	# vars
	Player1 = ""
	Player2 = ""
	turn = ""

	# dynamic input
	print("Welcome to the pawn game!")
	print("The white and black player compete to make their pawns get to other side")
	print("The White player always goes first and is Player 1")
	
	Player1 = 'w'
	Player2 = 'b'
	turn = 'w'

	return Player1, Player2, turn

def get_move(world, user, recently_used):
	# vars
	move = []
	valid = 0

	while(valid != 1):
		print("Please enter a move as Column-Row to Column-Row\n ex) A3 B4 or world to print the world again")
		choice = input(">").lower()
		if choice == 'world':
			print_world(world)
		elif len(choice.strip()) == 5:
			l = choice.split()
			if len(l) != 2:
				print("Invalid input")
			else:
				# Get variables
				from_col = l[0][0]
				from_row = l[0][1]
				to_col = l[1][0]
				to_row = l[1][1]

				# Note what is valid
				valid_col = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
				valid_row = ['1', '2', '3', '4', '5', '6', '7', '8']

				# Check for validity
				if from_col in valid_col and to_col in valid_col and to_row in valid_row and from_row in valid_row:
					# Translate
					try:
						from_col = valid_col.index(from_col)
						to_col = valid_col.index(to_col)
						from_row = valid_row.index(from_row)
						to_row = valid_row.index(to_row)
					except:
						print("That move is not valid.")
						continue
					
					#Validates the input
					valid = validate_move(world, from_col, from_row, to_col, to_row, user)
					print(user, valid)

					if valid == -1: #They tried to move other team
						print("You can't move a pawn you don't control. Try Again.")
					elif valid == 0: #Not valid
						print("That move is not valid.")
						continue
					elif valid == 1: #Valid!!!
						valid = validate_killing_move(world, from_col, from_row, to_col, to_row, user, recently_used)

						if valid == 0:
							return ([from_row, from_col, to_row, to_col], 1)
						elif valid == 1:
							return ([from_row, from_col, to_row, to_col], 0)
						elif valid == -1:
							print("You have to make a killing move")
							continue

				else:
					print("Invalid input")
		else:
			print("Invalid input")

	# This should never happen
	return ([0,0,0,0], 1)

def print_tie():
	print("A deadlock has been reached\nNo Winner, Tie\n")

def print_victory(player, isUser):
	if player == 'b': player = "Black"
	if player == 'w': player = "White"
	if isUser:
		comment = "the User"
	else:
		comment = "the Computer"
	print("!!!A Winner has been reached!!!\nWinner is " + player + ", " + comment)

def validate_killing_move(world, from_col, from_row, to_col, to_row, user, recently_used):

	if (from_row, from_col) in recently_used:
		return -1

	print(len(world.board), len(world.board[0]))
	killing_list = collections.defaultdict(list)
	for i in range(8):
		for j in range(8):
			if (world.board[i][j] == user) and (user == 'w'):
				if (i-1 >=0) and (j-1 >= 0) and (world.board[i-1][j-1]) == 'b':
					if (i, j) not in recently_used:
						killing_list[(i, j)].append((i-1, j-1))
				if (i-1 >=0) and (j+1 < 8) and (world.board[i-1][j+1]) == 'b':
					if (i, j) not in recently_used:
						killing_list[(i, j)].append((i-1, j+1))
			elif (world.board[i][j] == user) and (user == 'b'):
				if (i+1 < 8) and (j-1 >= 0) and (world.board[i+1][j-1]) == 'w':
					if (i, j) not in recently_used:
						killing_list[(i, j)].append((i+1, j-1))
				if (i+1 < 8) and (j+1 < 8) and (world.board[i+1][j+1]) == 'w':
					if (i, j) not in recently_used:
						killing_list[(i, j)].append((i+1, j+1))
	
	if len(killing_list) <= 0:
		return 0
	if (from_row, from_col) not in killing_list:
		print("from 1st -1: ", killing_list, from_row, from_col)
		return -1
	else:
		lst = killing_list[(from_row, from_col)]
		if (to_row, to_col) in lst:
			return 1
		else:
			print("from 2nd -1: ", killing_list, from_row, from_col)
			return -1


#Validates a user input
def validate_move(world, from_col, from_row, to_col, to_row, user):
	#Starts Validation
	#If white
	if (world.board[from_row][from_col]== 'w') and (user == 'w'): 
		print(user, world.board[from_row][from_col], "1")
		if(to_row == from_row -1): #If going one space foward  - covers non-attack moves

			if (to_col == from_col + 1) or (to_col == from_col -1): #Diagonal

				if world.board[to_row][to_col] == 'b': #Can attack opponent
					return 1
				else:
					return 0

			elif (to_col == from_col):
				if world.board[to_row][to_col] == 'e':
					return 1
				else:
					return 0

			else: #Moving multiple diagonals - this is not a knight
				return 0
			
		else: #Moving multiple or no rows
			return 0

	#IF they are black but trying to control white
	elif (world.board[from_row][from_col] == 'w') and (user == 'b'):
		return -1

	#If black
	elif world.board[from_row][from_col] == 'b' and user == 'b':
		if(to_row == from_row +1): #If going one space foward  - covers non-attack moves

			if (to_col == from_col + 1) or (to_col == from_col -1): #Diagonal

				if world.board[to_row][to_col] == 'w': #Can attack opponent
					return 1
				else:
					return 0

			elif (to_col == from_col):
				if world.board[to_row][to_col] == 'e':
					return 1
				else:
					return 0

			else: #Moving multiple diagonals - this is not a knight
				return 0
			
		else: #Moving multiple or no rows
			return 0

	#IF they are white but trying to control black
	elif (world.board[from_row][from_col] == 'b') and (user == 'w'):
		print(user, world.board[from_row][from_col])
		return -1

	#If they try moving something not there
	else: #e so invalid 
		return 0
