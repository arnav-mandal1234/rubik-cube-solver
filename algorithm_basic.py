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

class algorithm():

	solved_cube = Cube()

	def scramble_random(self,cube_scrmbl):

		# perform random scramble

		return cube_scrmbl

	def input_cube(self):

		cube_input = Cube()

		# take input

		return cube_input

	def check_state(self,state_flag,cube_to_check):

		# If ret_flag is 1 then present state is satisfied acc. to state_flag
		ret_flag = 1

		return ret_flag

	def solve_state_one(unsolved_cube,string_solved_cube):
	def solve_state_two(unsolved_cube,string_solved_cube):
	def solve_state_three(unsolved_cube,string_solved_cube):
	def solve_state_four(unsolved_cube,string_solved_cube):
	def solve_state_five(unsolved_cube,string_solved_cube):
	def solve_state_six(unsolved_cube,string_solved_cube):
	def solve_state_seven(unsolved_cube,string_solved_cube):

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

		string solved_cube = "E"

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
		

		return string_solved_cube