from Lobby import Lobby
from GameTest import match_1

PLAYER_0_USERNAME = "Francis"
PLAYER_1_USERNAME = "Edward"
ROOM_NAME = "Challenger"

lobby = Lobby()

lobby.add_player(PLAYER_0_USERNAME)
lobby.add_player(PLAYER_1_USERNAME)

lobby.create_room(PLAYER_0_USERNAME, ROOM_NAME)

lobby.add_player_in_room(PLAYER_1_USERNAME, ROOM_NAME)

game = lobby.create_room_game(ROOM_NAME)

match_1(game)
