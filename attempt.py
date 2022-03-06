import numpy as np
import matplotlib.pyplot as plt
#import pygame


# Define Action Sets (x,y): Right, Left, Up, Down, top right, top left, bottom right, bottom left
Action_sets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

# ask user for input
start_point_x = input("Enter starting x coordinate:")
start_point_y = input("Enter starting y coordinate:")
goal_x = input("Enter goal x coordinate:")
goal_y = input("Enter goal y coordinate:")

start_point_x = int(start_point_x)
start_point_y = int(start_point_y)
goal_x = int(goal_x)
goal_y = int(goal_y)

# Initial node
current_nodex, current_nodey = start_point_x, start_point_y

# Case where start and end goal are the same
if (start_point_x, start_point_y) == (goal_x, goal_y):
    goal_reached = True
    print(
        "You entered the same coordinate for goal and starting point, please re-run the code and enter different coordinates for the goal")
    exit()

goal_reached = False


def move(a, nodex, nodey):
    if a == Action_sets[0]:
        print("move right")
        nodex = nodex + 1
        nodey = nodey
        cost = 1

    elif a == Action_sets[1]:
        print("move left")
        nodex = nodex - 1
        nodey = nodey
        cost = 1

    elif a == Action_sets[2]:
        print("move up")
        nodex = nodex
        nodey = nodey + 1
        cost = 1

    elif a == Action_sets[3]:
        print("move down")
        nodex = nodex
        nodey = nodey - 1
        cost = 1

    elif a == Action_sets[4]:
        print("move top right")
        nodex = nodex + 1
        nodey = nodey + 1
        cost = 1.4

    elif a == Action_sets[5]:
        print("move top left")
        nodex = nodex - 1
        nodey = nodey + 1
        cost = 1.4

    elif a == Action_sets[6]:
        print("move bot right")
        nodex = nodex + 1
        nodey = nodey - 1
        cost = 1.4

    elif a == Action_sets[7]:
        print("move bot left")
        nodex = nodex - 1
        nodey = nodey - 1
        cost = 1.4

    return nodex, nodey, cost


Open = []
Close = []


def check_and_dijistra(next_nodex, next_nodey, current_nodex, current_nodey, direction_cost):
    print("went inside dijistra")
    current_parent_ind, current_index, current_c2c, current_xy_point = dic[current_nodex, current_nodey]

    for k in only_path_points:

        # Check if node exists, or if there is an obsticle
        if k == (next_nodex, next_nodey):
            print("next node k is", k)
            next_parent_ind, next_index, next_c2c, next_xy_point = dic[next_nodex, next_nodey]
            print("Node exists in graph! We can proceed")

            # the point (or node) k also has to be unvisited, k should not be in the closed list
            # check if new node values are in the closed loop, and if so, then abort

            for check in Close:
                if check == dic[next_nodex, next_nodey]:
                    print("found duplicate in closed loop, aborting")
                    return

            # Calculate new cost
            updated_c2c = current_c2c + direction_cost

            # Dijistra Order priority for choosing nodes
            # if next_c2c == np.inf or
            if updated_c2c < next_c2c:
                # update parent node of new node
                updated_parent_ind = current_index

                # Update dictionary for new node
                dic[(next_nodex, next_nodey)] = (
                updated_parent_ind, dic[(next_nodex, next_nodey)][1], updated_c2c, (next_nodex, next_nodey))
                print("Updated Dictionary! new parent index, index, cost to go!!! ", dic[next_nodex, next_nodey])

                # Note that current node information does not have to change

                # Update open and closed lists
                # Add new nodes to list of Open nodes, one of these will be the current node later
                Open.append(dic[next_nodex, next_nodey])
                # print("Open is :", Open)


                # return open_dup, close_dup, final_check
        else:
            # print("Cannot move in this direction")
            pass
    return


# Calculate area of triangle formed by (x1, y1),(x2, y2) and (x3, y3)
def area_triangle(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


# Check whether point P(x, y) lies inside the triangle formed by A(x1, y1), B(x2, y2) and C(x3, y3)
def isInside_triangle(x1, y1, x2, y2, x3, y3, x, y):
    # Calculate area of triangle ABC
    A = area_triangle(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = area_triangle(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = area_triangle(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = area_triangle(x1, y1, x2, y2, x, y)

    # Check if sum of A1, A2 and A3
    # is same as A
    if (A == A1 + A2 + A3):
        return True
    else:
        return False


# Define Obstacle Space
x = 400.00
y = 250.00
xp = []
yp = []
all_graph_points = []

for i in range(int(x) + 1):
    for j in range(int(y) + 1):
        point = (i, j)
        all_graph_points.append(point)

remove_circle = []
for i in all_graph_points:
    # Most right circle
    if (i[0] - 300) ** 2 + (i[1] - 185) ** 2 <= 40 ** 2:
        remove_circle.append((i[0], i[1]))

    # Hexagon
    # I replaces it with a circle to get an aestimate at least
    elif (i[0] - 200) ** 2 + (i[1] - 100) ** 2 <= 35 ** 2:
        remove_circle.append((i[0], i[1]))

    # Check if point is inside triangle
    elif isInside_triangle(36, 185, 115, 210, 80, 180, i[0], i[1]):
        pass

    elif isInside_triangle(105, 100, 36, 185, 80, 180, i[0], i[1]):
        pass

    else:
        xp.append(i[0])
        yp.append(i[1])

only_path_points = []
for i, j in zip(xp, yp):
    point = (i, j)
    only_path_points.append(point)

# xp and yp have all node points, no points present on the obstacle space
plt.plot(xp, yp, 'o')
plt.show()

dic = {}

# for i, j in zip(xp, yp):
# print("i is" , i)
# print("y is", y)

# dic[{x,y}] = (parent_ind, index, c2c)
parent_ind = np.Infinity
c2c = np.Infinity
index = 1

# Generate Final graph Nodes
# Note: This contains the same points as only_path_points = [] (could've written it better to not duplicate)
for i, j in zip(range(len(xp)), range(len(yp))):
    dic[(xp[i], yp[j])] = (parent_ind, index, c2c, (xp[i], yp[j]))
    index = index + 1

# initialize first node
dic[(start_point_y, start_point_y)] = (1, 1, 0, (start_point_x, start_point_y))

current_nodex = start_point_x
current_nodey = start_point_y
c2c_list = []

############Dijistra run code ######################3
while (goal_reached == False):

    # Check if goal coordinate is in closed list
    for i in Close:
        if i[3] == (goalx, goal_y):
            goal_reached == (True)
            print("Goal Reached!")
            exit()
            break

    # Add inital current node to list of Open nodes
    Open.append(dic[current_nodex, current_nodey])
    print("Open is : ", Open)
    # Search the nodes, then check and dijistra
    for action in Action_sets:
        # Go from current node to another based on the action
        new_nodex, new_nodey, direction_cost = move(action, current_nodex, current_nodey)

        # Dijistra and Check if the new node exists in the graph (make sure there are no obstacles)
        check_and_dijistra(new_nodex, new_nodey, current_nodex, current_nodey, direction_cost)
        # print("open list is :" , open_dup)

    # Add current node to list of closed nodes
    Close.append(dic[current_nodex, current_nodey])


    print("Open list after popping current node", Open)

    # pop current node from open list
    Open.remove(dic[current_nodex, current_nodey])





    c2c_list = []

    print("cleared c2c is :", c2c_list)

    # Choose next node with lowest cost
    '''
    for i, j in zip(Open, Close):
        if i != j:
            c2c_list.append(i[2])
    '''

    for i in Open:
        c2c_list.append(i[2])
    min_c2c = min(c2c_list)

    print("c2c list is ", c2c_list)

    for i, j in zip(Open, Close):
        if i != j:
            # Pull out the dictionary key with the lowest c2c
            if i[2] == min_c2c:
                # print("Detected min next c2c node from open list: ", i)
                lowest_c2c_node = i

    # update current node
    current_nodex, current_nodey = lowest_c2c_node[3][0], lowest_c2c_node[3][1]

    # print("updated cuerrent nodex : ", current_nodex)
    # print("updated current nodey : ", current_nodey)





#Visualisation
pygame.init()

display_width = 400
display_height = 250
gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
pygame.display.set_caption('Animation')

color = (150,150,233)
white = (255,255,255)


gameDisplay.fill(white)
for i in Open:
    x = i[3][0]
    y = i[0][1]
    pygame.draw.rect(gameDisplay, (0, 0, 255), [x, y, 1, 1])

