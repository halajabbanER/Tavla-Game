import random


class Dice:
    def roll(self):
        return random.randint(1, 6), random.randint(1, 6)


class Player:
    def __init__(self, player_id, name, symbol, direction):
        self.player_id = player_id
        self.name = name
        self.symbol = symbol      # 1 or -1
        self.direction = direction
        self.borne_off = 0


class Board:
    def __init__(self):
        self.points = [0] * 24

        # bar للقطع المضروبة
        self.bar = {
            1: 0,
            -1: 0
        }

        self.setup_board()

    def setup_board(self):
        self.points[0] = 2
        self.points[11] = 5
        self.points[16] = 3
        self.points[18] = 5

        self.points[23] = -2
        self.points[12] = -5
        self.points[7] = -3
        self.points[5] = -5

    def is_own_point(self, index, player):
        return self.points[index] * player.symbol > 0

    def is_blocked(self, index, player):
        return self.points[index] * player.symbol < -1

    def can_hit(self, index, player):
        return self.points[index] * player.symbol == -1

    def move_checker(self, from_pos, to_pos, player):
        # إذا اللاعب داخل من bar
        if from_pos == -1:
            self.bar[player.symbol] -= 1
        else:
            self.points[from_pos] -= player.symbol

        # bearing off
        if to_pos < 0 or to_pos >= 24:
            player.borne_off += 1
            return "borne_off"

        # hit
        if self.can_hit(to_pos, player):
            opponent_symbol = -player.symbol
            self.bar[opponent_symbol] += 1
            self.points[to_pos] = 0

        self.points[to_pos] += player.symbol
        return "moved"

    def is_win(self, player):
        return player.borne_off >= 15

    def to_dict(self):
        return self.points