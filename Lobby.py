from Player import Player
from Room import Room


class Lobby:
    def __init__(self):
        self.players = dict()
        self.rooms = dict()
        self.current_id = 0
        self.players_id = dict()

    @staticmethod
    def string_converter(l):
        result = ""
        for i in l:
            result = result+str(i)+', '
        return result

    def to_dict(self):
        return {
            "players": list(self.players.keys()),
            "rooms": list(self.rooms.keys())
        }

    def add_player(self, username):
        if username in self.players:
            return None
        new_player = Player(username)
        self.players[username] = new_player
        self.players_id[username] = self.current_id
        self.current_id = self.current_id + 1
        return new_player

    def create_room(self, username, room_name):
        player = self.players[username]
        # if player is not here, return PLAYER_UNKNOWN
        if room_name in self.rooms:
            return None
        new_room = Room(player, room_name, self)
        self.rooms[room_name] = new_room
        return new_room

    def get_player(self, username):
        return self.players[username]

    def add_player_in_room(self, username, room_name):
        self.rooms[room_name].player_1 = self.players[username]

    def create_room_game(self, room_name):
        room = self.rooms[room_name]
        if room.player_1 is not None:
            room.create_game()
        return room.game
