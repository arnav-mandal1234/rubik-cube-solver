cube_row = 3
cube_column = 3

class Cube:

    Rubic_W = [['W' for rw in range(cube_row)] for cw in range(cube_column)]
    Rubic_W_links={'UP':'R','DOWN':'O','LEFT':'B','RIGHT':'G'}
    Rubic_W_adj = 'RGOBR'

    Rubic_R = [['R' for rr in range(cube_row)] for cr in range(cube_column)]
    Rubic_R_links={'UP':'Y','DOWN':'W','LEFT':'B','RIGHT':'G'}
    Rubic_R_adj = 'WBYGW'

    Rubic_G = [['G' for rg in range(cube_row)] for cg in range(cube_column)]
    Rubic_G_links={'UP':'R','DOWN':'O','LEFT':'W','RIGHT':'Y'}
    Rubic_G_adj = 'WRYOW'

    Rubic_O = [['O' for ro in range(cube_row)] for co in range(cube_column)]
    Rubic_O_links={'UP':'W','DOWN':'Y','LEFT':'B','RIGHT':'G'}
    Rubic_O_adj = 'WGYBW'

    Rubic_B = [['B' for rb in range(cube_row)] for cb in range(cube_column)]
    Rubic_B_links={'UP':'R','DOWN':'O','LEFT':'Y','RIGHT':'W'}
    Rubic_B_adj = 'WOYRW'

    Rubic_Y = [['Y' for ry in range(cube_row)] for cy in range(cube_column)]
    Rubic_Y_links={'UP':'O','DOWN':'R','LEFT':'B','RIGHT':'G'}
    Rubic_Y_adj = 'RBOBR'

    rotating_list_upper=['W','W','W','W','W','W','W','W',]

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

    def get_center_block(self,move_id,ref_center,ref_up_center):
        switcher = {
            'UP'    :  ref_up_center,
            'DOWN'  :  Cube.get_opp_center_block(self,ref_up_center),
            'FRONT' :  ref_center,
            'BACK'  :  Cube.get_opp_center_block(self,ref_center),
            'LEFT'  :  Cube.get_right_or_left_center_block(self,'LEFT' ,ref_center,ref_up_center),
            'RIGHT' :  Cube.get_right_or_left_center_block(self,'RIGHT' ,ref_center,ref_up_center),
        }
        return switcher.get(move_id, "E")

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

    def get_chars_to_rotate_upper(self,center_block):

        if center_block is 'W':
            Cube.rotating_list_upper = [self.Rubic_W[0][1], self.Rubic_W[0][2],
                                        self.Rubic_W[1][2], self.Rubic_W[2][2],
                                        self.Rubic_W[2][1], self.Rubic_W[2][0],
                                        self.Rubic_W[1][0], self.Rubic_W[0][0], ]
        elif center_block is 'R':
            Cube.rotating_list_upper = [self.Rubic_R[0][1], self.Rubic_R[0][2],
                                        self.Rubic_R[1][2], self.Rubic_R[2][2],
                                        self.Rubic_R[2][1], self.Rubic_R[2][0],
                                        self.Rubic_R[1][0], self.Rubic_R[0][0], ]
        elif center_block is 'G':
            Cube.rotating_list_upper = [self.Rubic_G[0][1], self.Rubic_G[0][2],
                                        self.Rubic_G[1][2], self.Rubic_G[2][2],
                                        self.Rubic_G[2][1], self.Rubic_G[2][0],
                                        self.Rubic_G[1][0], self.Rubic_G[0][0], ]
        elif center_block is 'O':
            Cube.rotating_list_upper = [self.Rubic_O[0][1], self.Rubic_O[0][2],
                                        self.Rubic_O[1][2], self.Rubic_O[2][2],
                                        self.Rubic_O[2][1], self.Rubic_O[2][0],
                                        self.Rubic_O[1][0], self.Rubic_O[0][0], ]
        elif center_block is 'B':
            Cube.rotating_list_upper = [self.Rubic_B[0][1], self.Rubic_B[0][2],
                                        self.Rubic_B[1][2], self.Rubic_B[2][2],
                                        self.Rubic_B[2][1], self.Rubic_B[2][0],
                                        self.Rubic_B[1][0], self.Rubic_B[0][0], ]
        elif center_block is 'Y':
            Cube.rotating_list_upper = [self.Rubic_Y[0][1], self.Rubic_Y[0][2],
                                        self.Rubic_Y[1][2], self.Rubic_Y[2][2],
                                        self.Rubic_Y[2][1], self.Rubic_Y[2][0],
                                        self.Rubic_Y[1][0], self.Rubic_Y[0][0], ]
        else:
            print("Error in get_chars_to_rotate_upper")
        print("Upper Chars Taken")

    def put_chars_upper(self,dir,center_block):
        if dir is 'Clock':
            if center_block is 'W':
                self.Rubic_W[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[7]
            elif center_block is 'R':

                self.Rubic_R[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_R[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_R[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_R[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_R[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_R[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_R[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_R[0][2] = Cube.rotating_list_upper[7]
            elif center_block is 'G':
                self.Rubic_G[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_G[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_G[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_G[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_G[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_G[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_G[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_G[0][2] = Cube.rotating_list_upper[7]
            elif center_block is 'O':
                self.Rubic_O[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_O[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_O[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_O[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_O[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_O[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_O[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_O[0][2] = Cube.rotating_list_upper[7]
            elif center_block is 'B':
                self.Rubic_B[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_B[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_B[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_B[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_B[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_B[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_B[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_B[0][2] = Cube.rotating_list_upper[7]
            elif center_block is 'Y':
                self.Rubic_Y[1][2] = Cube.rotating_list_upper[0]
                self.Rubic_Y[2][2] = Cube.rotating_list_upper[1]
                self.Rubic_Y[2][1] = Cube.rotating_list_upper[2]
                self.Rubic_Y[2][0] = Cube.rotating_list_upper[3]
                self.Rubic_Y[1][0] = Cube.rotating_list_upper[4]
                self.Rubic_Y[0][0] = Cube.rotating_list_upper[5]
                self.Rubic_Y[0][1] = Cube.rotating_list_upper[6]
                self.Rubic_Y[0][2] = Cube.rotating_list_upper[7]
        elif dir is 'Anti_Clock':
            if center_block is 'W':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
            elif center_block is 'R':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
            elif center_block is 'G':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
            elif center_block is 'O':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
            elif center_block is 'B':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
            elif center_block is 'Y':
                self.Rubic_W[1][0] = Cube.rotating_list_upper[0]
                self.Rubic_W[0][0] = Cube.rotating_list_upper[1]
                self.Rubic_W[0][1] = Cube.rotating_list_upper[2]
                self.Rubic_W[0][2] = Cube.rotating_list_upper[3]
                self.Rubic_W[1][2] = Cube.rotating_list_upper[4]
                self.Rubic_W[2][2] = Cube.rotating_list_upper[5]
                self.Rubic_W[2][1] = Cube.rotating_list_upper[6]
                self.Rubic_W[2][0] = Cube.rotating_list_upper[7]
        else:
            print("Error in put_chars_upper")
        print("Upper Put ")

    def get_chars_to_rotate_side(self, dir, center_block):
        side_shifter = ['D','D','D',]
        if dir is 'Clock':
            if center_block is 'W':
                side_shifter[0]    = Cube.Rubic_R[2][0]; side_shifter[1]    = Cube.Rubic_R[2][1]; side_shifter[2]    = Cube.Rubic_R[2][2]
                Cube.Rubic_R[2][0] = Cube.Rubic_B[2][2]; Cube.Rubic_R[2][1] = Cube.Rubic_B[1][2]; Cube.Rubic_R[2][2] = Cube.Rubic_B[0][2]
                Cube.Rubic_B[2][2] = Cube.Rubic_O[0][2]; Cube.Rubic_B[1][2] = Cube.Rubic_O[0][1]; Cube.Rubic_B[0][2] = Cube.Rubic_O[0][0]
                Cube.Rubic_O[0][2] = Cube.Rubic_G[0][0]; Cube.Rubic_O[0][1] = Cube.Rubic_G[1][0]; Cube.Rubic_O[0][0] = Cube.Rubic_G[2][0]
                Cube.Rubic_G[0][0] = side_shifter[0]   ; Cube.Rubic_G[1][0] = side_shifter[1]   ; Cube.Rubic_G[2][0] = side_shifter[2]
            elif center_block is 'R':
                side_shifter[0]    = Cube.Rubic_Y[2][0]; side_shifter[1]    = Cube.Rubic_Y[2][1]; side_shifter[2]    = Cube.Rubic_Y[2][2]
                Cube.Rubic_Y[2][0] = Cube.Rubic_B[0][2]; Cube.Rubic_Y[2][1] = Cube.Rubic_B[0][1]; Cube.Rubic_Y[2][2] = Cube.Rubic_B[0][0]
                Cube.Rubic_B[0][2] = Cube.Rubic_W[0][2]; Cube.Rubic_B[0][1] = Cube.Rubic_W[0][1]; Cube.Rubic_B[0][0] = Cube.Rubic_W[0][0]
                Cube.Rubic_W[0][2] = Cube.Rubic_G[0][2]; Cube.Rubic_W[0][1] = Cube.Rubic_G[0][1]; Cube.Rubic_W[0][0] = Cube.Rubic_G[0][0]
                Cube.Rubic_G[0][2] = side_shifter[0]   ; Cube.Rubic_G[0][1] = side_shifter[1]   ; Cube.Rubic_G[0][0] = side_shifter[2]
            elif center_block is 'G':
                side_shifter[0]    = Cube.Rubic_R[2][2]; side_shifter[1]    = Cube.Rubic_R[1][2]; side_shifter[2]    = Cube.Rubic_R[0][2]
                Cube.Rubic_R[2][2] = Cube.Rubic_W[2][2]; Cube.Rubic_R[1][2] = Cube.Rubic_W[1][2]; Cube.Rubic_R[0][2] = Cube.Rubic_W[0][2]
                Cube.Rubic_W[2][2] = Cube.Rubic_O[2][2]; Cube.Rubic_W[1][2] = Cube.Rubic_O[1][2]; Cube.Rubic_W[0][2] = Cube.Rubic_O[0][2]
                Cube.Rubic_O[2][2] = Cube.Rubic_Y[2][2]; Cube.Rubic_O[1][2] = Cube.Rubic_Y[1][2]; Cube.Rubic_O[0][2] = Cube.Rubic_Y[0][2]
                Cube.Rubic_Y[2][2] = side_shifter[0]   ; Cube.Rubic_Y[1][2] = side_shifter[1]   ; Cube.Rubic_Y[0][2] = side_shifter[2]
            elif center_block is 'O':
                side_shifter[0]    = Cube.Rubic_W[2][0]; side_shifter[1]    = Cube.Rubic_W[2][1]; side_shifter[2]    = Cube.Rubic_W[2][2]
                Cube.Rubic_W[2][0] = Cube.Rubic_B[2][0]; Cube.Rubic_W[2][1] = Cube.Rubic_B[2][1]; Cube.Rubic_W[2][2] = Cube.Rubic_B[2][2]
                Cube.Rubic_B[2][0] = Cube.Rubic_Y[0][2]; Cube.Rubic_B[2][1] = Cube.Rubic_Y[0][1]; Cube.Rubic_B[2][2] = Cube.Rubic_Y[0][0]
                Cube.Rubic_Y[0][2] = Cube.Rubic_G[2][0]; Cube.Rubic_Y[0][1] = Cube.Rubic_G[2][1]; Cube.Rubic_Y[0][0] = Cube.Rubic_G[2][2]
                Cube.Rubic_G[2][0] = side_shifter[0]   ; Cube.Rubic_G[2][1] = side_shifter[1]   ; Cube.Rubic_G[2][2] = side_shifter[2]
            elif center_block is 'B':
                side_shifter[0]    = Cube.Rubic_R[2][0]; side_shifter[1]    = Cube.Rubic_R[1][0]; side_shifter[2]    = Cube.Rubic_R[0][0]
                Cube.Rubic_R[2][0] = Cube.Rubic_Y[2][0]; Cube.Rubic_R[1][0] = Cube.Rubic_Y[1][0]; Cube.Rubic_R[0][0] = Cube.Rubic_Y[0][0]
                Cube.Rubic_Y[2][0] = Cube.Rubic_O[2][0]; Cube.Rubic_Y[1][0] = Cube.Rubic_O[1][0]; Cube.Rubic_Y[0][0] = Cube.Rubic_O[0][0]
                Cube.Rubic_O[2][0] = Cube.Rubic_W[2][0]; Cube.Rubic_O[1][0] = Cube.Rubic_W[1][0]; Cube.Rubic_O[0][0] = Cube.Rubic_W[0][0]
                Cube.Rubic_W[2][0] = side_shifter[0]   ; Cube.Rubic_W[1][0] = side_shifter[1]   ; Cube.Rubic_W[0][0] = side_shifter[2]
            elif center_block is 'Y':
                side_shifter[0]    = Cube.Rubic_R[0][2]; side_shifter[1]    = Cube.Rubic_R[0][1]; side_shifter[2]    = Cube.Rubic_R[0][0]
                Cube.Rubic_R[0][2] = Cube.Rubic_G[2][2]; Cube.Rubic_R[0][1] = Cube.Rubic_G[1][2]; Cube.Rubic_R[0][0] = Cube.Rubic_G[0][2]
                Cube.Rubic_G[2][2] = Cube.Rubic_O[2][0]; Cube.Rubic_G[1][2] = Cube.Rubic_O[2][1]; Cube.Rubic_G[0][2] = Cube.Rubic_O[2][2]
                Cube.Rubic_O[2][0] = Cube.Rubic_B[0][0]; Cube.Rubic_O[2][1] = Cube.Rubic_B[1][0]; Cube.Rubic_O[2][2] = Cube.Rubic_B[2][0]
                Cube.Rubic_B[0][0] = side_shifter[0]   ; Cube.Rubic_B[1][0] = side_shifter[1]   ; Cube.Rubic_B[2][0] = side_shifter[2]
        elif dir is 'Anti_Clock':
            if center_block is 'W':
                side_shifter[0]    = Cube.Rubic_R[2][0]; side_shifter[1]    = Cube.Rubic_R[2][1];side_shifter[2]    = Cube.Rubic_R[2][2]
                Cube.Rubic_R[2][0] = Cube.Rubic_G[0][0]; Cube.Rubic_R[2][1] = Cube.Rubic_G[1][0];Cube.Rubic_R[2][2] = Cube.Rubic_G[0][0]
                Cube.Rubic_G[0][0] = Cube.Rubic_O[0][2]; Cube.Rubic_G[1][0] = Cube.Rubic_O[0][1];Cube.Rubic_G[0][0] = Cube.Rubic_O[0][0]
                Cube.Rubic_O[0][2] = Cube.Rubic_B[2][2]; Cube.Rubic_O[0][1] = Cube.Rubic_B[1][2];Cube.Rubic_O[0][0] = Cube.Rubic_B[0][2]
                Cube.Rubic_G[2][2] = side_shifter[0]   ; Cube.Rubic_G[1][2] = side_shifter[1]   ;Cube.Rubic_G[0][2] = side_shifter[2]
            elif center_block is 'R':
                side_shifter[0]    = Cube.Rubic_Y[2][0]; side_shifter[1]    = Cube.Rubic_Y[2][1] ;side_shifter[2]    = Cube.Rubic_Y[2][2]
                Cube.Rubic_Y[2][0] = Cube.Rubic_G[0][2]; Cube.Rubic_Y[2][1] = Cube.Rubic_G[0][1] ;Cube.Rubic_Y[2][2] = Cube.Rubic_G[0][0]
                Cube.Rubic_G[0][2] = Cube.Rubic_W[0][2]; Cube.Rubic_G[0][1] = Cube.Rubic_W[0][1] ;Cube.Rubic_G[0][0] = Cube.Rubic_W[0][0]
                Cube.Rubic_W[0][2] = Cube.Rubic_B[0][2]; Cube.Rubic_W[0][1] = Cube.Rubic_B[0][1] ;Cube.Rubic_W[0][0] = Cube.Rubic_B[0][0]
                Cube.Rubic_B[0][2] = side_shifter[0]   ; Cube.Rubic_B[0][1] = side_shifter[1]    ;Cube.Rubic_B[0][0] = side_shifter[2]
            elif center_block is 'G':
                side_shifter[0]    = Cube.Rubic_R[2][2]; side_shifter[1]    = Cube.Rubic_R[1][2] ; side_shifter[2]    = Cube.Rubic_R[0][2]
                Cube.Rubic_R[2][2] = Cube.Rubic_Y[2][2]; Cube.Rubic_R[1][2] = Cube.Rubic_Y[1][2] ; Cube.Rubic_R[0][2] = Cube.Rubic_Y[0][2]
                Cube.Rubic_Y[2][2] = Cube.Rubic_O[2][2]; Cube.Rubic_Y[1][2] = Cube.Rubic_O[1][2] ; Cube.Rubic_Y[0][2] = Cube.Rubic_O[0][2]
                Cube.Rubic_O[2][2] = Cube.Rubic_W[2][2]; Cube.Rubic_O[1][2] = Cube.Rubic_W[1][2] ; Cube.Rubic_O[0][2] = Cube.Rubic_W[0][2]
                Cube.Rubic_W[2][2] = side_shifter[0]   ; Cube.Rubic_W[1][2] = side_shifter[1]    ; Cube.Rubic_W[0][2] = side_shifter[2]
            elif center_block is 'O':
                side_shifter[0]    = Cube.Rubic_W[2][0]; side_shifter[1]    = Cube.Rubic_W[2][1]; side_shifter[2]    = Cube.Rubic_W[2][2]
                Cube.Rubic_W[2][0] = Cube.Rubic_G[2][0]; Cube.Rubic_W[2][1] = Cube.Rubic_G[2][1]; Cube.Rubic_W[2][2] = Cube.Rubic_G[2][2]
                Cube.Rubic_G[2][0] = Cube.Rubic_Y[0][2]; Cube.Rubic_G[2][1] = Cube.Rubic_Y[0][1]; Cube.Rubic_G[2][2] = Cube.Rubic_Y[0][0]
                Cube.Rubic_Y[0][2] = Cube.Rubic_B[2][0]; Cube.Rubic_Y[0][1] = Cube.Rubic_B[2][1]; Cube.Rubic_Y[0][0] = Cube.Rubic_B[2][2]
                Cube.Rubic_B[2][0] = side_shifter[0]   ; Cube.Rubic_B[2][1] = side_shifter[1];    Cube.Rubic_B[2][2] = side_shifter[2]
            elif center_block is 'B':
                side_shifter[0]    = Cube.Rubic_R[2][0]; side_shifter[1]    = Cube.Rubic_R[1][0]; side_shifter[2]    = Cube.Rubic_R[0][0]
                Cube.Rubic_R[2][0] = Cube.Rubic_W[2][0]; Cube.Rubic_R[1][0] = Cube.Rubic_W[1][0]; Cube.Rubic_R[0][0] = Cube.Rubic_W[0][0]
                Cube.Rubic_W[2][0] = Cube.Rubic_O[2][0]; Cube.Rubic_W[1][0] = Cube.Rubic_O[1][0]; Cube.Rubic_W[0][0] = Cube.Rubic_O[0][0]
                Cube.Rubic_O[2][0] = Cube.Rubic_Y[2][0]; Cube.Rubic_O[1][0] = Cube.Rubic_Y[1][0]; Cube.Rubic_O[0][0] = Cube.Rubic_Y[0][0]
                Cube.Rubic_Y[2][0] = side_shifter[0];    Cube.Rubic_Y[1][0] = side_shifter[1];    Cube.Rubic_Y[0][0] = side_shifter[2]
            elif center_block is 'Y':
                side_shifter[0]    = Cube.Rubic_R[0][2]; side_shifter[1]    = Cube.Rubic_R[0][1]; side_shifter[2]    = Cube.Rubic_R[0][0]
                Cube.Rubic_R[0][2] = Cube.Rubic_B[0][0]; Cube.Rubic_R[0][1] = Cube.Rubic_B[1][0]; Cube.Rubic_R[0][0] = Cube.Rubic_B[2][0]
                Cube.Rubic_B[0][0] = Cube.Rubic_O[2][0]; Cube.Rubic_B[1][0] = Cube.Rubic_O[2][1]; Cube.Rubic_B[2][0] = Cube.Rubic_O[2][2]
                Cube.Rubic_O[2][0] = Cube.Rubic_G[2][2]; Cube.Rubic_O[2][1] = Cube.Rubic_G[1][2]; Cube.Rubic_O[2][2] = Cube.Rubic_G[0][2]
                Cube.Rubic_G[2][2] = side_shifter[0];    Cube.Rubic_G[1][2] = side_shifter[1];    Cube.Rubic_G[0][2] = side_shifter[2]
        print("Side Chars Moved")

    def move_u(self,ref_center,ref_up_center):
        center_block=Cube.get_center_block(self,'UP',ref_center,ref_up_center)
        Cube.get_chars_to_rotate_upper(self,center_block)
        Cube.put_chars_upper(self,'Clock',center_block)
        Cube.get_chars_to_rotate_side(self,'Clock',center_block)
        print('Up Move made')
    def move_d(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'DOWN', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Clock', center_block)
        print('Down Move made')
    def move_r(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'RIGHT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Clock', center_block)
        print('Right Move made')
    def move_l(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'LEFT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Clock', center_block)
        print('Left Move made')
    def move_f(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'FRONT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Clock', center_block)
        print('Front Move made')
    def move_b(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'BACK', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Clock', center_block)
        print('Back Move made')
    def move_u_inv(self, ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'UP', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Up Inverse Move made')
    def move_d_inv(self, ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'DOWN', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Down Inverse Move made')
    def move_r_inv(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'RIGHT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Right Inverse Move made')
    def move_l_inv(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'LEFT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Left Inverse Move made')
    def move_f_inv(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'FRONT', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Front Inverse Move made')
    def move_b_inv(self,ref_center,ref_up_center):
        center_block = Cube.get_center_block(self, 'BACK', ref_center, ref_up_center)
        Cube.get_chars_to_rotate_upper(self, center_block)
        Cube.put_chars_upper(self, 'Anti_Clock', center_block)
        Cube.get_chars_to_rotate_side(self, 'Anti_Clock', center_block)
        print('Back Inverse Move made')