class actor:
    __position = [0, 0]

    def teleport_to(self, x, y):
        self.__position = [x, y]
        self.moved_this_turn = True

    def move_in_direction(self, direction):
        if direction == "left":
            self.__position[0] -= 1
        elif direction == "right":
            self.__position[0] += 1
        elif direction == "up":
            self.__position[1] -= 1
        elif direction == "down":
            self.__position[1] += 1
        
    def get_position(self):
        return self.__position
