class Card:
    TYPE_LINK = "L"
    TYPE_VIRUS = "V"
    TYPE_BOOST_LINE = "BL"
    TYPE_FIREWALL = "FW"
    TYPE_404_NOT_FOUND = "NF"
    TYPE_VIRUS_CHECKER = "VC"

    def __init__(self, card_type):
        self.card_type = card_type

    def is_link(self):
        return self.card_type == Card.TYPE_LINK

    def is_virus(self):
        return self.card_type == Card.TYPE_VIRUS

    def is_boost_line(self):
        return self.card_type == Card.TYPE_BOOST_LINE

    def is_firewall(self):
        return self.card_type == Card.TYPE_FIREWALL

    def is_404_not_found(self):
        return self.card_type == Card.TYPE_404_NOT_FOUND

    def is_virus_checker(self):
        return self.card_type == Card.TYPE_VIRUS_CHECKER

    @staticmethod
    def create_link():
        return Card(Card.TYPE_LINK)

    @staticmethod
    def create_virus():
        return Card(Card.TYPE_VIRUS)

    @staticmethod
    def create_boost_line():
        return Card(Card.TYPE_BOOST_LINE)

    @staticmethod
    def create_firewall():
        return Card(Card.TYPE_FIREWALL)

    @staticmethod
    def create_404_not_found():
        return Card(Card.TYPE_404_NOT_FOUND)

    @staticmethod
    def create_virus_checker():
        return Card(Card.TYPE_VIRUS_CHECKER)
