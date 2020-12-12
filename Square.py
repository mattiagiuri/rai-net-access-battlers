class Square:
    TYPE_SERVER_PORT = "S"
    TYPE_NORMAL = "N"

    SETUP_ZONE = [[(1, 1), (2, 1), (3, 1), (4, 2), (5, 2), (6, 1), (7, 1), (8, 1)], [(1, 8), (2, 8), (3, 8), (4, 7), (5, 7), (6, 8), (7, 8), (8, 8)]]
    SERVER_PORTS = [[(4, 1), (5, 1)], [(4, 8), (5, 8)]]
    DIRECTIONS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

    def __init__(self, file, rank):
        if file < 1 or file > 8:
            raise RuntimeError("Illegal argument for file: " + file)
        if rank < 1 or rank > 8:
            raise RuntimeError("Illegal argument for rank: " + rank)

        self.square_coordinates = (file, rank)
        self.square_type = self.__compute_square_type()
        self.player_card = None
        self.player_boost_card = None

    def __compute_square_type(self):
        if self.square_coordinates == (4, 1) or self.square_coordinates == (5, 1) or self.square_coordinates == (4, 8) or self.square_coordinates == (5, 8):
            return Square.TYPE_SERVER_PORT
        else:
            return Square.TYPE_NORMAL

    def is_setup(self, game_player_index):
        return Square.SETUP_ZONE[game_player_index].index(self.square_coordinates) >= 0

    @property
    def file(self):
        return self.square_coordinates[0]

    @property
    def rank(self):
        return self.square_coordinates[1]

    def check_go_north(self):
        return self.rank != 8

    def check_go_south(self):
        return self.rank != 1

    def check_go_east(self):
        return self.file != 8

    def check_go_west(self):
        return self.file != 1

