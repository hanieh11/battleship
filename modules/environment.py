from .errors import PlayerLostError


class Environment:
    def __init__(self, p1, p2):
        # get players' boards
        self.players = [p1, p2]
        self.num_turns = 0

    def _check_shot(self, defender=None, coordinate=None):
        # check if player i has hit player j
        # return boolean
        # update boards
        if self.players[defender].info['board'][coordinate[0], coordinate[1]] == 1:
            self.players[defender].info['board'][coordinate[0], coordinate[1]] = 0
            return True
        return False

    def _judge(self, defender=None):
        # check if a player is a winner
        try:
            assert self.players[defender].info['board'].sum() != 0
        except AssertionError:
            raise PlayerLostError

    def play_turn(self, shooter=None, coordinate=None):
        self.num_turns += 1
        is_hit = self._check_shot(defender=shooter-1, coordinate=coordinate) #is_hit is boolean
        try:
            self._judge(defender=shooter-1)
        except PlayerLostError:
            print('FINAL HIT!')
            self.num_turns //= 2
            raise
        return is_hit

    def launch_one_game(self):
        flag = 0
        while flag < 200:
            try:
                flag += 1
                # p1
                winner = self.players[0].info['name']
                is_hit = self.play_turn(shooter=0, coordinate=self.players[0].shoot())
                self.players[0].get_log(is_hit)

                # p2
                winner = self.players[1].info['name']
                is_hit = self.play_turn(shooter=1, coordinate=self.players[1].shoot())
                self.players[1].get_log(is_hit)
            except PlayerLostError:
                return winner
        return 'draw'

    def launch_game(self, iterations=None):
        winners = []
        for _ in range(iterations):
            winners.append(self.launch_one_game())
            self.players[0].reset_board()
            self.players[1].reset_board()
        print(winners)