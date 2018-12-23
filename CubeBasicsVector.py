cube_row = 3
cube_column = 3

class Cube:

    Rubic_W = [['W' for rw in range(cube_row)] for cw in range(cube_column)]
    Rubic_W_links={'UP':'B','DOWN':'G','LEFT':'O','RIGHT':'R','FRONT':'W','BACK':'Y'}
    Rubic_W_adj = 'BRGOB'

    Rubic_R = [['R' for rr in range(cube_row)] for cr in range(cube_column)]
    Rubic_R_links={'UP':'W','DOWN':'Y','LEFT':'G','RIGHT':'B','FRONT':'R','BACK':'O'}
    Rubic_R_adj = 'WBYGW'

    Rubic_G = [['G' for rg in range(cube_row)] for cg in range(cube_column)]
    Rubic_G_links={'UP':'W','DOWN':'Y','LEFT':'O','RIGHT':'R','FRONT':'G','BACK':'B'}
    Rubic_G_adj = 'WRYOW'

    Rubic_O = [['O' for ro in range(cube_row)] for co in range(cube_column)]
    Rubic_O_links={'UP':'Y','DOWN':'W','LEFT':'G','RIGHT':'B','FRONT':'O','BACK':'R'}
    Rubic_O_adj = 'YBWGW'

    Rubic_B = [['B' for rb in range(cube_row)] for cb in range(cube_column)]
    Rubic_B_links={'UP':'Y','DOWN':'W','LEFT':'O','RIGHT':'R','FRONT':'B','BACK':'G'}
    Rubic_B_adj = 'YRWOY'

    Rubic_Y = [['Y' for ry in range(cube_row)] for cy in range(cube_column)]
    Rubic_Y_links={'UP':'G','DOWN':'B','LEFT':'O','RIGHT':'R','FRONT':'Y','BACK':'W'}
    Rubic_Y_adj = 'GRBOG'

    move_center = [['E' for rm in range(cube_row)] for cm in range(cube_column)]
    move_side = [['E' for rms in range(cube_row)] for cms in range(cube_column+1)]
    move_ref = {'UP':'E','DOWN':'E','LEFT':'E','RIGHT':'E','FRONT' : 'E','BACK' : 'E'}
    move_center_id = 'E'
    move_dir = 'E'
    move_conversion = {'U':'UP','D':'DOWN','L':'LEFT','R':'RIGHT','F':'FRONT','B':'BACK'}

    def print_Cube(self):

        print(self.Rubic_W[0]); print(self.Rubic_W[1]); print(self.Rubic_W[2])
        print("\n")
        print(self.Rubic_R[0]); print(self.Rubic_R[1]); print(self.Rubic_R[2])
        print("\n")
        print(self.Rubic_G[0]); print(self.Rubic_G[1]); print(self.Rubic_G[2])
        print("\n")
        print(self.Rubic_O[0]); print(self.Rubic_O[1]); print(self.Rubic_O[2])
        print("\n")
        print(self.Rubic_B[0]); print(self.Rubic_B[1]); print(self.Rubic_B[2])
        print("\n")
        print(self.Rubic_Y[0]); print(self.Rubic_Y[1]); print(self.Rubic_Y[2])
        print("\n")


    def get_opp_center_block(self,center_block_id):

        switcher = {
            'W': 'Y',
            'R': 'O',
            'G': 'B',
            'O': 'R',
            'B': 'G',
            'Y': 'W',
        }

        return switcher.get(center_block_id, "E")


    def get_right_or_left_center_block(self,request ,ref_center,ref_up_center):

        right_center = 'E'
        left_center = 'E'
        switcher = {
            'W': Cube.Rubic_W_adj,
            'R': Cube.Rubic_R_adj,
            'G': Cube.Rubic_G_adj,
            'O': Cube.Rubic_O_adj,
            'B': Cube.Rubic_B_adj,
            'Y': Cube.Rubic_Y_adj,
        }
        adj_squares = switcher.get(ref_center, "E")
        for elements in range(5):
            if ref_up_center is adj_squares[elements]:
                right_center = adj_squares[elements + 1]
                left_center = adj_squares[elements - 1]
                if elements is 0:
                    left_center = adj_squares[3]
                break
        if request is 'RIGHT':
            return right_center
        elif request is 'LEFT':
            return left_center


    def make_move(self,ref_center,ref_up_center,move_id_given):

		self.move_ref['FRONT'] = ref_center
		self.move_ref['BACK'] = get_opp_center_block(self,ref_center)
		self.move_ref['UP'] = ref_up_center
		self.move_ref['DOWN'] = get_opp_center_block(self,ref_up_center)
		self.move_ref['LEFT'] = get_right_or_left_center_block(self,'LEFT',ref_center,ref_up_center)
		self.move_ref['RIGHT'] = get_right_or_left_center_block(self,'RIGHT',ref_center,ref_up_center)

		self.move_dir = 'C'
		move_id_make = move_id_given[0]

		if len(move_id_given) is 2:
    		self.move_dir = 'A'

    	if ref_center is 'W': 
    		self.move_center_id = self.Rubic_W_links[self.move_conversion[move_id_make]]
    	elif ref_center is 'R':
    		self.move_center_id = self.Rubic_R_links[self.move_conversion[move_id_make]]
    	elif ref_center is 'G':
    		self.move_center_id = self.Rubic_G_links[self.move_conversion[move_id_make]]
    	elif ref_center is 'O':
    		self.move_center_id = self.Rubic_O_links[self.move_conversion[move_id_make]]
    	elif ref_center is 'B':
    		self.move_center_id = self.Rubic_B_links[self.move_conversion[move_id_make]]
    	elif ref_center is 'Y':
    		self.move_center_id = self.Rubic_Y_links[self.move_conversion[move_id_make]]

		prepare_move_pieces(self)

		perform_move(self)


    def prepare_move_pieces(self):
    	



    def perform_move(self):





