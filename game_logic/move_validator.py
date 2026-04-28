class MoveValidator:
    def is_valid_move(self, board, player, from_pos, dice_value):
        if from_pos < 0 or from_pos >= 24:
            return False, "Invalid start position"

        if not board.is_own_point(from_pos, player):
            return False, "You do not have a checker there"

        to_pos = from_pos + (dice_value * player.direction)

        if 0 <= to_pos < 24:
            if board.is_blocked(to_pos, player):
                return False, "Target point is blocked"

        return True, to_pos