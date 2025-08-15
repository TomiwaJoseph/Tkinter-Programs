
class Card:
    def __init__(self, card_id, card_type, card_value, card_status="hidden"):
        self.id = card_id
        self.type = card_type
        self.value = card_value
        self.status = card_status
