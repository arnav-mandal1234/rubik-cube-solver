from CubeBasicsVector import Cube
from algorithm_basic import algorithm

def driver():


	solve_mode : 0 - input and solve, 1 - random scramble and solve

	solve_mode = 1

	cube_solve = Cube()
	algo_solve = algorithm()

	if solve_mode is 1:
		cube_solve = algo_solve.scramble_random(cube_solve)
	else:
		cube_solve = algo_solve.input_cube()

	solve_moves = algo_solve.solve(cube_solve)

	print(solve_moves)

driver()
