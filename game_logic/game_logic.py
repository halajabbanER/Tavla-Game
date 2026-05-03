from game_logic.game_state import Board, Dice
from game_logic.move_validator import MoveValidator


class GameLogic:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.validator = MoveValidator()

    def roll_dice(self):
        return self.dice.roll()

    def move_player(self, player, from_pos, dice_value):
        is_valid, result = self.validator.is_valid_move(
            self.board,
            player,
            from_pos,
            dice_value
        )

        if not is_valid:
            return {
                "success": False,
                "message": result
            }

        to_pos = result
        move_type = self.board.move_checker(from_pos, to_pos, player)

        return {
            "success": True,
            "message": "Checker moved",
            "from": from_pos,
            "to": to_pos,
            "dice_used": dice_value,
            "move_type": move_type,
            "borne_off": player.borne_off,
            "winner": self.board.is_win(player)
        }

    def get_board(self):
        return self.board.to_dict()

    def get_bar(self):
        return self.board.bar