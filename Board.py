from Square import Square


class Board:
    def __init__(self):
        self.files = []
        for i in range(1, 9):
            file = []
            for j in range(1, 9):
                file.append(Square(i, j))
            self.files.append(file)

    def square_at(self, file, rank):
        if file < 1 or file > 8:
            raise RuntimeError("Illegal argument for file: " + str(file))
        if rank < 1 or rank > 8:
            raise RuntimeError("Illegal argument for rank: " + str(rank))

        return self.files[file - 1][rank - 1]

    def to_string(self):
        result = ""
        for j in range(8, 0, -1):
            for i in range(1, 9):
                square = self.square_at(i, j)
                if square.player_card is None:
                    result = result + ".. "
                else:
                    result = result + square.player_card.card_name + " "
            result = result + "\n\n"
        return result

    def to_string_for_player(self, selected_player, game_player_index):

        result = ""
        if game_player_index == 0:
            range_start = 8
            range_end = 0
            range_step = -1
        elif game_player_index == 1:
            range_start = 1
            range_end = 9
            range_step = 1
        else:
            raise RuntimeError("Bad game player index")

        for j in range(range_start, range_end, range_step):
            for i in range(1, 9):
                square = self.square_at(i, j)
                if square.player_card is None:
                    result = result + ".. "
                else:
                    if square.player_card.player == selected_player:
                        result = result + square.player_card.card_name + " "
                    else:
                        if square.player_card.revealed:
                            result = result + square.player_card.card_name + " "
                        else:
                            result = result + "OC "
            result = result + "\n\n"
        return result
