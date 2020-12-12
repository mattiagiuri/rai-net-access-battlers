from Card import Card
from PlayerCard import PlayerCard
from StackArea import StackArea


class GamePlayer:
    RETURN_CODE_MOVE_OK = 0
    RETURN_CODE_MOVE_BLOCKED = 1
    RETURN_CODE_MOVE_CANNOT_TRANSIT = 2
    RETURN_CODE_MOVE_BOARDER = 3

    def __init__(self, player, game, game_player_index):
        self.player = player
        self.game = game
        self.my_cards = dict()
        self.stack_area = StackArea()
        self.__add_all_cards()
        self.game_player_index = game_player_index
        self.firewall_count = 0
        self.count_404 = 0
        self.line_boosted = None
        self.virus_checker_counter = 0
        self.win = False
        self.lose = False

    def __add_cards(self, card, card_name):
        player_card = PlayerCard(self.player, card, card_name)
        self.my_cards[card_name] = player_card

    def __add_all_cards(self):
        for i in range(0, 4):
            self.__add_cards(Card.create_virus(), "V" + str(i))
            self.__add_cards(Card.create_link(), "L" + str(i))

        self.__add_cards(Card.create_404_not_found(), "NF")
        self.__add_cards(Card.create_boost_line(), "BL")
        self.__add_cards(Card.create_firewall(), "FW")
        self.__add_cards(Card.create_virus_checker(), "VC")

    def do_put_card_on_setup(self, file, rank, card_name):
        square = self.game.board.square_at(file, rank)
        if square.is_setup(self.game_player_index):
            player_card = self.my_cards[card_name]
            if player_card.current_square is not None:
                player_card.current_square.player_card = None
                player_card.current_square = None
            square.player_card = player_card
            player_card.current_square = square
            return True
        else:
            return False

    def step(self, file, rank, card_name):
        if self.game.started and self.game.turn == self.game_player_index:
            final_square = self.game.board.square_at(file, rank)
            moving_card = self.my_cards[card_name]
            if final_square.player_card is not None:
                self.capture(final_square)

            self.__place_card(final_square, moving_card)
        else:
            raise RuntimeError("Ehi you moron, not your turn", self.game.turn,  self.game_player_index)

    def escape(self, card_name):
        escaping_card = self.my_cards[card_name]
        if escaping_card.current_square.square_type == "S":
            self.auto_line_boost_detach(self, escaping_card.current_square.file, escaping_card.current_square.rank)
            self.capture(escaping_card.current_square)
            self.__remove_card(escaping_card)
        else:
            raise RuntimeError("You can only escape from a server port")

    def capture(self, final_square):
        if final_square.player_card.card.is_link():
            self.stack_area.links.append(final_square.player_card)
            self.is_terminating()
        if final_square.player_card.card.is_virus():
            self.stack_area.viruses.append(final_square.player_card)
            self.is_terminating()

    def __place_card(self, final_square, moving_card):
        if moving_card.current_square is not None:
            moving_card.current_square.player_card = None
        enemy_player = self.game.game_players[1 - self.game_player_index]
        if final_square.player_card == enemy_player.line_boosted:
            self.auto_line_boost_detach(enemy_player, final_square.file, final_square.rank)
        final_square.player_card = moving_card
        moving_card.current_square = final_square

    @staticmethod
    def __remove_card(moving_card):
        if moving_card.current_square is not None:
            moving_card.current_square.player_card = None
            moving_card.current_square = None

    def is_blocked(self, square):
        if square.square_coordinates == square.SERVER_PORTS[self.game_player_index][0] or square.square_coordinates == square.SERVER_PORTS[self.game_player_index][1]:
            return True

        if square.player_card is None:
            return False

        if square.player_card.card.card_type == "FW":
            return True

        for i in self.my_cards.keys():
            if square.player_card == self.my_cards[i]:
                return True

        return False

    def free_for_transit(self, square):
        if square.square_coordinates == square.SERVER_PORTS[self.game_player_index][0] or square.square_coordinates == \
                square.SERVER_PORTS[self.game_player_index][1]:
            return False

        if square.player_card is None:
            return True

        return False

    def card_move(self, card_name, direction1, direction2=None):
        if direction2 is not None and self.line_boosted != self.my_cards[card_name]:
            raise RuntimeError("You can't move twice a non line boosted card")
        parity = pow(-1, self.game_player_index)
        moving_card = self.my_cards[card_name]
        square = moving_card.current_square
        if direction2 is not None:
            if direction1 == "F":
                raise RuntimeError("You can't escape before making another move")
            if self.game.check_go_direction(direction1, square, self.game_player_index):

                transit_square = self.game.board.square_at(square.file + parity * square.DIRECTIONS[direction1][0], square.rank + parity * square.DIRECTIONS[direction1][1])
                if self.free_for_transit(transit_square):
                    if direction2 == "F":
                        self.step(transit_square.file, transit_square.rank, card_name)

                        self.escape(card_name)
                    else:
                        final_square = self.game.board.square_at(transit_square.file + parity * transit_square.DIRECTIONS[direction2][0], transit_square.rank + parity * transit_square.DIRECTIONS[direction2][1])
                        if not self.is_blocked(final_square):
                            self.step(final_square.file, final_square.rank, card_name)
                            self.game.turn = 1 - self.game.turn
                            return GamePlayer.RETURN_CODE_MOVE_OK
                        else:
                            return GamePlayer.RETURN_CODE_MOVE_BLOCKED
                else:
                    return GamePlayer.RETURN_CODE_MOVE_CANNOT_TRANSIT
            else:
                return GamePlayer.RETURN_CODE_MOVE_BOARDER

        if direction2 is None:
            if direction1 == "F":
                self.escape(card_name)
            else:
                if self.game.check_go_direction(direction1, square, self.game_player_index):
                    final_square = self.game.board.square_at(square.file + parity * square.DIRECTIONS[direction1][0], square.rank + parity * square.DIRECTIONS[direction1][1])
                    if not self.is_blocked(final_square):
                        self.step(final_square.file, final_square.rank, moving_card.card_name)
                        self.game.turn = 1 - self.game.turn
                        return GamePlayer.RETURN_CODE_MOVE_OK

                    else:
                        return GamePlayer.RETURN_CODE_MOVE_BLOCKED
                else:
                    return GamePlayer.RETURN_CODE_MOVE_BOARDER

    def use_virus_checker(self, file, rank):
        if self.virus_checker_counter != 0:
            raise RuntimeError("Already used")

        square = self.game.board.square_at(file, rank)

        enemy_card = square.player_card
        if enemy_card is None:
            raise RuntimeError("There's no card to check")

        elif enemy_card.card.card_type == "L" or enemy_card.card.card_type == "V":
            self.virus_checker_counter = self.virus_checker_counter + 1
            enemy_card.revealed = True

        else:
            raise RuntimeError("Invalid Card")
        self.game.turn = 1 - self.game.turn

    def install_firewall(self, file, rank):
        if self.firewall_count > 0:
            raise RuntimeError("Firewall already installed")
        else:

            square = self.game.board.square_at(file, rank)

            if square.player_card is None or square.square_type != "S":
                self.__place_card(square, self.my_cards["FW"])
                self.firewall_count = self.firewall_count + 1
                self.game.turn = 1 - self.game.turn
            else:
                raise RuntimeError("You can't put a firewall in a nonempty or Server Port square.")

    def uninstall_firewall(self, file, rank):
        if self.firewall_count < 1:
            raise RuntimeError("Firewall not installed")
        else:

            square = self.game.board.square_at(file, rank)

            if square.player_card.card.is_firewall():
                self.__remove_card(square.player_card)
                self.game.turn = 1 - self.game.turn
            else:
                raise RuntimeError("You can't place firewall on server ports or other cards")

    def place_line_boost(self, file, rank):
        if self.line_boosted is None:

            square = self.game.board.square_at(file, rank)

            if square.player_card.card.is_link() or square.player_card.card.is_virus():
                self.line_boosted = square.player_card
                self.game.turn = 1 - self.game.turn
            else:
                raise RuntimeError("Invalid Card")

    def detach_line_boost(self, file, rank):
        if self.line_boosted is not None:

            square = self.game.board.square_at(file, rank)

            if square.player_card == self.line_boosted:
                self.line_boosted = None
                self.game.turn = 1 - self.game.turn
            else:
                raise RuntimeError("Invalid Card")
        else:
            raise RuntimeError("You can't detach if you didn't attach")

    def use_404_not_found(self, first_card_name, second_card_name, switch):
        if self.count_404 == 0:
            first_card = self.my_cards[first_card_name]
            second_card = self.my_cards[second_card_name]
            if first_card.card.is_firewall() or second_card.card.is_firewall():
                raise RuntimeError("You can't touch firewalls with 404 not found")
            first_card.revealed = False
            second_card.revealed = False
            first_square = first_card.current_square
            second_square = second_card.current_square

            if switch:
                if first_card == self.line_boosted:
                    self.line_boosted = second_card
                elif second_card == self.line_boosted:
                    self.line_boosted = first_card
                self.__remove_card(first_card)
                self.__remove_card(second_card)
                self.__place_card(second_square, first_card)
                self.__place_card(first_square, second_card)

            self.game.turn = 1 - self.game.turn
            self.count_404 = self.count_404 + 1
        else:
            raise RuntimeError("Already used")

    @staticmethod
    def auto_line_boost_detach(game_player, file, rank):

        if game_player.line_boosted is not None:

            square = game_player.game.board.square_at(file, rank)

            if square.player_card == game_player.line_boosted:
                game_player.line_boosted = None
            else:
                raise RuntimeError("Invalid Card:", + square.player_card.card_name)

    @staticmethod
    def auto_line_boost_attach(game_player, file, rank):
        if game_player.line_boosted is None:

            square = game_player.game.board.square_at(rank, file)

            if square.player_card.card.is_link() or square.player_card.card.is_virus():
                game_player.line_boosted = square.player_card
            else:
                raise RuntimeError("Invalid Card")

    def is_terminating(self):
        if len(self.stack_area.viruses) == 4 or len(self.stack_area.links) == 4:
            self.game.started = False
            return True
        else:
            return False

    def is_winning(self):
        if len(self.stack_area.links) == 4:
            return True
        else:
            return False
