import curses


def draw_wall_or_space(x_coord, y_coord, maze_attributes):
    is_wall = str(maze_attributes['walls'][y_coord, x_coord])
    if is_wall == 'True':
        return '#'
    if is_wall == 'False':
        return '.'


def draw_with_map(stdscr, game_state, maze_attributes):
    for y in range(maze_attributes['shape'][0]):
        for x in range(maze_attributes['shape'][1]):
            if ((y == game_state['player_position'][0]) and (
                    x == game_state['player_position'][1])):
                if game_state['player_dead'] is False:
                    stdscr.addstr('@', curses.color_pair(1))
                else:
                    stdscr.addstr('@', curses.color_pair(6))
            else:
                if ((y == game_state['enemy_position'][0]) and (x == game_state['enemy_position'][1])):
                    if game_state['enemy_behaviour'] == 2:
                        stdscr.addstr('&', curses.color_pair(6))
                    else:
                        stdscr.addstr('&', curses.color_pair(1))
                else:
                    if ((y == maze_attributes['entry'][0]) and (x == maze_attributes['entry'][1])):
                        stdscr.addstr('*', curses.color_pair(2))
                    else:
                        if ((y == maze_attributes['exit'][0]) and (
                                x == maze_attributes['exit'][1])):
                            stdscr.addstr('$', curses.color_pair(3))
                        else:
                            cchar = draw_wall_or_space(x, y, maze_attributes)
                            if ((game_state['hilite_char'] is True) and (
                                    (x == game_state['player_position'][1]) or
                                    (y == game_state['player_position'][0]))):
                                stdscr.addstr(
                                    cchar, curses.color_pair(5))
                            else:
                                stdscr.addstr(
                                    cchar, curses.color_pair(4))
        stdscr.addstr('\n')


def draw_centered_around_player(stdscr, game_state, maze_attributes):
    max = 4
    y = max * (-1)
    while y <= max:
        drawnline = False
        x = max * (-1)
        while x <= max:
            if ((game_state['player_position'][1] + x < 0) or
                    (game_state['player_position'][1] + x > maze_attributes['shape'][1] - 1) or (
                    game_state['player_position'][0] + y < 0) or
                    (game_state['player_position'][0] + y > maze_attributes['shape'][0] - 1)):
                pass
            else:
                drawnline = True
                if ((x == 0) and (y == 0)):
                    if game_state['player_dead'] is False:
                        stdscr.addstr('@', curses.color_pair(1))
                    else:
                        stdscr.addstr('@', curses.color_pair(6))
                else:
                    if ((game_state['player_position'][1] + x == game_state['enemy_position'][1])
                            and (game_state['player_position'][0] + y == game_state['enemy_position'][0])):
                        if game_state['enemy_behaviour'] == 2:
                            stdscr.addstr('&', curses.color_pair(6))
                        else:
                            stdscr.addstr('&', curses.color_pair(1))
                    else:
                        if ((game_state['player_position'][1] + x == maze_attributes['entry'][1])
                                and (game_state['player_position'][0] + y == maze_attributes['entry'][0])):
                            stdscr.addstr('*', curses.color_pair(2))
                        else:
                            if ((game_state['player_position'][1] + x == maze_attributes['exit'][1])
                                    and (game_state['player_position'][0] + y) == maze_attributes['exit'][0]):
                                stdscr.addstr(
                                    '$', curses.color_pair(3))
                            else:
                                cchar = draw_wall_or_space(
                                    game_state['player_position'][1] +
                                    x, game_state['player_position'][0] + y,
                                    maze_attributes)
                                if (game_state['hilite_char'] is True):
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
        game_state['hilite_char'] = False

