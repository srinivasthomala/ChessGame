import math
import world as world_mod

# Global
GAME_TIE = "TIE"
GAME_BLACK = 'b'
GAME_WHITE  = 'w'
GAME_EMPTY = 'e'
_BASE_WIN = 100
_BASE_LOSS = -100

def get_possible_moves(world, player):
	moveset = []
	for i in range(8):
		for j in range(8):
			if world.board[i][j] == player:
				# We found a pawn, can it move?
				move = move_forward(world.board, i, j, player)
				attack = attack_forward(world.board, i, j, player)
				if move: moveset.append(move)
				if attack: moveset.append(attack)

	# Return found move
	return moveset

def move_forward(world, i, j, player):
	if player == GAME_BLACK:
		if i + 1 > 7 or world[i + 1 ][j] != GAME_EMPTY:
			return False
		else:
			return [i, j, i+1, j]
	
	# white
	if player == GAME_WHITE:
		if 0 > i - 1 or world[i - 1][j] != GAME_EMPTY:
			return False
		else:
			return [i, j, i-1, j]

	# Return move
	return False

def attack_forward(world, i, j, player):
	# Check if we can attack a piece
	# white
	if player == GAME_WHITE:
		# Check if upward move is possible
		if 0 > i - 1:
			return False

		# Check two cases
		# left
		if 0 <= j - 1 and world[i - 1][j - 1] == GAME_BLACK:
			return [i, j, i-1, j-1]
		# Right
		if 7 >= j + 1 and world[i - 1][j + 1] == GAME_BLACK:
			return [i, j, i-1, j+1]

	if player == GAME_BLACK:
		# Check if upward move is possible
		if i + 1 > 7:
			return False

		# Check two cases
		# left
		if 0 <= j - 1 and world[i + 1][j - 1] == GAME_WHITE:
			return [i, j, i+1, j-1]
		# Right
		if 7 >= j + 1 and world[i + 1][j + 1] == GAME_WHITE:
			return [i, j, i+1, j+1]			

	# Something happened
	return False 

def evaluator_func(world, player):
	# Evaluate whether a victory has been had
	s_row = world.board[0]
	t_row = world.board[7]

	# Check that any remaining enemy pawns exist
	player_exists = False
	for i in range(8):
		for j in range(8):
			if world.board[i][j] == player:
				player_exists = True
	if not player_exists:
		return _BASE_LOSS, -1, -1

	# Check white
	if player == GAME_WHITE:
		if GAME_WHITE in s_row:
			return _BASE_WIN, -1, -1
		if GAME_BLACK in t_row:
			return _BASE_LOSS, -1, -1

	# Check black
	else:
		if GAME_WHITE in s_row:
			return _BASE_LOSS, -1, -1
		if GAME_BLACK in t_row:
			return _BASE_WIN, -1, -1

	# Check if deadlock has happened
	if player == GAME_BLACK:
		opponent = GAME_WHITE
	else:
		opponent = GAME_BLACK
	opp_moves =	get_possible_moves(world, opponent)	
	moves = get_possible_moves(world, player)
	if len(moves) == 0 and len(opp_moves) == 0:
		return GAME_TIE, -1, -1
	elif len(moves) == 0 and len(opp_moves) != 0:
		return GAME_TIE, -1, -1
	elif len(moves) != 0 and len(opp_moves) == 0:
		return GAME_TIE, -1, -1
	else:
		return 0, moves, opp_moves

def check_victory(world):
	# Run the world through the evaluator function
	worth, empty1, empty2 = evaluator_func(world, GAME_WHITE)
	if worth == _BASE_WIN:
		return GAME_WHITE
	elif worth == _BASE_LOSS:
		return GAME_BLACK
	elif worth == GAME_TIE:
		return GAME_TIE
	else:
		return False 