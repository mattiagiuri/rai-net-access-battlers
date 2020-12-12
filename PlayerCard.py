class PlayerCard:
    def __init__(self, player, card, card_name):
        self.player = player
        self.card = card
        self.card_name = card_name
        self.current_square = None
        self.revealed = False
