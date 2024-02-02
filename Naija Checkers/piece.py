
class Piece:
    def __init__(self, row, column, color, is_king, piece_id):
        self.row = row
        self.column = column
        self.color = color
        self.is_king = is_king
        self.piece_id = piece_id

    def get_north_east_direction(self):
        return 1

    def get_north_west_direction(self):
        return 1

    def get_south_east_direction(self):
        return 1

    def get_south_west_direction(self):
        return 1

    def update_piece_info(self, row, column):
        return
