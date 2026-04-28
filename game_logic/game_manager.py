from game_logic.game_session import GameSession


class GameManager:
    def __init__(self):
        self.session = GameSession()

    def add_player(self, player_id, name):
        player = self.session.add_player(player_id, name)

        if player is None:
            return {
                "success": False,
                "message": "Room is full"
            }

        return {
            "success": True,
            "type": "player_joined",
            "player_id": player.player_id,
            "name": player.name,
            "symbol": player.symbol,
            "state": self.session.get_state()
        }

    def handle_roll(self, player_id):
        result = self.session.roll(player_id)
        result["type"] = "roll_result"
        result["state"] = self.session.get_state()
        return result

    def handle_move(self, player_id, from_pos, dice_value):
        result = self.session.move(player_id, from_pos, dice_value)
        result["type"] = "move_result"
        return result

    def get_state(self):
        return {
            "type": "game_state",
            "state": self.session.get_state()
        }