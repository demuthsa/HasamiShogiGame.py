# Author: Sam DeMuth
# Date: 24 Nov 2021
# Description: Hasami Shogi


class HasamiShogiGame:

    def __init__(self):
        self._board = [
            [" ", 1, 2, 3, 4, 5, 6, 7, 8, 9],
            ["a", "R", "R", "R", "R", "R", "R", "R", "R", "R"],
            ["b", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["c", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["d", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["e", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["f", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["g", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["h", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ["i", "B", "B", "B", "B", "B", "B", "B", "B", "B"]
        ]
        self._current_state = "UNFINISHED"
        self._active_player = "BLACK"

    def get_board(self):
        return self._board

    def get_game_state(self):
        return self._current_state

    def get_active_player(self):
        return self._active_player

    def set_active_player(self):
        if self._active_player == "BLACK":
            self._active_player = "RED"
        elif self._active_player == "RED":
            self._active_player = "BLACK"


    def get_num_captured_pieces(self, color):
        count = 0

        if color == "BLACK":
            for row in self.get_board():
                count += row.count("B")
        elif color == "RED":
            for row in self.get_board():
                count += row.count("R")
        return 9 - count

    def get_row_column(self, space):

        row = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i"].index(space[0])
        column = int(space[1])

        return row, column

    def get_square_occupant(self, space):

        row, column = self.get_row_column(space)

        if self.get_board()[row][column] == "R":
            return "RED"
        elif self.get_board()[row][column] == "B":
            return "Black"
        else:
            return None

    def set_square_occupant(self, space, piece):

        row, column = self.get_row_column(space)

        self.get_board()[row][column] = piece

    def traverse(self, row, column, direction, player, opponent):

        result = []

        current_column = column
        current_row = row

        if direction == "up":
            current_row -= 1
            while current_row >= 1:
                if self.get_board()[current_row][column] == opponent:
                    result.append((current_row, column))
                elif self.get_board()[current_row][column] == player:
                    return result
                elif self.get_board()[current_row][column] == ".":
                    return []
                current_row -= 1

        if direction == "down":
            current_row += 1
            while current_row <= 9:
                if self.get_board()[current_row][column] == opponent:
                    result.append((current_row, column))
                elif self.get_board()[current_row][column] == player:
                    return result
                elif self.get_board()[current_row][column] == ".":
                    return []
                current_row += 1

        if direction == "left":
            current_column -= 1
            while current_column >= 1:
                if self.get_board()[row][current_column] == opponent:
                    result.append((row, current_column))
                elif self.get_board()[row][current_column] == player:
                    return result
                elif self.get_board()[row][current_column] == ".":
                    return []
                current_column -= 1

        if direction == "right":
            current_column += 1
            while current_column <= 9:
                if self.get_board()[row][current_column] == opponent:
                    result.append((row, current_column))
                elif self.get_board()[row][current_column] == player:
                    return result
                elif self.get_board()[row][current_column] == ".":
                    return []
                current_column += 1
        return []

    def current_piece(self, space):
        row, column = self.get_row_column(space)

        return self.get_board()[row][column]



    def make_move(self, current_space, new_space):
        current_piece = self.current_piece(current_space)

        if self.get_active_player() == "BLACK" and current_piece != "B":
            return False

        if self.get_active_player() == "RED" and current_piece != "R":
            return False

        new_piece = self.current_piece(new_space)

        if new_piece != ".":
            return False

        if self.get_game_state() == "BLACK_WON":
            return False

        if self.get_game_state() == "RED_WON":
            return False

        current_row, current_column = self.get_row_column(current_space)
        new_row, new_column = self.get_row_column(new_space)

        # Check if move is diagonally
        if (current_row != new_row) and (current_column != new_column):
            return False

        ## moving the piece

        self.set_square_occupant(current_space, ".")
        self.set_square_occupant(new_space, current_piece)

        ### Check if captured

        directions = ["up", "down", "left", "right"]

        if self.get_active_player() == "BLACK":
            for direction in directions:
                captured_positions = self.traverse(new_row, new_column, direction, "B", "R")
                for row, column in captured_positions:
                    self.get_board()[row][column] = "."


        elif self.get_active_player() == "RED":
            for direction in directions:
                captured_positions = self.traverse(new_row, new_column, direction, "R", "B")
                for row, column in captured_positions:
                    self.get_board()[row][column] = "."


        if self.get_active_player() == "RED":
            self.set_active_player()
            captured = self.get_num_captured_pieces("BLACK")
            if captured >= 8:
                self._current_state = "RED_WON"

        else:
            self.set_active_player()
            captured = self.get_num_captured_pieces("RED")
            if captured >= 8:
                self._current_state = "BLACK_WON"
        return True

    def print_board(self):
        for row in self.get_board():
            print(*row)



game = HasamiShogiGame()
game.print_board()
print()
print()

# moves = [
#     ("i1", "f1"),  # Black
#     ("a2", "f2"),  # Red
#     ("i3", "f3"),  # Black
#     ("i2", "h2"),  # Black
#     ("i5", "f5"),
#     ("a1", "c1")
# ]
#
# for move in moves:
#     current_space, new_space = move
#     game.make_move(current_space, new_space)
#     game.print_board()
#     print()
#     print()

# print(game.print_board())


move_result = game.make_move('i1', 'f1') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a2', 'f2') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i3', 'f3') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a4', 'f4') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i2', 'a2') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a1', 'e1') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i4', 'a4') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a6', 'f6') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i6', 'a6') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('e1', 'e2') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i5', 'f5') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a8', 'f8') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i9', 'f9') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a7', 'b7') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('i7', 'f7') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('e2', 'b2') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('f1', 'f2') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('b7', 'e7') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('f2', 'c2') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a9', 'b9') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('a6', 'd6') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('b9', 'a9') # Red
game.print_board()
print(move_result)
print()
move_result = game.make_move('d6', 'd7') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a9', 'a8') # Red
game.print_board()
print(move_result)
print()




print(game.get_active_player())
print(game.get_game_state())
print(game.get_num_captured_pieces("RED"))

# print(game.get_active_player())
# print(game.get_square_occupant('a4'))
# print(game.get_game_state())