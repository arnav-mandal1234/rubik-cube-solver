from CubeBasicsVector import Cube
from algorithm_basic import algorithm

def driver():


	algo = algorithm()
	cube = Cube()
	cube_scramble = algo.scramble_random1(cube)
	algo.insert_to_db_from_cube(cube, 'U')
	algo.update_db_from_cube(cube_scramble, 'E')
	algo.update_db_from_cube(cube_scramble, 'C')
	print(algo.find_piece(cube_scramble, 'E', 'WR'))
	print(algo.find_piece(cube_scramble, 'E', 'WG'))
	print(algo.find_piece(cube_scramble, 'E', 'WO'))
	print(algo.find_piece(cube_scramble, 'E', 'WB'))
	print(algo.find_piece(cube_scramble, 'E', 'RG'))
	print(algo.find_piece(cube_scramble, 'E', 'GO'))
	print(algo.find_piece(cube_scramble, 'E', 'OB'))
	print(algo.find_piece(cube_scramble, 'E', 'BR'))
	print(algo.find_piece(cube_scramble, 'E', 'YR'))
	print(algo.find_piece(cube_scramble, 'E', 'YG'))
	print(algo.find_piece(cube_scramble, 'E', 'YO'))
	print(algo.find_piece(cube_scramble, 'E', 'YB'))

	# algo.solve_state_one(cube_scramble, "RR" )
	# #algo.insert_to_db_from_cube(cube_scramble,'U')
	# print("---------------------------------------------------------------------------------------")
	# print(algo.check_state_one(cube_scramble))
	# cube_scramble.print_Cube()


	# solve_mode : 0 - input and solve, 1 - random scramble and solve
	#
	# solve_mode = 1
	#
	# cube_solve = Cube()
	# algo_solve = algorithm()
	#
	# if solve_mode is 1:
	# 	cube_solve = algo_solve.scramble_random(cube_solve)
	# else:
	# 	cube_solve = algo_solve.input_cube()
	#
	# solve_moves = algo_solve.solve(cube_solve)
	#
	# print(solve_moves)

driver()
