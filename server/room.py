from game_logic.game_manager import GameManager


class Room:
    def __init__(self):
        self.active_clients = []
        self.waiting_clients = []
        self.game_manager = GameManager()
        self.max_players = 2

    def add_client(self, client_handler):
        if len(self.active_clients) < self.max_players:
            self.active_clients.append(client_handler)
            client_handler.send({
                "success": True,
                "message": "You joined the game"
            })
        else:
            self.waiting_clients.append(client_handler)
            client_handler.send({
                "success": False,
                "message": "Room full. Please wait..."
            })

    def remove_client(self, client_handler):
        if client_handler in self.active_clients:
            self.active_clients.remove(client_handler)

            self.broadcast({
                "type": "player_left",
                "message": f"Player left: {client_handler.player_id}"
            })

            if self.waiting_clients:
                next_client = self.waiting_clients.pop(0)
                self.active_clients.append(next_client)

                next_client.send({
                    "success": True,
                    "message": "You can join now!"
                })

        elif client_handler in self.waiting_clients:
            self.waiting_clients.remove(client_handler)

    def broadcast(self, data):
        for client in self.active_clients:
            try:
                client.send(data)
            except:
                pass

    def handle_message(self, client_handler, message):
        if client_handler not in self.active_clients:
            return {
                "success": False,
                "message": "Please wait for your turn"
            }

        action = message.get("action")

        if action == "join":
            name = message.get("name", "Player")

            response = self.game_manager.add_player(
                client_handler.player_id,
                name
            )

            self.broadcast(response)
            return None

        if action == "roll":
            response = self.game_manager.handle_roll(
                client_handler.player_id
            )

            self.broadcast(response)
            return None

        if action == "move":
            from_pos = message.get("from")
            dice_value = message.get("dice")

            response = self.game_manager.handle_move(
                client_handler.player_id,
                from_pos,
                dice_value
            )

            self.broadcast(response)
            return None

        if action == "skip":
            dice_value = message.get("dice")

            response = self.game_manager.handle_skip(
                client_handler.player_id,
                dice_value
            )

            self.broadcast(response)
            return None

        if action == "state":
            return self.game_manager.get_state()

        return {
            "success": False,
            "message": "Unknown action"
        }