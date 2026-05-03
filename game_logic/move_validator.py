class MoveValidator:
    def is_valid_move(self, board, player, from_pos, dice_value):
        # If the player has checkers on the bar, they must enter them first
        if board.bar[player.symbol] > 0:
            if from_pos != -1:
                return False, "You must enter from the bar first"

            if player.symbol == 1:
                to_pos = dice_value - 1
            else:
                to_pos = 24 - dice_value

            if board.is_blocked(to_pos, player):
                return False, "Target point is blocked"

            return True, to_pos

        # Normal move
        if from_pos < 0 or from_pos >= 24:
            return False, "Invalid start position"

        if not board.is_own_point(from_pos, player):
            return False, "You do not have a checker there"

        to_pos = from_pos + (dice_value * player.direction)

        if 0 <= to_pos < 24:
            if board.is_blocked(to_pos, player):
                return False, "Target point is blocked"

        return True, to_pos