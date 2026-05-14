from game_logic.game_manager import GameManager


class Room:
    def __init__(self):
        self.active_clients = []
        self.waiting_clients = []
        self.game_manager = GameManager()
        self.max_players = 2

    def add_client(self, client_handler):
        print(f"Current active clients: {len(self.active_clients)}")

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

            self.game_manager.session.players = [
                p for p in self.game_manager.session.players
                if p.player_id != client_handler.player_id
            ]

            self.broadcast({
                "type": "player_left",
                "message": f"Player left: {client_handler.player_id}"
            })

            if not self.active_clients:
                self.game_manager = GameManager()

    def broadcast(self, data):
        for client in self.active_clients:
            try:
                client.send(data)
            except Exception as e:
                print("Broadcast error:", e, flush=True)

    def handle_message(self, client_handler, message):
        if client_handler not in self.active_clients:
            return {
                "success": False,
                "message": "Please wait for your turn"
            }

        action = message.get("action")

        if action == "join":
            name = message.get("name", "Player")
            print(f"DEBUG: Player {name} with ID {client_handler.player_id} is trying to join.")
            print(f"DEBUG: Current players in session: {len(self.game_manager.session.players)}")

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