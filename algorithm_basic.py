import numpy as np
import copy
import mysql.connector
from CubeBasicsVector import Cube

# Beginner's Rubics Cube Algorithm

# Format - "State" - "(Things that are more than previous state)" - "[What to do if not this state, but satisfies previous]"
# 1. Getting the white cross (White Edges) [Solving white Edges]
# 2. Getting the 1st Layer (All Whites)[Solving White Corners]
# 3. Getting the second/middle layer (White + 2 columns of 4 sides adj. to white) [Solving 4 Edges]
# 4. Getting the yellow cross (Yellow Edges) [Solving 4 yellow edges]
# 5. Getting the Yellow Face (Yellow Face whole) [Solving 4 yellow corners]
# 6. Getting the third layer corner pieces (Yellow Corners aligned) [Solving yellow Corners wrt. cube]
# 7. Finishing the cube (All Done) [Solving Yellow Edges wrt. Cube]

class algorithm:

	solved_cube = Cube()

	inv_rubic_switcher = {
            0 : 'W',
            1 : 'R',
            2 : 'G',
            3 : 'O',
            4 : 'B',
            5 : 'Y',
    }
	dir_switcher = {
    		0 : 'U',
            1 : 'D',
            2 : 'L',
            3 : 'R',
            4 : 'F',
            5 : 'B',
    }

	cube_edges_col = ['WR','WG','WO','WB','RG','GO','OB','BR','YR','YG','YO','YB']

	cube_edges_index = [[1,2,0,1],[2,1,0,1],[1,0,2,1],[0,1,2,1],
    				   [1,0,1,2],[1,0,1,0],[1,2,1,0],[1,2,1,2],
    				   [1,2,2,1],[0,1,2,1],[1,0,0,1],[2,1,0,1]]

	cube_corners_col = ['WRG','WGO','WOB','WBR','YRG','YGO','YOB','YBR']

	cube_corners_index = [[2,2,0,0,0,2],[2,0,0,0,2,0],[0,0,2,2,2,0],[0,2,2,2,0,2],
    				   [0,2,2,0,2,2],[0,0,2,0,0,0],[2,0,0,2,0,0],[2,2,0,2,2,2]]

	def __init__(self):
		try:
			self.db = mysql.connector.connect(user='root', password='root',
	                                 host='localhost',
	                                 database='cube_solver')
		except mysql.connector.Error as err:
			  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			  		print("Something is wrong with your user name or password")
			  elif err.errno == errorcode.ER_BAD_DB_ERROR:
			    	print("Database does not exist")
			  else:
			    	print(err)
		else:
			  self.cursor = self.db.cursor()

	def insert(self, query, insert_args):
		self.cursor.execute(sql, insert_args)
		self.db.commit()

	def update(self, query, update_args):
		self.cursor.execute(sql, update_args)
		self.db.commit()

	# algo_solve.insert("insert into input_cube_edge 
	# (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) 
	# values ('RG','1','0','0','1','R','G')")

	# cube_type : U is input, S is solved
	# piece-type : 'C' is corner, 'E'is edge
	def insert_to_db_from_cube(self, cube, piece_type, cube_type):

		max_itr = 12
		if piece_type is 'C':
			max_itr = 8

		for itr in range(max_itr):

			if piece_type is 'C':
				ColorCode = self.cube_corners_col[itr]
				input_args = (ColorCode, 
							   self.cube_corners_index[itr][0], self.cube_corners_index[itr][1], self.cube_corners_index[itr][2],
							   self.cube_corners_index[itr][3], self.cube_corners_index[itr][4], self.cube_corners_index[itr][5],
							   cube.Rubics[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_corners_index[itr][0]][self.cube_corners_index[itr][1]],
						 	   cube.Rubics[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_corners_index[itr][2]][self.cube_corners_index[itr][3]],
						       cube.Rubics[cube.rubic_switcher.get(ColorCode[2],'E')][self.cube_corners_index[itr][4]][self.cube_corners_index[itr][5]])

			else :
				ColorCode = self.cube_edges_col[itr]
				input_args = (ColorCode,
							   cube_edges_index[itr][0], cube_edges_index[itr][1],
							   cube_edges_index[itr][2], cube_edges_index[itr][3],
							   cube.Rubics[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_edges_index[itr][0]][self.cube_edges_index[itr][1]],
						 	   cube.Rubics[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_edges_index[itr][2]][self.cube_edges_index[itr][3]])
				

			if cube_type is 'S':
				if piece_type is 'C':
					self.insert("INSERT INTO solved_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorIndex_x3, ColorIndex_y3, ColorPresent_1, ColorPresent_2, ColorPresent_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", input_args)
				else : 
					self.insert("INSERT INTO solved_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) VALUES (%s, %s, %s, %s, %s, %s, %s)", input_args)
			else :
				if piece_type is 'C':
					self.insert("INSERT INTO input_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorIndex_x3, ColorIndex_y3, ColorPresent_1, ColorPresent_2, ColorPresent_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", input_args)	
				else :
					self.insert("INSERT INTO input_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) VALUES (%s, %s, %s, %s, %s, %s, %s)", input_args)





	# cube is always unsolved, solve cube is never updated
	# piece-type : 'C' is corner, 'E'is edge
	def update_db_from_cube(self, cube, piece_type):

		max_itr = 12
		if piece_type is 'C':
			max_itr = 8

		for itr in range(max_itr):

			if piece_type is 'C':
				ColorCode = self.cube_corners_col[itr]
				update_args = (cube.Rubics[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_corners_index[itr][0]][self.cube_corners_index[itr][1]],
						 	   cube.Rubics[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_corners_index[itr][2]][self.cube_corners_index[itr][3]],
						       cube.Rubics[cube.rubic_switcher.get(ColorCode[2],'E')][self.cube_corners_index[itr][4]][self.cube_corners_index[itr][5]],
						       ColorCode)

			else :
				ColorCode = self.cube_edges_col[itr]
				update_args = (cube.Rubics[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_edges_index[itr][0]][self.cube_edges_index[itr][1]],
						 	   cube.Rubics[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_edges_index[itr][2]][self.cube_edges_index[itr][3]],
						       ColorCode)
				

			
			if piece_type is 'C':
				self.update("UPDATE input_cube_edge SET ColorPresent_1 = %s, ColorPresent_2 = %s, ColorPresent_3 = %s WHERE ColorCode = %s;", update_args)	
			else :
				self.update("UPDATE input_cube_edge SET ColorPresent_1 = %s, ColorPresent_2 = %s WHERE ColorCode = %s;", update_args)


	def scramble_random(self,cube_scrmbl):

		random_scramble_moves = "E"

		# No of random scrambles
		num_rand_scramble = 50

		rand_moves_ref_center = np.ceil(np.random.rand(num_rand_scramble)*6)
		rand_moves_ref_up_center = np.ceil(np.random.rand(num_rand_scramble)*6)
		rand_moves_move_face = np.ceil(np.random.rand(num_rand_scramble)*6)
		rand_moves_move_direction = np.ceil(np.random.rand(num_rand_scramble)*2)

		for move_rand in range(num_rand_scramble):
			ref_center = self.inv_rubic_switcher.get(int(rand_moves_ref_center[move_rand]), "E")
			ref_up_center = self.inv_rubic_switcher.get(int(rand_moves_ref_up_center[move_rand]), "E")
			move_id_given = self.dir_switcher.get(int(rand_moves_move_face[move_rand]), "E")
			if (rand_moves_move_direction[move_rand]) is 1:
				move_id_given = move_id_given + 'i'
			cube_scrmbl.make_movdbc = ("localhost","root","1234","users")


		# perform random scramble

		print("Random Scrambling Moves are -> "+random_scramble_moves)

		return cube_scrmbl

	def input_cube(self):

		cube_input = Cube()

		# take input

		return cube_input

	def check_state(self,state,cube_to_check):

		# If ret_flag is 1 then present state is satisfied acc. to state_flag
		ret_flag = 1

		state_flag = self.check_state_flags.get(state, "E")

		for colors_cube in range(6):
			for x_index in range(3):
				for y_index in range(3):
					if state_flag[colors_cube][x_index][y_index] is 1:
						if (cube_to_check[colors_cube][x_index][y_index] != self.solved_cube[colors_cube][x_index][y_index]):
							return 0

		return ret_flag

	# 1. Getting the white cross (White Edges) [Solving white Edges]
	# def solve_state_one(unsolved_cube,string_solved_cube):
	#
	# # 2. Getting the 1st Layer (All Whites)[Solving White Corners]
	# def solve_state_two(unsolved_cube,string_solved_cube):
	#
	#
	# # 3. Getting the second/middle layer (White + 2 columns of 4 sides adj. to white) [Solving 4 Edges]
	# def solve_state_three(unsolved_cube,string_solved_cube):
	#
	#
	# # 4. Getting the yellow cross (Yellow Edges) [Solving 4 yellow edges]
	# def solve_state_four(unsolved_cube,string_solved_cube):
	#
	#
	# # 5. Getting the Yellow Face (Yellow Face whole) [Solving 4 yellow corners]
	# def solve_state_five(unsolved_cube,string_solved_cube):
	#
	#
	# # 6. Getting the third layer corner pieces (Yellow Corners aligned) [Solving yellow Corners wrt. cube]
	# def solve_state_six(unsolved_cube,string_solved_cube):
	#
	#
	# # 7. Finishing the cube (All Done) [Solving Yellow Edges wrt. Cube]
	# def solve_state_seven(unsolved_cube,string_solved_cube):


	def solve_state_main(self,state,unsolved_cube,string_solved_cube):

		if state is 1:
			self.solve_state_one(unsolved_cube,string_solved_cube)
		elif state is 2:
			self.solve_state_two(unsolved_cube,string_solved_cube)
		elif state is 3:
			self.solve_state_three(unsolved_cube,string_solved_cube)
		elif state is 4:
			self.solve_state_four(unsolved_cube,string_solved_cube)
		elif state is 5:
			self.solve_state_five(unsolved_cube,string_solved_cube)
		elif state is 6:
			self.solve_state_six(unsolved_cube,string_solved_cube)
		elif state is 7:
			self.solve_state_seven(unsolved_cube,string_solved_cube)
		else:
			print("State out of bounds, State ="+str(state))

		print("State "+str(state)+" is solved")

		return

	def solve(self,unsolved_cube):

		solution = "E"

		for state in range(1,8):
			if self.check_state(state,unsolved_cube) is 0:
				if self.check_state(state-1,unsolved_cube) is 1:
					# If cube doesn't satisfy this state but satisfies previous state conditions
					self.solve_state_main(state,unsolved_cube,string_solved_cube)
				else:
					# This is encountered if wrong moves result in Cube going into previous states
					print("Problem Algorithm Not Stable Exit at State ")
					print(state)
					state = state - 2
			else:
				# This is encountered if the cube already satisfies current state
				print("State "+state+" is solved")

		return solution
