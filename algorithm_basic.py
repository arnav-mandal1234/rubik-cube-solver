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

		scramble = "RLDBDLRUDFRLFBUBDFLBDUBBDFFUBUBFDRL"
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
				"SELECT ColorCode, ColorPresent_1, ColorPresent_2, ColorPresent_3 FROM input_cube_corner WHERE "
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
			result = self.find_piece(unsolved_cube, 'E', cur_edge)
			color_to = cur_edge[1]

			if result['colorcode'][0] == 'W':
				unsolved_cube.make_move(result['colorcode'][1], 'W', 'F')
				unsolved_cube.make_move(result['colorcode'][1], 'W', 'F')
				color_from = result['colorcode'][1]

			elif result['colorcode'][0] != 'Y':
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'Fi')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'Di')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'F')
				unsolved_cube.make_move(result['colorcode'][0], 'W', 'D')
				color_from = result['colorcode'][0]

			else:
				color_from = result['colorcode'][1]

			#color_to - The face we have to move the edge to
			#color_from - The Face we have the edge in

			# Move into Correct Face
			if(unsolved_cube.get_right_or_left_center_block('LEFT',color_from,'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'Di')

			elif(unsolved_cube.get_opp_center_block(color_from) == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')
				unsolved_cube.make_move(color_to, 'W', 'D')

			elif(unsolved_cube.get_right_or_left_center_block('RIGHT',color_from,'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')

			y_links = unsolved_cube.switcher_links.get('Y')
			rev_y_links = {v: k for k, v in y_links.items()}
			cur_dir = rev_y_links[color_to]
			cur_index = unsolved_cube.index_switcher.get(cur_dir)

			# Correct Orientation
			if(unsolved_cube.Rubic[unsolved_cube.rubic_switcher.get('Y')][cur_index[1][0]][cur_index[1][1]] == 'W'):
				unsolved_cube.make_move(color_to, 'W', 'Fi')
				unsolved_cube.make_move(color_to, 'W', 'Fi')

			# Wrong Orientation
			else:
				unsolved_cube.make_move(color_to, 'W', 'F')
				unsolved_cube.make_move(color_to, 'W', 'U')
				unsolved_cube.make_move(color_to, 'W', 'Li')
				unsolved_cube.make_move(color_to, 'W', 'Ui')

			self.update_db_from_cube(unsolved_cube,'E')




	# 2. Getting the 1st Layer (All Whites)[Solving White Corners]
	def solve_state_two(self, unsolved_cube, string_solved_cube):

		for white_corner in range(4):

			cur_corner = self.cube_corners_col[white_corner]
			result = self.find_piece(unsolved_cube, 'C', cur_corner)
			color_to = cur_corner[2]
			color_from = result['colorcode'][2]

			if result['colorcode'][0] == 'W':
				unsolved_cube.make_move(color_from, 'W', 'Ri')
				unsolved_cube.make_move(color_from, 'W', 'D')
				unsolved_cube.make_move(color_from, 'W', 'R')

			# Move into Correct Face
			if (unsolved_cube.get_right_or_left_center_block('LEFT', color_from, 'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'Di')

			elif (unsolved_cube.get_opp_center_block(color_from) == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')
				unsolved_cube.make_move(color_to, 'W', 'D')

			elif (unsolved_cube.get_right_or_left_center_block('RIGHT', color_from, 'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')

			unsolved_cube.make_move(color_to, 'W', 'Ri')
			unsolved_cube.make_move(color_to, 'W', 'Di')
			unsolved_cube.make_move(color_to, 'W', 'R')

			w_links = unsolved_cube.switcher_links.get('W')
			rev_w_links = {v: k for k, v in w_links.items()}
			cur_dir = rev_w_links[color_to]
			cur_index = unsolved_cube.index_switcher.get(cur_dir)

			# Correct Orientation
			while (unsolved_cube.Rubic[unsolved_cube.rubic_switcher.get('W')][cur_index[2][0]][cur_index[2][1]] != 'W'):
				unsolved_cube.make_move(color_to, 'W', 'Ri')
				unsolved_cube.make_move(color_to, 'W', 'Di')
				unsolved_cube.make_move(color_to, 'W', 'R')
				unsolved_cube.make_move(color_to, 'W', 'D')
				unsolved_cube.make_move(color_to, 'W', 'Ri')
				unsolved_cube.make_move(color_to, 'W', 'Di')
				unsolved_cube.make_move(color_to, 'W', 'R')

			self.update_db_from_cube(unsolved_cube, 'C')


	# 3. Getting the second/middle layer (White + 2 columns of 4 sides adj. to white) [Solving 4 Edges]
	def solve_state_three(self, unsolved_cube,string_solved_cube):

		for mid_edge in range(4):

			cur_edge = self.cube_edges_col[mid_edge + 4]
			result = self.find_piece(unsolved_cube, 'E', cur_edge)
			color_to = cur_edge[0]
			color_from = result['colorcode'][1]
			dir_rotate = 'L'

			if result['colorcode'][0] != 'Y':
				unsolved_cube.make_move(color_from, 'Y', 'Ui')
				unsolved_cube.make_move(color_from, 'Y', 'Li')
				unsolved_cube.make_move(color_from, 'Y', 'U')
				unsolved_cube.make_move(color_from, 'Y', 'L')
				unsolved_cube.make_move(color_from, 'Y', 'U')
				unsolved_cube.make_move(color_from, 'Y', 'F')
				unsolved_cube.make_move(color_from, 'Y', 'Ui')
				unsolved_cube.make_move(color_from, 'Y', 'Fi')
				unsolved_cube.make_move(color_from, 'Y', 'U')
				unsolved_cube.make_move(color_from, 'Y', 'U')

			if (unsolved_cube.get_right_or_left_center_block('LEFT', color_from, 'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'Di')

			elif (unsolved_cube.get_opp_center_block(color_from) == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')
				unsolved_cube.make_move(color_to, 'W', 'D')

			elif (unsolved_cube.get_right_or_left_center_block('RIGHT', color_from, 'W') == color_to):
				unsolved_cube.make_move(color_to, 'W', 'D')

			y_links = unsolved_cube.switcher_links.get('Y')
			rev_y_links = {v: k for k, v in y_links.items()}
			cur_dir = rev_y_links[color_to]
			cur_index = unsolved_cube.index_switcher.get(cur_dir)

			# Correct Orientation
			if (unsolved_cube.Rubic[unsolved_cube.rubic_switcher.get('Y')][cur_index[1][0]][cur_index[1][1]] == color_to):
				unsolved_cube.make_move(color_from, 'Y', 'Ui')
				color_to = cur_edge[1]
				dir_rotate = 'R'

			if dir_rotate == 'L':
				unsolved_cube.make_move(color_to, 'Y', 'U')
				unsolved_cube.make_move(color_to, 'Y', 'R')
				unsolved_cube.make_move(color_to, 'Y', 'Ui')
				unsolved_cube.make_move(color_to, 'Y', 'Ri')
				unsolved_cube.make_move(color_to, 'Y', 'Ui')
				unsolved_cube.make_move(color_to, 'Y', 'Fi')
				unsolved_cube.make_move(color_to, 'Y', 'U')
				unsolved_cube.make_move(color_to, 'Y', 'F')

			else :
				unsolved_cube.make_move(color_to, 'Y', 'Ui')
				unsolved_cube.make_move(color_to, 'Y', 'Li')
				unsolved_cube.make_move(color_to, 'Y', 'U')
				unsolved_cube.make_move(color_to, 'Y', 'L')
				unsolved_cube.make_move(color_to, 'Y', 'U')
				unsolved_cube.make_move(color_to, 'Y', 'F')
				unsolved_cube.make_move(color_to, 'Y', 'Ui')
				unsolved_cube.make_move(color_to, 'Y', 'Fi')

			self.update_db_from_cube(unsolved_cube, 'E')


	# 4. Getting the yellow cross (Yellow Edges) [Solving 4 yellow edges]
	def solve_state_four(self, unsolved_cube,string_solved_cube):

		# None of Yellow Faces of Edge piece in place
		if ( ( unsolved_cube.Rubic[5][0][1] != 'Y' ) and ( unsolved_cube.Rubic[5][1][0] != 'Y' ) and ( unsolved_cube.Rubic[5][2][1] != 'Y' ) and ( unsolved_cube.Rubic[5][1][2] != 'Y' ) ) :
			self.moves_state_four_first(unsolved_cube, string_solved_cube, 'R')

		if ( ( unsolved_cube.Rubic[5][0][1] == 'Y' ) and ( unsolved_cube.Rubic[5][2][1] == 'Y' ) ):
			self.moves_state_four_second(unsolved_cube, string_solved_cube, 'R')

		elif ( ( unsolved_cube.Rubic[5][1][0] == 'Y' )  and ( unsolved_cube.Rubic[5][1][2] == 'Y' ) ):
			self.moves_state_four_second(unsolved_cube, string_solved_cube, 'B')

		# State 4
		elif ((unsolved_cube.Rubic[5][0][1] == 'Y') and (unsolved_cube.Rubic[5][1][0] == 'Y')):
			self.moves_state_four_first(unsolved_cube, string_solved_cube, 'B')

		elif ((unsolved_cube.Rubic[5][1][0] == 'Y') and (unsolved_cube.Rubic[5][2][1] == 'Y')):
			self.moves_state_four_first(unsolved_cube, string_solved_cube, 'R')

		elif ((unsolved_cube.Rubic[5][2][1] == 'Y') and (unsolved_cube.Rubic[5][1][2] == 'Y')):
			self.moves_state_four_first(unsolved_cube, string_solved_cube, 'G')
			unsolved_cube.make_move('G', 'Y', 'Fi')

		elif ((unsolved_cube.Rubic[5][1][2] == 'Y') and (unsolved_cube.Rubic[5][0][1] == 'Y')):
			self.moves_state_four_first(unsolved_cube, string_solved_cube, 'O')
		
		self.update_db_from_cube(unsolved_cube, 'E')
		return

	# 5. Getting the Yellow Face (Yellow Face whole) [Solving 4 yellow corners]
	def solve_state_five(self, unsolved_cube, string_solved_cube):

		while(self.check_state_five(unsolved_cube) == False):

			if unsolved_cube.Rubic[5][0][0] != 'Y' and unsolved_cube.Rubic[5][2][0] != 'Y' and unsolved_cube.Rubic[5][2][2] != 'Y' and unsolved_cube.Rubic[5][0][2] != 'Y':

				if unsolved_cube.Rubic[1][2][0] == 'Y':
					ref_center = 'G'
				elif unsolved_cube.Rubic[2][2][0] == 'Y':
					ref_center = 'O'
				elif unsolved_cube.Rubic[3][0][2] == 'Y':
					ref_center = 'B'
				elif unsolved_cube.Rubic[4][0][2] == 'Y':
					ref_center = 'R'

			elif self.corners_with_yellow_count(unsolved_cube) == 2:

				if unsolved_cube.Rubic[1][2][2] == 'Y':
					ref_center = 'R'
				elif unsolved_cube.Rubic[2][2][2] == 'Y':
					ref_center = 'G'
				elif unsolved_cube.Rubic[3][0][0] == 'Y':
					ref_center = 'O'
				elif unsolved_cube.Rubic[4][0][0] == 'Y':
					ref_center = 'B'

			elif unsolved_cube.Rubic[5][2][0] == 'Y':
				ref_center = 'B'

			elif unsolved_cube.Rubic[5][0][0] == 'Y':
				ref_center = 'O'

			elif unsolved_cube.Rubic[5][0][2]== 'Y':
				ref_center = 'G'

			elif unsolved_cube.Rubic[5][2][2] == 'Y':
				ref_center = 'R'

			self.moves_state_five(unsolved_cube, string_solved_cube, ref_center)
			self.update_db_from_cube(unsolved_cube, 'E')
			self.update_db_from_cube(unsolved_cube, 'C')

		return

	# 6. Getting the third layer corner pieces (Yellow Corners aligned) [Solving yellow Corners wrt. cube]
	def solve_state_six(self, unsolved_cube,string_solved_cube):

		# Rotates till we get two corners right and returns if they are at Diagonals or at same face
		back_side, cube_state = self.get_two_corner_correct(unsolved_cube)

		#If already has correct corner pieces, return
		if (cube_state == 'S'):
			return

		# If they are at Diagonals get two corners at same face
		if(cube_state == 'D'):
			self.moves_state_six(unsolved_cube, string_solved_cube, 'R')
			back_side, cube_state = self.get_two_corner_correct(unsolved_cube)

		front_side = unsolved_cube.get_opp_center_block(back_side)

		self.moves_state_six(unsolved_cube, string_solved_cube, front_side)
		self.update_db_from_cube(unsolved_cube, 'E')
		self.update_db_from_cube(unsolved_cube, 'C')

		#unsolved_cube.print_Cube()

		return

	# 7. Finishing the cube (All Done) [Solving Yellow Edges wrt. Cube]
	def solve_state_seven(self, unsolved_cube,string_solved_cube):

		# If 4 edges are incorrect, Do this sequence to get one correct edge
		if(self.state_seven_edges_incorrect(unsolved_cube, 'num') == 4):
			self.moves_state_seven(unsolved_cube, string_solved_cube, 'R', 'C')

		# Get the Front Facing Side for Remaining Moves (Opp Correct Edge)
		back_side = self.state_seven_edges_incorrect(unsolved_cube, 'side')
		front_side = unsolved_cube.get_opp_center_block(back_side)

		# Get which direction to rotate and then do respective sequences
		if(self.get_dir_rotate_state_seven(unsolved_cube, front_side) == 'C'):
			self.moves_state_seven(unsolved_cube, string_solved_cube, front_side, 'C')
		else:
			self.moves_state_seven(unsolved_cube, string_solved_cube, front_side, 'A')

		self.update_db_from_cube(unsolved_cube, 'E')
		self.update_db_from_cube(unsolved_cube, 'C')

		return

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

	def moves_state_four_first(self, unsolved_cube, string_solved_cube, ref_center):

		unsolved_cube.make_move(ref_center, 'Y', 'F')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'R')
		unsolved_cube.make_move(ref_center, 'Y', 'Ui')
		unsolved_cube.make_move(ref_center, 'Y', 'Ri')
		unsolved_cube.make_move(ref_center, 'Y', 'Fi')

		return

	def moves_state_four_second(self, unsolved_cube, string_solved_cube, ref_center):

		unsolved_cube.make_move(ref_center, 'Y', 'F')
		unsolved_cube.make_move(ref_center, 'Y', 'R')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'Ri')
		unsolved_cube.make_move(ref_center, 'Y', 'Ui')
		unsolved_cube.make_move(ref_center, 'Y', 'Fi')

		return

	def moves_state_five(self, unsolved_cube, string_solved_cube, ref_center):

		unsolved_cube.make_move(ref_center, 'Y', 'R')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'Ri')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'R')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'U')
		unsolved_cube.make_move(ref_center, 'Y', 'Ri')

		return

	def moves_state_six(self, unsolved_cube, string_solved_cube, front_side):

		unsolved_cube.make_move(front_side, 'Y', 'Ri')
		unsolved_cube.make_move(front_side, 'Y', 'F')
		unsolved_cube.make_move(front_side, 'Y', 'Ri')
		unsolved_cube.make_move(front_side, 'Y', 'B')
		unsolved_cube.make_move(front_side, 'Y', 'B')
		unsolved_cube.make_move(front_side, 'Y', 'R')
		unsolved_cube.make_move(front_side, 'Y', 'Fi')
		unsolved_cube.make_move(front_side, 'Y', 'Ri')
		unsolved_cube.make_move(front_side, 'Y', 'B')
		unsolved_cube.make_move(front_side, 'Y', 'B')
		unsolved_cube.make_move(front_side, 'Y', 'R')
		unsolved_cube.make_move(front_side, 'Y', 'R')
		unsolved_cube.make_move(front_side, 'Y', 'Ui')

		return

	def moves_state_seven(self, unsolved_cube, string_solved_cube, front_side, dir):

		if dir == 'A':
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'U')
			unsolved_cube.make_move(front_side, 'Y', 'L')
			unsolved_cube.make_move(front_side, 'Y', 'Ri')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'Li')
			unsolved_cube.make_move(front_side, 'Y', 'R')
			unsolved_cube.make_move(front_side, 'Y', 'U')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')
		else:
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'Ui')
			unsolved_cube.make_move(front_side, 'Y', 'L')
			unsolved_cube.make_move(front_side, 'Y', 'Ri')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'Li')
			unsolved_cube.make_move(front_side, 'Y', 'R')
			unsolved_cube.make_move(front_side, 'Y', 'Ui')
			unsolved_cube.make_move(front_side, 'Y', 'F')
			unsolved_cube.make_move(front_side, 'Y', 'F')

		return

	def corners_with_yellow_count(self, unsolved_cube):

		count = 0;

		if unsolved_cube.Rubic[5][0][0] == 'Y':
			count += 1
		if unsolved_cube.Rubic[5][2][0] == 'Y':
			count += 1
		if unsolved_cube.Rubic[5][2][2] == 'Y':
			count += 1
		if unsolved_cube.Rubic[5][0][2] == 'Y':
			count += 1

		return count

	def get_two_corner_correct(self, unsolved_cube):

		count = 0

		while(1):
			
			back_side, cube_state = self.two_yellow_cor_correct(unsolved_cube)
			
			if (back_side != 'E') or (cube_state == 'S'):
				break

			if (count == 4):
				print("Error at Get Two Corner Correct")
			
			unsolved_cube.make_move('R', 'Y', 'U')
			count += 1

		return back_side, cube_state

	def two_yellow_cor_correct(self, unsolved_cube):

		back_side = 'E'
		cube_state = 'E'
		correct_corners = 0
		corner_string = ''
		correct_corner_index = ['N' for i in range(4)]

		if ( unsolved_cube.Rubic[1][2][0] == 'R' ) and ( unsolved_cube.Rubic[2][2][2] == 'G' ):
			correct_corners += 1
			correct_corner_index[0] = 'Y'

		if ( unsolved_cube.Rubic[2][2][0] == 'G' ) and ( unsolved_cube.Rubic[3][0][0] == 'O' ):
			correct_corners += 1
			correct_corner_index[1] = 'Y'

		if ( unsolved_cube.Rubic[3][0][2] == 'O' ) and ( unsolved_cube.Rubic[4][0][0] == 'B' ):
			correct_corners += 1
			correct_corner_index[2] = 'Y'

		if ( unsolved_cube.Rubic[4][2][0] == 'B' ) and ( unsolved_cube.Rubic[1][2][2] == 'R' ):
			correct_corners += 1
			correct_corner_index[3] = 'Y'

		if(correct_corners < 2):
			return back_side, cube_state
		elif(correct_corners == 4):
			cube_state = 'S'
			return back_side, cube_state
		else:
			if ((correct_corner_index[0] == 'Y') and (correct_corner_index[2] == 'Y')) or ((correct_corner_index[1] == 'Y') and (correct_corner_index[3] == 'Y')):
				cube_state = 'D'
				back_side = 'R' 
			elif (correct_corner_index[0] == 'Y') and (correct_corner_index[1] == 'Y'):
				back_side = 'G'
			elif (correct_corner_index[1] == 'Y') and (correct_corner_index[2] == 'Y'):
				back_side = 'O'
			elif (correct_corner_index[2] == 'Y') and (correct_corner_index[3] == 'Y'):
				back_side = 'B'
			elif (correct_corner_index[3] == 'Y') and (correct_corner_index[0] == 'Y'):
				back_side = 'R'

		return back_side, cube_state

	def state_seven_edges_incorrect(self, unsolved_cube, request):

		incorrect_edges = 0
		back_side = 'E'

		if(unsolved_cube.Rubic[1][2][1] != 'R'):
			incorrect_edges += 1
		else:
			back_side = 'R'
		
		if(unsolved_cube.Rubic[2][2][1] != 'G'):
			incorrect_edges += 1
		else:
			back_side = 'G'
		
		if(unsolved_cube.Rubic[3][0][1] != 'O'):
			incorrect_edges += 1
		else:
			back_side = 'O'
		
		if(unsolved_cube.Rubic[4][0][1] != 'B'):
			incorrect_edges += 1
		else:
			back_side = 'B'

		if request == 'num':
			return incorrect_edges
		else:
			return back_side

	def get_dir_rotate_state_seven(self, unsolved_cube, front_side):

		left_side = unsolved_cube.rubic_switcher.get(unsolved_cube.get_right_or_left_center_block('LEFT', front_side, 'Y'), "E")

		if (left_side == 'B') or (left_side == 'O'):
			left_edge_current = unsolved_cube.Rubic[left_side][0][1]
		else:
			left_edge_current = unsolved_cube.Rubic[left_side][2][1]

		if left_edge_current == front_side :
			direction = 'C'
		else:
			direction = 'A'

		return direction