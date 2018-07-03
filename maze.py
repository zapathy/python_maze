import curses
from curses import wrapper
import numpy
from numpy.random import random_integers as rand
gh='5h9g908h4598yh45h43h5'

print("lol ez ez af + meg ezt is lol haha")
print("Mitortenik JOE?????????????????????????????????????")
#xdlol syepmunka nefijrkgbirghukwrkbjghiowegbeuwghiowl
print("Feri mitortenik")
height = 40
width = 80
shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
Z = numpy.zeros(shape, dtype=bool)
entryexit = [[0, 0], [0, 0]]

mapsize_x = shape[1]
mapsize_y = shape[0]
player_position = [0, 3]
running = True
hilite_char = False
show_map = False
finish_game = False


def getchar2(x, y):
    global Z
    retchar = str(Z[y, x])
    if retchar == 'True':
        retchar = '#'
    if retchar == 'False':
        retchar = '.'
    return retchar


def draw(stdscr):
    global hilite_char
    global entryexit
    global show_map
    global finish_game
    global running
    checkexit()
    if finish_game is False:
        stdscr.clear()
        if show_map is True:
            for y in range(mapsize_y):
                for x in range(mapsize_x):
                    if ((y == player_position[0]) and (
                            x == player_position[1])):
                        stdscr.addstr('@', curses.color_pair(1))
                    else:
                        if ((y == entryexit[0][0]) and (x == entryexit[0][1])):
                            stdscr.addstr('*', curses.color_pair(2))
                        else:
                            if ((y == entryexit[1][0]) and (
                                    x == entryexit[1][1])):
                                stdscr.addstr('$', curses.color_pair(3))
                            else:
                                cchar = getchar2(x, y)
                                if ((hilite_char is True) and (
                                        (x == player_position[1]) or (y == player_position[0]))):
                                    stdscr.addstr(cchar, curses.color_pair(5))
                                else:
                                    stdscr.addstr(cchar, curses.color_pair(4))
                stdscr.addstr('\n')
        else:
            max = 4
            y = max * (-1)
            while y <= max:
                drawnline = False
                x = max * (-1)
                while x <= max:
                    if ((player_position[1] + x < 0) or (player_position[1] + x > mapsize_x - 1) or (
                            player_position[0] + y < 0) or (player_position[0] + y > mapsize_y - 1)):
                        pass
                    else:
                        drawnline = True
                        if ((x == 0) and (y == 0)):
                            stdscr.addstr('@', curses.color_pair(1))
                        else:
                            if ((player_position[1] + x == entryexit[0][1])
                                    and (player_position[0] + y) == entryexit[0][0]):
                                stdscr.addstr('*', curses.color_pair(2))
                            else:
                                if ((player_position[1] + x == entryexit[1][1])
                                        and (player_position[0] + y) == entryexit[1][0]):
                                    stdscr.addstr('$', curses.color_pair(3))
                                else:
                                    cchar = getchar2(
                                        player_position[1] + x, player_position[0] + y)
                                    if (hilite_char is True):
                                        stdscr.addstr(
                                            cchar, curses.color_pair(5))
                                    else:
                                        stdscr.addstr(
                                            cchar, curses.color_pair(4))
                    x += 1
                y += 1
                if (drawnline is True):
                    stdscr.addstr('\n')
                    drawnline = False
                hilite_char = False
        stdscr.refresh()
    else:
        stdscr.addstr('YOU WON')
        running = False
        stdscr.getkey()


def colorinit():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)


def input(key):
    if (key == 'q'):
        global running
        running = False
    if (key == 'f'):
        global hilite_char
        hilite_char = True
    if (key == 'm'):
        global show_map
        if show_map is False:
            show_map = True
        elif show_map is True:
            show_map = False
    if (key == 'w'):
        if player_position[0] > 0:
            if getchar2(player_position[1], player_position[0] - 1) != '#':
                player_position[0] -= 1
    if (key == 's'):
        if player_position[0] < mapsize_y:
            if getchar2(player_position[1], player_position[0] + 1) != '#':
                player_position[0] += 1
    if (key == 'a'):
        if player_position[1] > 0:
            if getchar2(player_position[1] - 1, player_position[0]) != '#':
                player_position[1] -= 1
    if (key == 'd'):
        if player_position[1] < mapsize_x:
            if getchar2(player_position[1] + 1, player_position[0]) != '#':
                player_position[1] += 1


def main(stdscr):
    colorinit()
    maze()
    while running is True:
        draw(stdscr)
        key = stdscr.getkey()
        input(key)


def checkexit():
    global player_position
    global finish_game
    if ((player_position[0] == entryexit[1][0]) and (
            player_position[1] == entryexit[1][1])):
        finish_game = True


def maze():
    global Z
    global shape
    global height
    global width
    global entryexit
    global player_position
    complexity = .85
    density = .85
    # Only odd shapes

    # Adjust complexity and density relative to maze size
    # number of components
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    # size of components
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Build actual maze

    # Fill borders
    Z[0, :] = Z[-1, :] = 1
    Z[:, 0] = Z[:, -1] = 1
    # Make aisles
    for i in range(density):
        x, y = rand(0, shape[1] // 2) * 2, rand(0,
                                                shape[0] // 2) * 2  # pick a random position
        Z[y, x] = 1
        for j in range(complexity):
            neighbours = []
            if x > 1:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 1:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                y_, x_ = neighbours[rand(0, len(neighbours) - 1)]
                if Z[y_, x_] == 0:
                    Z[y_, x_] = 1
                    Z[y_ + (y - y_) // 2, x_ + (x - x_) // 2] = 1
                    x, y = x_, y_
    entryexit[0] = [0, 1]
    entryexit[1] = [20, 40]
    Z[entryexit[0][0], entryexit[0][1]] = 0
    Z[entryexit[1][0], entryexit[1][1]] = 0
    player_position[0] = entryexit[0][0]
    player_position[1] = entryexit[0][1]

    return Z


wrapper(main)
