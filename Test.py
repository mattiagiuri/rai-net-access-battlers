from Card import *
from Player import *
from Board import *
from PlayerCard import *
import numpy

print(numpy.square(10))

new_card = Card.create_link()
assert new_card.is_link()

new_player = Player('Matt')
new_player.nickname = "Matt"
assert new_player.nickname == "Matt"

card1 = PlayerCard(new_player, new_card, 'L')

my_board = Board()
my_square = my_board.square_at(4, 3)
my_square.player_card = card1

assert my_board.square_at(4, 3).player_card.card.is_link()
assert my_board.square_at(4, 3).player_card.player.nickname == "Matt"

# print(new_card.card_type)
# print(new_card.is_link())
