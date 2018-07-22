from actor import actor


class player(actor):
    __moved_this_turn = False
    __is_dead = False

    def stand_still(self):
        self.__moved_this_turn = True

    def set_for_new_turn(self):
        self.__moved_this_turn = False

    def check_if_moved(self):
        return self.__moved_this_turn

    def check_if_dead(self, enemy_position):
        pass

    def move_in_direction(self, direction):
        super.move_in_direction(self, direction)
        self.__moved_this_turn = True

    
