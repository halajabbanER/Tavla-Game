
from game_logic.game_session import GameSession


def print_title(title: str):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def test_session_creation():
    print_title("TEST 1 - Session Creation")

    session = GameSession("ayla", "ayla")

    print("Players:", session.players)
    print("Player colors:", session.player_colors)
    print("Current turn:", session.state.turn)


def test_roll_dice():
    print_title("TEST 2 - Roll Dice")

    session = GameSession("ayla", "ayla")

    ok, msg, dice = session.roll_dice_for_player("ayla")
    print("Result:", ok, msg)
    print("Dice:", dice)


def test_wrong_player_roll():
    print_title("TEST 3 - Wrong Player Roll")

    session = GameSession("ayla", "ayla")

    ok, msg, dice = session.roll_dice_for_player("ayla")
    print("Result:", ok, msg)
    print("Dice:", dice)


def test_move_without_rolling():
    print_title("TEST 4 - Move Without Rolling")

    session = GameSession("ayla", "ayla")

    ok, msg, state = session.move_for_player("Ayla", 23, 20)
    print("Result:", ok, msg)


def test_end_turn_without_using_dice():
    print_title("TEST 5 - End Turn Without Using Dice")

    session = GameSession("ayla", "ayla")
    session.roll_dice_for_player("ayla")

    ok, msg, state = session.end_turn_for_player("ayla")
    print("Result:", ok, msg)


if __name__ == "__main__":
    test_session_creation()
    test_roll_dice()
    test_wrong_player_roll()
    test_move_without_rolling()
    test_end_turn_without_using_dice()