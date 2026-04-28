from game_logic.game_manager import GameManager


class Room:
    def __init__(self):
        self.clients = []
        self.game_manager = GameManager()

    def add_client(self, client_handler):
        self.clients.append(client_handler)

    def handle_message(self, client_handler, message):
        action = message.get("action")

        if action == "join":
            name = message.get("name", "Player")
            return self.game_manager.add_player(client_handler.player_id, name)

        if action == "roll":
            return self.game_manager.handle_roll(client_handler.player_id)

        if action == "move":
            from_pos = message.get("from")
            dice_value = message.get("dice")

            return self.game_manager.handle_move(
                client_handler.player_id,
                from_pos,
                dice_value
            )

        if action == "state":
            return self.game_manager.get_state()

        return {
            "success": False,
            "message": "Unknown action"
        }