# Created by bach, for "Waking up for a reason"
# You can find more information here: https://www.tooboat.com/?p=49

import os
import bpy
import bmesh
from math import pi
import sys

# Add path of the .blend to allow import of module
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir )

# To install kociemba, clone the repository https://github.com/muodov/kociemba and move the "kociemba" folder where your .blend file is
import kociemba

bpy.context.scene.render.engine = 'CYCLES'

os.system("cls") # Clearing the console
print("Hey WUFAR") # Hello World

# Cubestring notation is UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
# You can find more information in the readme and other examples in tests/ at kociemba's repository https://github.com/muodov/kociemba

#cubestring = "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"
cubestring = "FFRRULFBDRFBURLFBUDLBRFFDBRBUUDDDLRLRULRLDULLUDDUBFFBB"

# Clearing all rubiks materials
for material in bpy.data.materials:
    if material.name.startswith("rubik"):
        material.user_clear()
        bpy.data.materials.remove(material)

# Creating new material
def createNewMat(name, r, g, b):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    diffuse = nodes.get("Diffuse BSDF")
    output = nodes.get("Material Output")
    nodes.remove(diffuse)
    mat.diffuse_color = (r, g, b)

    # Creating principled shader
    node_princ = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_princ.inputs[0].default_value = (r, g, b, 1)
    node_princ.location = 0,0

    # link nodes
    links = mat.node_tree.links
    link = links.new(node_princ.outputs[0], output.inputs[0])
    return mat

mat_black = createNewMat("rubik_black", 0.025, 0.025, 0.025)
mat_red = createNewMat("rubik_red", 0.475, 0, 0)
mat_white = createNewMat("rubik_white", 0.8, 0.8, 0.8)
mat_blue = createNewMat("rubik_blue", 0, 0, 0.475)
mat_green = createNewMat("rubik_green", 0, 0.475, 0)
mat_orange = createNewMat("rubik_orange", 0.754, 0.110, 0)
mat_yellow = createNewMat("rubik_yellow", 0.754, 0.443, 0)

bpy.app.debug = True # Allowing to view vertices indexes

scn = bpy.context.scene
scn.frame_start = 1
current_frame = 20

bpy.context.scene.frame_set(current_frame)

for i in bpy.data.objects: # To be able to launch the script multiple time
    if i.name.startswith("rubik"):
        bpy.data.objects.remove(i)

# Adding a quick text object
text = bpy.ops.object.text_add(radius=2.0, location=(-1.85, -0.5, -0.150), rotation=((pi * 90) / 180, 0, (pi * 180) / 180))
bpy.context.object.data.materials.append(mat_black)
bpy.data.objects[-1].name = "rubik_text"
bpy.data.objects["rubik_text"].data.body = "Go"
textChange = [{"frame": 0, "text": "Go"}]

def updateText(scene):
    for i in textChange:
        if scene.frame_current >= i['frame'] and scene.frame_current <= i['frame'] + 28:
            bpy.data.objects["rubik_text"].data.body = i['text']

bpy.app.handlers.frame_change_pre.append(updateText) # At each frame change, do updateText()

# Create the main cube and \o Paint it Black o/
for i in range(27):
    bpy.ops.mesh.primitive_cube_add(radius=0.25, location=(-0.50 * (int(i / 3) % 3), 0.50 * int(i / 9), 0.50 * (i % 3))) # Creating a cube
    bpy.context.object.name = "rubiks"+str(i)
    bpy.context.object.data.materials.append(mat_black)
    bpy.context.object.data.materials.append(mat_white)
    bpy.context.object.data.materials.append(mat_red)
    bpy.context.object.data.materials.append(mat_green)
    bpy.context.object.data.materials.append(mat_blue)
    bpy.context.object.data.materials.append(mat_yellow)
    bpy.context.object.data.materials.append(mat_orange)

# Extrude all faces
def extrude(name, faces, index, trans, size, material):
    for j in range(9):
        for i in bpy.data.objects:
            if i.name == "rubiks"+str(faces[j]):
                vg = i.vertex_groups.new(name)
                vg.add(index, 0, "ADD")
                bpy.context.scene.objects.active = i
                bpy.ops.object.mode_set(mode = 'OBJECT')
                bpy.ops.object.mode_set(mode = 'EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.context.object.vertex_groups.active = vg
                bpy.ops.object.vertex_group_select()
                bpy.ops.mesh.extrude_faces_indiv()
                bpy.ops.transform.translate(value=trans)
                bpy.ops.transform.resize(value=(size, size, size))
                bpy.ops.object.mode_set(mode = 'OBJECT')
                vg.remove(index)
                bpy.ops.object.mode_set(mode = 'EDIT')
                i.active_material_index = material[j]
                bpy.ops.object.material_slot_assign()
                bpy.ops.object.mode_set(mode = 'OBJECT')

def assignMat(cs):
    mat = []
    for i in range(9):
        if cs[i] == "U":
            mat.append(3)
        elif cs[i] == "R":
            mat.append(6)
        elif cs[i] == "F":
            mat.append(1)
        elif cs[i] == "D":
            mat.append(4)
        elif cs[i] == "L":
            mat.append(2)
        elif cs[i] == "B":
            mat.append(5)
    return mat

"""
backMat = [5, 5, 5, 5, 5, 5, 5, 5, 5]
leftMat = [2, 2, 2, 2, 2, 2, 2, 2, 2]
upMat = [3, 3, 3, 3, 3, 3, 3, 3, 3]
rightMat = [6, 6, 6, 6, 6, 6, 6, 6, 6]
frontMat = [1, 1, 1, 1, 1, 1, 1, 1, 1]
downMat = [4, 4, 4, 4, 4, 4, 4, 4, 4]
"""
upMat = assignMat(cubestring[0:9])
rightMat = assignMat(cubestring[9:18])
frontMat = assignMat(cubestring[18:27])
downMat = assignMat(cubestring[27:36])
leftMat = assignMat(cubestring[36:45])
backMat = assignMat(cubestring[45:54])

back = [8, 5, 2, 7, 4, 1, 6, 3, 0]
extrude("back", back, [1, 5, 0, 4], (0, -0.05, 0), 0.9, backMat)
left = [2, 11, 20, 1, 10, 19, 0, 9, 18]
extrude("left", left, [4, 5, 6, 7], (0.05, 0, 0), 0.9, leftMat)
up = [2, 5, 8, 11, 14, 17, 20, 23, 26]
extrude("up", up, [1, 3, 5, 7], (0, 0, 0.05), 0.9, upMat)
right = [26, 17, 8, 25, 16, 7, 24, 15, 6]
extrude("right", right, [0, 1, 2, 3], (-0.05, 0, 0), 0.9, rightMat)
front = [20, 23, 26, 19, 22, 25, 18, 21, 24]
extrude("front", front, [2, 3, 6, 7], (0, 0.05, 0), 0.9, frontMat)
down = [18, 21, 24, 9, 12, 15, 0, 3, 6]
extrude("down", down, [0, 2, 4, 6], (0, 0, -0.05), 0.9, downMat)

# Front White = 1
# Left Red = 2
# Up Green = 3
# Down Blue = 4
# Back Yellow = 5
# Right Orange = 6

# Moves
def pause(nb):
    global current_frame
    for i in range(nb):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

def moveRight(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    global textChange
    if not two:
        textChange.append({"frame": current_frame, "text": "R"})
    else:
        textChange.append({"frame": current_frame, "text": "R2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in right:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    right = [right[6], right[3], right[0], right[7], right[4], right[1], right[8], right[5], right[2]]
    frontcpy = list(front)
    front[2] = down[2]
    front[5] = down[5]
    front[8] = down[8]
    down[2] = back[6]
    down[5] = back[3]
    down[8] = back[0]
    back[6] = up[2]
    back[3] = up[5]
    back[0] = up[8]
    up[2] = frontcpy[2]
    up[5] = frontcpy[5]
    up[8] = frontcpy[8]

def moveRightPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "R'"})
    else:
        textChange.append({"frame": current_frame, "text": "R'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in right:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    right = [right[2], right[5], right[8], right[1], right[4], right[7], right[0], right[3], right[6]]
    frontcpy = list(front)
    front[2] = up[2]
    front[5] = up[5]
    front[8] = up[8]
    up[2] = back[6]
    up[5] = back[3]
    up[8] = back[0]
    back[6] = down[2]
    back[3] = down[5]
    back[0] = down[8]
    down[2] = frontcpy[2]
    down[5] = frontcpy[5]
    down[8] = frontcpy[8]

def moveUp(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "U"})
    else:
        textChange.append({"frame": current_frame, "text": "U2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in up:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(0, 0, 1))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    up = [up[6], up[3], up[0], up[7], up[4], up[1], up[8], up[5], up[2]]
    frontcpy = list(front)
    front[0] = right[0]
    front[1] = right[1]
    front[2] = right[2]
    right[0] = back[0]
    right[1] = back[1]
    right[2] = back[2]
    back[0] = left[0]
    back[1] = left[1]
    back[2] = left[2]
    left[0] = frontcpy[0]
    left[1] = frontcpy[1]
    left[2] = frontcpy[2]

def moveUpPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "U'"})
    else:
        textChange.append({"frame": current_frame, "text": "U'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in up:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(0, 0, 1))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    up = [up[2], up[5], up[8], up[1], up[4], up[7], up[0], up[3], up[6]]
    frontcpy = list(front)
    front[0] = left[0]
    front[1] = left[1]
    front[2] = left[2]
    left[0] = back[0]
    left[1] = back[1]
    left[2] = back[2]
    back[0] = right[0]
    back[1] = right[1]
    back[2] = right[2]
    right[0] = frontcpy[0]
    right[1] = frontcpy[1]
    right[2] = frontcpy[2]

def moveLeft(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "L"})
    else:
        textChange.append({"frame": current_frame, "text": "L2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in left:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    left = [left[6], left[3], left[0], left[7], left[4], left[1], left[8], left[5], left[2]]
    frontcpy = list(front)
    front[0] = up[0]
    front[3] = up[3]
    front[6] = up[6]
    up[0] = back[8]
    up[3] = back[5]
    up[6] = back[2]
    back[8] = down[0]
    back[5] = down[3]
    back[2] = down[6]
    down[0] = frontcpy[0]
    down[3] = frontcpy[3]
    down[6] = frontcpy[6]

def moveLeftPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "L'"})
    else:
        textChange.append({"frame": current_frame, "text": "L'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in left:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(1, 0, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    left = [left[2], left[5], left[8], left[1], left[4], left[7], left[0], left[3], left[6]]
    frontcpy = list(front)
    front[0] = down[0]
    front[3] = down[3]
    front[6] = down[6]
    down[0] = back[8]
    down[3] = back[5]
    down[6] = back[2]
    back[8] = up[0]
    back[5] = up[3]
    back[2] = up[6]
    up[0] = frontcpy[0]
    up[3] = frontcpy[3]
    up[6] = frontcpy[6]

def moveDown(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "D"})
    else:
        textChange.append({"frame": current_frame, "text": "D2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in down:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(0, 0, 1))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    down = [down[6], down[3], down[0], down[7], down[4], down[1], down[8], down[5], down[2]]
    frontcpy = list(front)
    front[6] = left[6]
    front[7] = left[7]
    front[8] = left[8]
    left[6] = back[6]
    left[7] = back[7]
    left[8] = back[8]
    back[6] = right[6]
    back[7] = right[7]
    back[8] = right[8]
    right[6] = frontcpy[6]
    right[7] = frontcpy[7]
    right[8] = frontcpy[8]

def moveDownPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "D'"})
    else:
        textChange.append({"frame": current_frame, "text": "D'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in down:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(0, 0, 1))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    down = [down[2], down[5], down[8], down[1], down[4], down[7], down[0], down[3], down[6]]
    frontcpy = list(front)
    front[6] = right[6]
    front[7] = right[7]
    front[8] = right[8]
    right[6] = back[6]
    right[7] = back[7]
    right[8] = back[8]
    back[6] = left[6]
    back[7] = left[7]
    back[8] = left[8]
    left[6] = frontcpy[6]
    left[7] = frontcpy[7]
    left[8] = frontcpy[8]

def moveFront(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "F"})
    else:
        textChange.append({"frame": current_frame, "text": "F2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in front:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(0, 1, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    front = [front[6], front[3], front[0], front[7], front[4], front[1], front[8], front[5], front[2]]
    upcpy = list(up)
    up[6] = left[8]
    up[7] = left[5]
    up[8] = left[2]
    left[8] = down[2]
    left[5] = down[1]
    left[2] = down[0]
    down[2] = right[0]
    down[1] = right[3]
    down[0] = right[6]
    right[0] = upcpy[6]
    right[3] = upcpy[7]
    right[6] = upcpy[8]

def moveFrontPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "F'"})
    else:
        textChange.append({"frame": current_frame, "text": "F'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in front:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(0, 1, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    front = [front[2], front[5], front[8], front[1], front[4], front[7], front[0], front[3], front[6]]
    upcpy = list(up)
    up[6] = right[0]
    up[7] = right[3]
    up[8] = right[6]
    right[0] = down[2]
    right[3] = down[1]
    right[6] = down[0]
    down[2] = left[8]
    down[1] = left[5]
    down[0] = left[2]
    left[8] = upcpy[6]
    left[5] = upcpy[7]
    left[2] = upcpy[8]

def moveBack(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "B"})
    else:
        textChange.append({"frame": current_frame, "text": "B2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in back:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * 10) / 180, axis=(0, 1, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    back = [back[6], back[3], back[0], back[7], back[4], back[1], back[8], back[5], back[2]]
    upcpy = list(up)
    up[0] = right[2]
    up[1] = right[5]
    up[2] = right[8]
    right[2] = down[8]
    right[5] = down[7]
    right[8] = down[6]
    down[8] = left[6]
    down[7] = left[3]
    down[6] = left[0]
    left[6] = upcpy[0]
    left[3] = upcpy[1]
    left[0] = upcpy[2]

def moveBackPrime(two = False):
    global current_frame
    global front
    global right
    global left
    global back
    global up
    global down
    if not two:
        textChange.append({"frame": current_frame, "text": "B'"})
    else:
        textChange.append({"frame": current_frame, "text": "B'2"})
    bpy.ops.object.select_all(action='DESELECT')
    for i in back:
        bpy.ops.object.select_pattern(pattern="rubiks"+str(i))
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    for i in range(9):
        current_frame += 2
        bpy.context.scene.frame_set(current_frame)
        bpy.ops.transform.rotate(value=(pi * -10) / 180, axis=(0, 1, 0))
        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    back = [back[2], back[5], back[8], back[1], back[4], back[7], back[0], back[3], back[6]]
    upcpy = list(up)
    up[0] = left[6]
    up[1] = left[3]
    up[2] = left[0]
    left[6] = down[8]
    left[3] = down[7]
    left[0] = down[6]
    down[8] = right[2]
    down[7] = right[5]
    down[6] = right[8]
    right[2] = upcpy[0]
    right[5] = upcpy[1]
    right[8] = upcpy[2]

def solutionParser(solution):
    for move in solution.split(" "):
        if move[-1] != "2" and move[-1] != "'":
            if move[0] == "R":
                moveRight()
            elif move[0] == "L":
                moveLeft()
            elif move[0] == "U":
                moveUp()
            elif move[0] == "D":
                moveDown()
            elif move[0] == "F":
                moveFront()
            elif move[0] == "B":
                moveBack()
        elif move[-1] == "'":
            if move[0] == "R":
                moveRightPrime()
            elif move[0] == "L":
                moveLeftPrime()
            elif move[0] == "U":
                moveUpPrime()
            elif move[0] == "D":
                moveDownPrime()
            elif move[0] == "F":
                moveFrontPrime()
            elif move[0] == "B":
                moveBackPrime()
        else:
            if move[0] == "R":
                moveRight(1)
                pause(5)
                moveRight(1)
            elif move[0] == "L":
                moveLeft(1)
                pause(5)
                moveLeft(1)
            elif move[0] == "U":
                moveUp(1)
                pause(5)
                moveUp(1)
            elif move[0] == "D":
                moveDown(1)
                pause(5)
                moveDown(1)
            elif move[0] == "F":
                moveFront(1)
                pause(5)
                moveFront(1)
            elif move[0] == "B":
                moveBack(1)
                pause(5)
                moveBack(1)
        pause(5)
    textChange.append({"frame": current_frame, "text": ":)"})

solutionParser(kociemba.solve(cubestring))
bpy.ops.object.select_all(action='DESELECT')


scn.frame_end = current_frame+40
