from Game import Game
from Player import Player

new_player1 = Player('Jkans')
new_player1.nickname = "Jkans"

new_player2 = Player('Troller')
new_player2.nickname = "Troller"

new_game = Game(new_player1, new_player2)

assert new_game.game_players[1].my_cards["V0"].card.is_virus()


game_player_0 = new_game.game_players[0]

assert game_player_0.do_put_card_on_setup(1, 1, "V0")
assert game_player_0.do_put_card_on_setup(2, 1, "V1")
assert game_player_0.do_put_card_on_setup(3, 1, "V2")
assert game_player_0.do_put_card_on_setup(4, 2, "V3")
assert game_player_0.do_put_card_on_setup(5, 2, "L0")
assert game_player_0.do_put_card_on_setup(6, 1, "L1")
assert game_player_0.do_put_card_on_setup(7, 1, "L2")
assert game_player_0.do_put_card_on_setup(8, 1, "L3")

game_player_1 = new_game.game_players[1]

assert game_player_1.do_put_card_on_setup(1, 8, "V0")
assert game_player_1.do_put_card_on_setup(2, 8, "V1")
assert game_player_1.do_put_card_on_setup(3, 8, "V2")
assert game_player_1.do_put_card_on_setup(4, 7, "V3")
assert game_player_1.do_put_card_on_setup(5, 7, "L0")
assert game_player_1.do_put_card_on_setup(6, 8, "L1")
assert game_player_1.do_put_card_on_setup(7, 8, "L2")
assert game_player_1.do_put_card_on_setup(8, 8, "L3")
assert game_player_1.do_put_card_on_setup(8, 8, "L2")


assert len(new_game.game_players) == 2


print(new_game.to_string())
