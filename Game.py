from Board import *
from GamePlayer import GamePlayer


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        game_player1 = GamePlayer(player1, self, 0)
        game_player2 = GamePlayer(player2, self, 1)
        self.game_players = [game_player1, game_player2]
        self.turn = 0
        self.started = False

    def start_game(self):
        active_squares = 0
        for j in range(1, 9):
            for i in range(1, 9):
                square = self.board.square_at(i, j)
                if square.player_card is None:
                    continue
                else:
                    active_squares = active_squares + 1
        if active_squares == 16:
            self.started = True
        else:
            self.started = False
        return self.started

    def check_go_direction(self, direction, square, game_player_index):
        if direction == "N":
            if game_player_index == 0:
                return square.check_go_north()
            else:
                return square.check_go_south()
        if direction == "E":
            if game_player_index == 0:
                return square.check_go_east()
            else:
                return square.check_go_west()
        if direction == "S":
            if game_player_index == 1:
                return square.check_go_north()
            else:
                return square.check_go_south()
        if direction == "W":
            if game_player_index == 1:
                return square.check_go_east()
            else:
                return square.check_go_west()
        raise RuntimeError("Bad direction: ", direction)

    def to_string(self):
        result = self.board.to_string()
        stack_area_0 = self.game_players[0].stack_area.to_string()
        stack_area_1 = self.game_players[1].stack_area.to_string()
        result = stack_area_1 + "\n\n" + result + stack_area_0 + "\n\n"
        if not self.started:
            if self.game_players[0].is_winning():
                result = "LOSER" + "\n\n" + result + "WINNER"
            if self.game_players[1].is_winning():
                result = "WINNER" + "\n\n" + result + "LOSER"
        return result

    def to_dict(self):
        return {
            "board": self.board.to_string(),
            "turn": self.turn,
            "started": self.started
        }

    def to_dict_for_player(self, game_player_index):
        return {
            "board": self.board.to_string_for_player(self.game_players[game_player_index].player, game_player_index),
            "turn": self.turn,
            "started": self.started
        }

    # @staticmethod
    # def create_game(player1, player2):
    #     game = Game()
    #     game.game_players =

