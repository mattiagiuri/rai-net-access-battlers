class StackArea:
    def __init__(self):
        self.links = []
        self.viruses = []

    def to_string(self):
        result = ""
        for i in self.links:
            result = result + i.card_name + " "
        for i in self.viruses:
            result = result + i.card_name + " "
        return result
