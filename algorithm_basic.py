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
		self.cursor.execute(query, insert_args)
		self.db.commit()

	def update(self, query, update_args):
		self.cursor.execute(query, update_args)
		self.db.commit()

	def query(self, query, query_args):
		self.cursor.execute(query, query_args)
		return self.cursor.fetchall()

	# algo_solve.insert("insert into input_cube_edge 
	# (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) 
	# values ('RG','1','0','0','1','R','G')")

	# cube_type : U is input, S is solved
	def insert_to_db_from_cube(self, cube, cube_type):

		max_itr = 12

		for itr in range(max_itr):
			{'colorcode': u'BR', 'orientation': 'WR'}

			if itr < 8:
				ColorCode = self.cube_corners_col[itr]
				input_args_corners = (ColorCode,
								   self.cube_corners_index[itr][0], self.cube_corners_index[itr][1], self.cube_corners_index[itr][2],
								   self.cube_corners_index[itr][3], self.cube_corners_index[itr][4], self.cube_corners_index[itr][5],
								   cube.Rubic[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_corners_index[itr][0]][self.cube_corners_index[itr][1]],
								   cube.Rubic[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_corners_index[itr][2]][self.cube_corners_index[itr][3]],
								   cube.Rubic[cube.rubic_switcher.get(ColorCode[2],'E')][self.cube_corners_index[itr][4]][self.cube_corners_index[itr][5]])

			ColorCode = self.cube_edges_col[itr]
			input_args_edges = (ColorCode,
								self.cube_edges_index[itr][0], self.cube_edges_index[itr][1],
								self.cube_edges_index[itr][2], self.cube_edges_index[itr][3],
							   cube.Rubic[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_edges_index[itr][0]][self.cube_edges_index[itr][1]],
							   cube.Rubic[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_edges_index[itr][2]][self.cube_edges_index[itr][3]])
				

			if cube_type is 'S':
				if itr < 8:
					self.insert("INSERT INTO solved_cube_corner (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorIndex_x3, ColorIndex_y3, ColorPresent_1, ColorPresent_2, ColorPresent_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", input_args_corners)
				self.insert("INSERT INTO solved_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) VALUES (%s, %s, %s, %s, %s, %s, %s)", input_args_edges)
			else :
				if itr < 8:
					self.insert("INSERT INTO input_cube_corner (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorIndex_x3, ColorIndex_y3, ColorPresent_1, ColorPresent_2, ColorPresent_3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", input_args_corners)
				self.insert("INSERT INTO input_cube_edge (ColorCode, ColorIndex_x1, ColorIndex_y1, ColorIndex_x2, ColorIndex_y2, ColorPresent_1, ColorPresent_2) VALUES (%s, %s, %s, %s, %s, %s, %s)", input_args_edges)





	# cube is always unsolved, solve cube is never updated
	# piece-type : 'C' is corner, 'E'is edge
	def update_db_from_cube(self, cube, piece_type):

		max_itr = 12
		if piece_type is 'C':
			max_itr = 8

		for itr in range(max_itr):

			if piece_type is 'C':
				ColorCode = self.cube_corners_col[itr]
				update_args = (cube.Rubic[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_corners_index[itr][0]][self.cube_corners_index[itr][1]],
						 	   cube.Rubic[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_corners_index[itr][2]][self.cube_corners_index[itr][3]],
						       cube.Rubic[cube.rubic_switcher.get(ColorCode[2],'E')][self.cube_corners_index[itr][4]][self.cube_corners_index[itr][5]],
						       ColorCode)

			else :
				ColorCode = self.cube_edges_col[itr]
				update_args = (cube.Rubic[cube.rubic_switcher.get(ColorCode[0],'E')][self.cube_edges_index[itr][0]][self.cube_edges_index[itr][1]],
						 	   cube.Rubic[cube.rubic_switcher.get(ColorCode[1],'E')][self.cube_edges_index[itr][2]][self.cube_edges_index[itr][3]],
						       ColorCode)
				

			
			if piece_type is 'C':
				self.update("UPDATE input_cube_corner SET ColorPresent_1 = %s, ColorPresent_2 = %s, ColorPresent_3 = %s WHERE ColorCode = %s;", update_args)
			else :
				self.update("UPDATE input_cube_edge SET ColorPresent_1 = %s, ColorPresent_2 = %s WHERE ColorCode = %s;", update_args)

	def scramble_random1(self, cube_scrmbl):

		scramble = "R"
		for c in scramble:
			cube_scrmbl.make_move('W','R',c)
		return cube_scrmbl

	# def scramble_random(self,cube_scrmbl):
	#
	# 	random_scramble_moves = "E"
	#
	# 	# No of random scrambles
	# 	num_rand_scramble = 50
	#
	# 	rand_moves_ref_center = np.floor(np.random.rand(num_rand_scramble)*6)
	# 	rand_moves_ref_up_center = np.floor(np.random.rand(num_rand_scramble)*6)
	# 	rand_moves_move_face = np.floor(np.random.rand(num_rand_scramble)*6)
	# 	rand_moves_move_direction = np.floor(np.random.rand(num_rand_scramble)*2)
	#
	# 	for move_rand in range(num_rand_scramble):
	# 		ref_center = self.inv_rubic_switcher.get(int(rand_moves_ref_center[move_rand]), "E")
	# 		ref_up_center = self.inv_rubic_switcher.get(int(rand_moves_ref_up_center[move_rand]), "E")
	# 		move_id_given = self.dir_switcher.get(int(rand_moves_move_face[move_rand]), "E")
	# 		if (int(rand_moves_move_direction[move_rand])) == 1:
	# 			move_id_given = move_id_given + 'i'
	# 		print(str(int(rand_moves_ref_center[move_rand]))+" "+str(int(rand_moves_ref_up_center[move_rand]))+" "+str(int(rand_moves_move_face[move_rand]))+" "+ str(int(rand_moves_move_direction[move_rand]))+" "+move_id_given)
	# 		cube_scrmbl.make_move(ref_center, ref_up_center, move_id_given)
	#
	# 	# perform random scramble
	#
	# 	print("Random Scrambling Moves are -> "+random_scramble_moves)
	#
	# 	return cube_scrmbl

	def input_cube(self):

		cube_input = Cube()

		# take input\

		return cube_input


	def check_state_one(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1, ColorPresent_2 FROM input_cube_edge WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s;",
			(self.cube_edges_col[0], self.cube_edges_col[1], self.cube_edges_col[2], self.cube_edges_col[3]))

		for ColorCode, ColorPresent_1, ColorPresent_2 in result:
			if ColorCode[0] != ColorPresent_1 or ColorCode[1] != ColorPresent_2:
				return 0

		return 1

	def check_state_two(self, unsolved_cube) :

		result = self.query("SELECT ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 FROM input_cube_corner WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ;",
			(self.cube_corners_col[0], self.cube_corners_col[1], self.cube_corners_col[2], self.cube_corners_col[3]))

		for ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 in result:
			if ColorCode[0] != ColorPresent_1 or ColorCode[1] != ColorPresent_2 or ColorCode[2] != ColorPresent_3 :
				return 0

		return 1

	def check_state_three(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1, ColorPresent_2 FROM input_cube_edge WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ",
			(self.cube_edges_col[4], self.cube_edges_col[5], self.cube_edges_col[6], self.cube_edges_col[7]))

		for ColorCode, ColorPresent_1, ColorPresent_2 in result:
			if ColorCode[0] != ColorPresent_1 or ColorCode[1] != ColorPresent_2:
				return 0

		return 1

	def check_state_four(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1 FROM input_cube_edge WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ",
			(self.cube_edges_col[8], self.cube_edges_col[9], self.cube_edges_col[10], self.cube_edges_col[11]))

		for ColorCode, ColorPresent_1 in result:
			if ColorCode[0] != ColorPresent_1 :
				return 0

		return 1

	def check_state_five(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1 FROM input_cube_corner WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ",
			(self.cube_corners_col[4], self.cube_corners_col[5], self.cube_corners_col[6], self.cube_corners_col[7]))

		for ColorCode, ColorPresent_1 in result:
			if ColorCode[0] != ColorPresent_1 :
				return 0

		return 1

	def check_state_six(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 FROM input_cube_corner WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ",
			(self.cube_corners_col[4], self.cube_corners_col[5], self.cube_corners_col[6], self.cube_corners_col[7]))

		for ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 in result:
			if ColorCode[0] != ColorPresent_1 or ColorCode[1] != ColorPresent_2 or ColorCode[2] != ColorPresent_3:
				return 0

		return 1

	def check_state_seven(self, unsolved_cube):

		result = self.query(
			"SELECT ColorCode, ColorPresent_1, ColorPresent_2 FROM input_cube_edge WHERE ColorCode = %s OR ColorCode = %s OR ColorCode = %s OR ColorCode = %s ",
			(self.cube_edges_col[8], self.cube_edges_col[9], self.cube_edges_col[10], self.cube_edges_col[11]))

		for ColorCode, ColorPresent_1, ColorPresent_2 in result:
			if ColorCode[0] != ColorPresent_1 or ColorCode[1] != ColorPresent_2:
				return 0

		return 1


	def check_state(self, cube_to_check):

		self.update_db_from_cube(cube_to_check, 'C')
		self.update_db_from_cube(cube_to_check, 'E')

		if ~self.check_state_one(cube_to_check):
			return 1
		if ~self.check_state_two(cube_to_check):
			return 2
		if ~self.check_state_three(cube_to_check):
			return 3
		if ~self.check_state_four(cube_to_check):
			return 4
		if ~self.check_state_five(cube_to_check):
			return 5
		if ~self.check_state_six(cube_to_check):
			return 6
		if ~self.check_state_seven(cube_to_check):
			return 7
		return 8

	def find_piece(self, unsolved_cube, piece_type, piece_name):

		self.update_db_from_cube(unsolved_cube, piece_type)
		if piece_type is 'E':
			query = self.query(
				"SELECT ColorCode, ColorPresent_1, ColorPresent_2 FROM input_cube_edge WHERE (ColorPresent_1 = %s AND ColorPresent_2 = %s) OR (ColorPresent_1 = %s AND ColorPresent_2 = %s);",
				(piece_name[0], piece_name[1], piece_name[1], piece_name[0]))
			result = {'colorcode': query[0][0],
					  'orientation': str(query[0][1]) + str(query[0][2])}
		else :
			query = self.query(
				"SELECT ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 FROM input_cube_edge WHERE "
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s) OR "
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s) OR "
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s) OR"
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s) OR "
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s) OR "
				"(ColorPresent_1 = %s AND ColorPresent_2 = %s AND ColorPresent_3 = %s);",
				(piece_name[0], piece_name[1], piece_name[2],
				 piece_name[0], piece_name[2], piece_name[1],
				 piece_name[1], piece_name[0], piece_name[2],
				 piece_name[1], piece_name[2], piece_name[0],
				 piece_name[2], piece_name[0], piece_name[1],
				 piece_name[2], piece_name[1], piece_name[0]))

			result = {'colorcode' : query[0][0],
					  'orientation' : str(query[0][1])+ str(query[0][2])+str(query[0][3])}

		return result


	# 1. Getting the white cross (White Edges) [Solving white Edges]
	def solve_state_one(self, unsolved_cube,string_solved_cube):

		for white_edge in range(4):

			cur_edge = self.cube_edges_col[white_edge]
			result = self.find_piece(unsolved_cube,'E',cur_edge)

			if result['colorcode'][0] is 'W':
				unsolved_cube.make_move(result['colorcode'][1], 'W', 'F')
				unsolved_cube.make_move(result['colorcode'][1], 'W', 'F')
				color_from = result['colorcode'][1]

			elif result['colorcode'][0] is not 'Y':
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'Fi')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'Bi')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'F')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'B')
				color_from = result['colorcode'][0]
			else:
				color_from = result['colorcode'][1]

			#cur_edge[1] - The face we have to move the edge to
			#color_from - The Face we have the edge in

			cur_links = unsolved_cube.switcher_links.get(cur_edge[1])
			rev_cur_links = {v: k for k, v in cur_links.items()}
			dir_move_from = rev_cur_links[color_from]

			# Move into Correct Face
			if(dir_move_from is 'LEFT'):
				unsolved_cube.make_move(cur_edge[1], 'W', 'B')
			elif(dir_move_from is 'BACK'):
				unsolved_cube.make_move(cur_edge[1], 'W', 'B')
				unsolved_cube.make_move(cur_edge[1], 'W', 'B')
			elif(dir_move_from is 'RIGHT'):
				unsolved_cube.make_move(cur_edge[1], 'W', 'Bi')


			y_links = unsolved_cube.switcher_links.get('Y')
			rev_y_links = {v: k for k, v in y_links.items()}
			cur_index = rev_y_links[cur_edge[1]][1]

			if(unsolved_cube.Rubic[cur_edge[1]][cur_index[0]][cur_index[1]]): #Correct Orientation
				unsolved_cube.make_move(cur_edge[1], 'W', 'Fi')
				unsolved_cube.make_move(cur_edge[1], 'W', 'Fi')
			else: #Wrong Orientation
				unsolved_cube.make_move(cur_edge[1], 'W', 'F')
				unsolved_cube.make_move(cur_edge[1], 'W', 'U')
				unsolved_cube.make_move(cur_edge[1], 'W', 'Li')
				unsolved_cube.make_move(cur_edge[1], 'W', 'Ui')






	# # 2. Getting the 1st Layer (All Whites)[Solving White Corners]
	# def solve_state_two(self, unsolved_cube,string_solved_cube):
	#
	#
	# # 3. Getting the second/middle layer (White + 2 columns of 4 sides adj. to white) [Solving 4 Edges]
	# def solve_state_three(self, unsolved_cube,string_solved_cube):
	#
	#
	# # 4. Getting the yellow cross (Yellow Edges) [Solving 4 yellow edges]
	# def solve_state_four(self, unsolved_cube,string_solved_cube):
	#
	#
	# # 5. Getting the Yellow Face (Yellow Face whole) [Solving 4 yellow corners]
	# def solve_state_five(self, unsolved_cube,string_solved_cube):
	#
	#
	# # 6. Getting the third layer corner pieces (Yellow Corners aligned) [Solving yellow Corners wrt. cube]
	# def solve_state_six(self, unsolved_cube,string_solved_cube):
	#
	#
	# # 7. Finishing the cube (All Done) [Solving Yellow Edges wrt. Cube]
	# def solve_state_seven(self, unsolved_cube,string_solved_cube):


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
		state = 1
		counter = 1

		while state != 8 :

			next_state = self.check_state(state,unsolved_cube)

			self.solve_state_main(next_state,unsolved_cube,solution)

			counter = counter + 1
			if counter is 10 :
				print("Error Counter 10")
				return 'E'

		return solution
