# Basic Abstraction of a Rubics Cube and Possible Moves 
# by Arnav Mandal and Ayan Sinha Mahapatra 

import copy

cube_row = 3
cube_column = 3
cube_faces = 6

class Cube:

    Rubic = [[['W' for r in range(cube_row)] for c in range(cube_column)] for f in range(cube_faces)]

    Rubic_R = [['R' for rr in range(cube_row)] for cr in range(cube_column)]
    Rubic[1] = Rubic_R
    Rubic_R_links={'UP':'W','DOWN':'Y','LEFT':'G','RIGHT':'B','FRONT':'R','BACK':'O'}
    Rubic_R_adj = 'WBYGW'
    
    Rubic_W = [['W' for rw in range(cube_row)] for cw in range(cube_column)]
    Rubic[0] = Rubic_W
    Rubic_W_links={'UP':'B','DOWN':'G','LEFT':'O','RIGHT':'R','FRONT':'W','BACK':'Y'}
    Rubic_W_adj = 'BRGOB'

    Rubic_R = [['R' for rr in range(cube_row)] for cr in range(cube_column)]
    Rubic[1] = Rubic_R
    Rubic_R_links={'UP':'W','DOWN':'Y','LEFT':'G','RIGHT':'B','FRONT':'R','BACK':'O'}
    Rubic_R_adj = 'WBYGW'

    Rubic_G = [['G' for rg in range(cube_row)] for cg in range(cube_column)]
    Rubic[2] = Rubic_G
    Rubic_G_links={'UP':'W','DOWN':'Y','LEFT':'O','RIGHT':'R','FRONT':'G','BACK':'B'}
    Rubic_G_adj = 'WRYOW'

    Rubic_O = [['O' for ro in range(cube_row)] for co in range(cube_column)]
    Rubic[3] = Rubic_O
    Rubic_O_links={'UP':'Y','DOWN':'W','LEFT':'G','RIGHT':'B','FRONT':'O','BACK':'R'}
    Rubic_O_adj = 'YBWGY'

    Rubic_B = [['B' for rb in range(cube_row)] for cb in range(cube_column)]
    Rubic[4] = Rubic_B
    Rubic_B_links={'UP':'Y','DOWN':'W','LEFT':'O','RIGHT':'R','FRONT':'B','BACK':'G'}
    Rubic_B_adj = 'YRWOY'

    Rubic_Y = [['Y' for ry in range(cube_row)] for cy in range(cube_column)]
    Rubic[5] = Rubic_Y
    Rubic_Y_links={'UP':'G','DOWN':'B','LEFT':'O','RIGHT':'R','FRONT':'Y','BACK':'W'}
    Rubic_Y_adj = 'GRBOG'

    move_center = [['E' for rm in range(cube_row)] for cm in range(cube_column)]
    move_side = [['E' for rms in range(cube_row)] for cms in range(cube_column+1)]
    move_ref = {'UP':'E','DOWN':'E','LEFT':'E','RIGHT':'E','FRONT' : 'E','BACK' : 'E'}
    move_center_id = 'E'
    move_dir = 'E'
    move_conversion = {'U':'UP','D':'DOWN','L':'LEFT','R':'RIGHT','F':'FRONT','B':'BACK'}

    move_side_index = [[[ 5 for x in range(2)] for y in range(3)] for z in range(4)]

    rubic_switcher = {
            'W': 0,
            'R': 1,
            'G': 2,
            'O': 3,
            'B': 4,
            'Y': 5,
    }

    index_switcher = {
            'UP'    : [[0,2], [0,1], [0,0]],
            'RIGHT' : [[2,2], [1,2], [0,2]],
            'DOWN'  : [[2,0], [2,1], [2,2]],
            'LEFT'  : [[0,0], [1,0], [2,0]],
    }

    switcher_adj = {
            'W': Rubic_W_adj,
            'R': Rubic_R_adj,
            'G': Rubic_G_adj,
            'O': Rubic_O_adj,
            'B': Rubic_B_adj,
            'Y': Rubic_Y_adj,
    }

    switcher_links = {
            'W': Rubic_W_links,
            'R': Rubic_R_links,
            'G': Rubic_G_links,
            'O': Rubic_O_links,
            'B': Rubic_B_links,
            'Y': Rubic_Y_links,
    }

    switcher_order_side= {
            0 : 'UP',
            1 : 'RIGHT',
            2 : 'DOWN',
            3 : 'LEFT',
    }

    cent_index = [[2, 0, 0, 0], [1, 0, 0, 1], [0, 0, 0, 2], [0, 1, 1, 2], [0, 2, 2, 2],
                  [1, 2, 2, 1], [2, 2, 2, 0], [2, 1, 1, 0], [1, 1, 1, 1]]


    def print_Cube(self):

        for sides in range(6):
            print(self.Rubic[sides][0])
            print(self.Rubic[sides][1])
            print(self.Rubic[sides][2])
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


    def get_right_or_left_center_block(self,request ,ref_center, ref_up_center):

        right_center = 'E'
        left_center = 'E'
        adj_squares = self.switcher_adj.get(ref_center, "E")

        for elements in range(5):
            if ref_up_center is adj_squares[elements]:
                right_center = adj_squares[elements + 1]
                if elements is 0:
                    left_center = adj_squares[3]
                else:
                    left_center = adj_squares[elements - 1]
                break
        if request is 'RIGHT':
            return right_center
        elif request is 'LEFT':
            return left_center


    def update_move_ref(self):

        links_sides = self.switcher_links.get(self.move_center_id, "E")
        self.move_ref['FRONT'] = links_sides['FRONT']
        self.move_ref['BACK']  = links_sides['BACK']
        self.move_ref['UP']    = links_sides['UP']
        self.move_ref['DOWN']  = links_sides['DOWN']
        self.move_ref['LEFT']  = links_sides['LEFT']
        self.move_ref['RIGHT'] = links_sides['RIGHT']

    def perform_move_center(self):

        rubic_select = self.rubic_switcher.get(self.move_center_id, "E")
        self.move_center = copy.deepcopy(self.Rubic[rubic_select])

        if (self.move_dir is 'A'):
            for index in range(0, 9):
                self.Rubic[rubic_select][self.cent_index[index][0]][self.cent_index[index][1]] = self.move_center[self.cent_index[index][2]][self.cent_index[index][3]]
        elif (self.move_dir is 'C'):
            for index in range(0, 9):
                self.Rubic[rubic_select][self.cent_index[index][2]][self.cent_index[index][3]] = self.move_center[self.cent_index[index][0]][self.cent_index[index][1]]


    def find_rev_corr(self,curr_side_col,ref_side):

        ref_col = self.move_ref[ref_side]
        ref_links = self.switcher_links.get(ref_col, "E")
        ref_inv_links = {v: k for k, v in ref_links.items()}
        corr_ret = ref_inv_links[curr_side_col]

        return corr_ret


    def get_move_side_index(self):

        curr_side_col = self.move_center_id

        for side in range(4):
            ref_side = self.switcher_order_side.get(side, "E")
            corr = self.find_rev_corr(curr_side_col,ref_side)

            self.move_side_index[side] = self.index_switcher.get(corr, "E")

    def perform_move_sides(self):

        self.get_move_side_index()

        # Move from Cube by using move_side_index to move_sides
        for side in range(4):
            for loc in range(3):
                rubic_col_index = self.rubic_switcher.get(self.move_ref[self.switcher_order_side.get(side, "E")], "E")
                self.move_side[side][loc] = self.Rubic[rubic_col_index][self.move_side_index[side][loc][0]][self.move_side_index[side][loc][1]]

        # Move from move_sides to Cube by using move_side_index
        if(self.move_dir is 'C'):
            for side in range(4):
                for loc in range(3):
                    clockwise_rotation = (side + 1) % 4
                    rubic_col_index = self.rubic_switcher.get(self.move_ref[self.switcher_order_side.get(clockwise_rotation, "E")], "E")
                    self.Rubic[rubic_col_index][self.move_side_index[clockwise_rotation][loc][0]][self.move_side_index[clockwise_rotation][loc][1]] = self.move_side[side][loc]

        elif(self.move_dir is 'A'):
            for side in range(4):
                for loc in range(3):
                    anticlockwise_rotation = (side + 3) % 4
                    rubic_col_index = self.rubic_switcher.get(self.move_ref[self.switcher_order_side.get(anticlockwise_rotation, "E")], "E")
                    self.Rubic[rubic_col_index][self.move_side_index[anticlockwise_rotation][loc][0]][self.move_side_index[anticlockwise_rotation][loc][1]] = self.move_side[side][loc]

    def make_move(self,ref_center,ref_up_center,move_id_given):

        # The Main Function where the move is perform
        self.move_dir = 'C'
        move_id_make = move_id_given[0]

        if len(move_id_given) is 2:
            self.move_dir = 'A'

        self.move_ref['FRONT'] = ref_center
        self.move_ref['BACK']  = self.get_opp_center_block(ref_center)
        self.move_ref['UP']    = ref_up_center
        self.move_ref['DOWN']  = self.get_opp_center_block(ref_up_center)
        self.move_ref['LEFT']  = self.get_right_or_left_center_block('LEFT', ref_center,ref_up_center)
        self.move_ref['RIGHT'] = self.get_right_or_left_center_block('RIGHT', ref_center,ref_up_center)

        self.move_center_id = self.move_ref[self.move_conversion[move_id_make]]

        self.update_move_ref()

        self.perform_move_center()

        self.perform_move_sides()
