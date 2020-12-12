from Game import Game


class Room:

    def __init__(self, player_0, name, lobby):
        self.name = name
        self.player_0 = player_0
        self.player_1 = None
        self.game = None
        self.lobby = lobby

    def set_player_1(self, username):
        self.player_1 = self.lobby.players[username]

    def create_game(self):
        self.game = Game(self.player_0, self.player_1)

    def get_game(self):
        return self.game
