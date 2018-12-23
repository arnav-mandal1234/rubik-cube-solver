ref_center = 'R'
ref_up_center = 'W'
Rubic_W_adj = 'RGOBR'
Rubic_R_adj = 'WBYGW'
Rubic_G_adj = 'WRYOW'
Rubic_O_adj = 'WGYBW'
Rubic_B_adj = 'WOYRW'
Rubic_Y_adj = 'RBOBR'


def get_center_block( move_id, ref_center, ref_up_center):
    switcher = {
        'UP': ref_up_center,
        'DOWN': get_opp_center_block( ref_up_center),
        'FRONT': ref_center,
        'BACK': get_opp_center_block( ref_center),
        'LEFT': get_right_or_left_center_block( 'LEFT', ref_center, ref_up_center),
        'RIGHT': get_right_or_left_center_block( 'RIGHT', ref_center, ref_up_center),
    }
    return switcher.get(move_id, "E")


def get_opp_center_block(center_block_id):
    switcher = {
        'W': 'Y',
        'R': 'O',
        'G': 'B',
        'O': 'R',
        'B': 'G',
        'Y': 'W',
    }
    return switcher.get(center_block_id, "E")


def get_right_or_left_center_block( request, ref_center, ref_up_center):
    right_center = 'E'
    left_center = 'E'
    switcher = {
        'W': Rubic_W_adj,
        'R': Rubic_R_adj,
        'G': Rubic_G_adj,
        'O': Rubic_O_adj,
        'B': Rubic_B_adj,
        'Y': Rubic_Y_adj,
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
print(get_center_block( 'RIGHT','R','W'))
