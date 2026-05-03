from game_logic.game_logic import GameLogic
from game_logic.game_state import Player


class GameSession:
    def __init__(self):
        self.players = []
        self.current_turn_index = 0
        self.logic = GameLogic()
        self.game_over = False
        self.winner = None
        self.current_dice = []

    def add_player(self, player_id, name):
        if len(self.players) >= 2:
            return None

        if len(self.players) == 0:
            player = Player(player_id, name, symbol=1, direction=1)
        else:
            player = Player(player_id, name, symbol=-1, direction=-1)

        self.players.append(player)
        return player

    def get_current_player(self):
        if not self.players:
            return None

        if self.current_turn_index >= len(self.players):
            self.current_turn_index = 0

        return self.players[self.current_turn_index]

    def roll(self, player_id):
        if self.game_over:
            return {"success": False, "message": "Game is over", "state": self.get_state()}

        current_player = self.get_current_player()

        if current_player is None:
            return {"success": False, "message": "No players yet", "state": self.get_state()}

        if current_player.player_id != player_id:
            return {"success": False, "message": "Not your turn", "state": self.get_state()}

        if self.current_dice:
            return {"success": False, "message": "Use current dice first", "state": self.get_state()}

        dice1, dice2 = self.logic.roll_dice()
        self.current_dice = [dice1, dice2]

        return {
            "success": True,
            "message": "Dice rolled",
            "dice": self.current_dice,
            "state": self.get_state()
        }

    def move(self, player_id, from_pos, dice_value):
        if self.game_over:
            return {"success": False, "message": "Game is over", "state": self.get_state()}

        current_player = self.get_current_player()

        if current_player is None:
            return {"success": False, "message": "No players yet", "state": self.get_state()}

        if current_player.player_id != player_id:
            return {"success": False, "message": "Not your turn", "state": self.get_state()}

        if dice_value not in self.current_dice:
            return {"success": False, "message": "Dice value not available", "state": self.get_state()}

        result = self.logic.move_player(current_player, from_pos, dice_value)

        if result["success"]:
            self.current_dice.remove(dice_value)

            if result.get("winner"):
                self.game_over = True
                self.winner = current_player.name
                self.current_dice = []

            elif len(self.current_dice) == 0:
                self.next_turn()

        result["state"] = self.get_state()
        return result

    def next_turn(self):
        if not self.players:
            return

        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    # ✅ FIXED: now inside class
    def skip_dice(self, player_id, dice_value):
        if self.game_over:
            return {"success": False, "message": "Game is over", "state": self.get_state()}

        current_player = self.get_current_player()

        if current_player.player_id != player_id:
            return {"success": False, "message": "Not your turn", "state": self.get_state()}

        if dice_value not in self.current_dice:
            return {"success": False, "message": "Dice value not available", "state": self.get_state()}

        self.current_dice.remove(dice_value)

        if len(self.current_dice) == 0:
            self.next_turn()

        return {"success": True, "message": "Dice skipped", "state": self.get_state()}

    # ✅ FIXED: indentation
    def get_state(self):
        current_player = self.get_current_player()

        return {
            "board": self.logic.get_board(),
            "bar": self.logic.get_bar(),
            "players": [
                {
                    "id": p.player_id,
                    "name": p.name,
                    "symbol": p.symbol,
                    "borne_off": p.borne_off
                }
                for p in self.players
            ],
            "current_turn": current_player.player_id if current_player else None,
            "current_dice": self.current_dice,
            "game_over": self.game_over,
            "winner": self.winner
        }