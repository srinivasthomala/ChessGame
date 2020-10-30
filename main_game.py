# Import local files
import world
import algo
import console

# Declare global variables
Player1, Player2, turn = console.get_user()
stop_loop = False

# Init the world
game_world = world.game_world()
console.print_info(Player2)

# Show the world
console.print_world(game_world)

# Start the game loop
while(stop_loop == False):

	recently_used = set()
	# Get the next move
	if turn == Player1:
		flag = 0
		while flag != 1:
			print("w 's move \n")
			move, flag = console.get_move(game_world, Player1, recently_used)
			recently_used.add((move[2], move[3]))

			game_world.update_world(move)
			console.print_world(game_world)
			# Check for victory
			victory = algo.check_victory(game_world)
			if victory == Player1:
				console.print_world(game_world)
				console.print_victory(Player1, False)
				stop_loop = True
				flag = 1
			elif victory == Player2:
				console.print_world(game_world)
				console.print_victory(Player2, True)
				stop_loop = True
				flag = 1
			elif victory == algo.GAME_TIE:
				console.print_world(game_world)
				console.print_victory(Player2, False)
				stop_loop = True
				flag = 1
		turn = Player2
	else:
		flag = 0
		while flag != 1:
			print("b 's move \n")
			move, flag = console.get_move(game_world, Player2, recently_used)
			recently_used.add((move[2], move[3]))

			game_world.update_world(move)
			console.print_world(game_world)
			# Check for victory
			victory = algo.check_victory(game_world)
			if victory == Player1:
				console.print_world(game_world)
				console.print_victory(Player1, False)
				stop_loop = True
				flag = 1
			elif victory == Player2:
				console.print_world(game_world)
				console.print_victory(Player2, True)
				stop_loop = True
				flag = 1
			elif victory == algo.GAME_TIE:
				console.print_world(game_world)
				console.print_victory(Player1, False)
				stop_loop = True
				flag = 1
		turn = Player1