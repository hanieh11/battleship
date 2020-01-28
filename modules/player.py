from numpy.random import randint
from numpy import zeros, matrix


class Player:
    def __init__(self, name=None):
        self.info = {
            'name': name,
            'board': random_board_creator()
        }
        self.last_shot = None
        self.is_hit = False
        self.shot_list = []
        self.target_stack = []

    def shoot(self):
        if self.target_stack : #is the stack is not empty
            self.last_shot = self._target()
        else : #the stack is empty
            self.last_shot = self._hunt()
        return self.last_shot

    def _hunt(self):
        while True :
            x= randint(0, 10)
            y= randint(0, 10)
            random_shot=(x,y)
            if self.shot_list :
                if tuple(random_shot) in self.shot_list :
                    pass
                else:
                    self.shot_list.append(random_shot)
                    return random_shot
            else:
                self.shot_list.append(random_shot)
                return random_shot
        return random_shot
    def _target(self):
        target_shot=self.target_stack.pop()
        return target_shot

    def get_log(self, is_hit):
        if is_hit :
            self._fill_target_stack(self.last_shot)
        else:
            pass

    def _fill_target_stack (self,t_shot):

        if t_shot[0]-1 >= 0 : #if the above row exists
            if (t_shot[0]-1,t_shot[1]) not in self.shot_list : #if the above cell is not already shooted
                new_shot=(t_shot[0] - 1,t_shot[1])
                self.target_stack.append(new_shot)

        if t_shot[0]+1 <= 9 :
            if (t_shot[0]+1,t_shot[1]) not in self.shot_list : #if the bellow cell is not already shooted
                new_shot=t_shot[0] + 1, t_shot[1]
                self.target_stack.append(new_shot)

        if t_shot[1]-1 >= 0 :
            if (t_shot[0],t_shot[1]-1) not in self.shot_list : #if the left cell is not already shooted
                new_shot = t_shot[0], t_shot[1] - 1
                self.target_stack.append(new_shot)

        if t_shot[1]+1 <= 9:
            if (t_shot[0],t_shot[1]+1) not in self.shot_list:  # if the right cell is not already shooted
                new_shot =t_shot[0], t_shot[1] + 1
                self.target_stack.append(new_shot)

    def reset_board(self):
        self.shot_list =[]
        self.target_stack =[]
        self.info['board'] = random_board_creator()
        # self.__init__(name=self.name)

def random_board_creator(board_size=10, ships=(4, 3, 2, 1)):
    board = zeros(shape=(board_size, board_size))
    for ship_length in ships:
        ship_location = False
        while ship_location is False:
            (x, y) = randint(0, board_size, 2)  #2 is the number of random integers we need!
            orientation = []
            # check if north side is open
            if x - (ship_length-1) >= 0:
                if sum(board[x-ship_length+1:x+1, y]) == 0:
                    orientation.append('north')
            # check if south side is open
            if x + (ship_length-1) <= board_size-1:
                if sum(board[x:x+ship_length, y]) == 0:
                    orientation.append('south')

            # check if east side is open
            if y + (ship_length-1) <= board_size-1:
                if sum(board[x, y:y+ship_length]) == 0:
                    orientation.append('east')
            # check if west side is open
            if y - (ship_length-1) >= 0:
                if sum(board[x, y-ship_length+1:y+1]) == 0:
                    orientation.append('west')

            try:
                # there is a possible move
                assert len(orientation) != 0

                # pick a random orientation
                orient = orientation[randint(0, len(orientation))]

                if orient is 'north':
                    board[x-ship_length+1:x+1, y] = 1
                elif orient is 'south':
                    board[x:x+ship_length, y] = 1
                elif orient is 'east':
                    board[x, y:y+ship_length] = 1
                elif orient is 'west':
                    board[x, y-ship_length+1:y+1] = 1
                else:
                    raise ValueError
                ship_location = True
            except AssertionError:
                continue
    return matrix(board)
