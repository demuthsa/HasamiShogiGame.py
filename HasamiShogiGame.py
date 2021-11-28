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

    def get_game_state(self):
        return self._current_state

    def get_active_player(self):
        return self._active_player

    def get_num_captured_pieces(self, color):
        count = 0

        if color == "BLACK":
            for row in self._board:
                count += row.count("B")
        elif color == "RED":
            for row in self._board:
                count += row.count("R")
        return count

    def get_row_column(self, space):

        row = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i"].index(space[0])
        column = int(space[1])

        return row, column

    def get_square_occupant(self, space):

        row, column = self.get_row_column(space)

        return self._board[row][column]

    def set_square_occupant(self, space, piece):

        row, column = self.get_row_column(space)

        self._board[row][column] = piece

    def traverse(self, row, column, direction, player, opponent):

        result = []

        current_column = column
        current_row = row

        if direction == "up":
            current_row -= 1
            while current_row >= 1:
                if self._board[current_row][column] == opponent:
                    result.append((current_row, column))
                elif self._board[current_row][column] == player:
                    return result
                elif self._board[current_row][column] == ".":
                    return []
                current_row -= 1

        if direction == "down":
            current_row += 1
            while current_row <= 9:
                if self._board[current_row][column] == opponent:
                    result.append((current_row, column))
                elif self._board[current_row][column] == player:
                    return result
                elif self._board[current_row][column] == ".":
                    return []
                current_row += 1

        if direction == "left":
            current_column -= 1
            while current_column >= 1:
                if self._board[row][current_column] == opponent:
                    result.append((row, current_column))
                elif self._board[row][current_column] == player:
                    return result
                elif self._board[row][current_column] == ".":
                    return []
                current_column -= 1

        if direction == "right":
            current_column += 1
            while current_column <= 9:
                if self._board[row][current_column] == opponent:
                    result.append((row, current_column))
                elif self._board[row][current_column] == player:
                    return result
                elif self._board[row][current_column] == ".":
                    return []
                current_column += 1
        return []

    def make_move(self, current_space, new_space):
        current_piece = self.get_square_occupant(current_space)

        if self._active_player == "BLACK" and current_piece != "B":
            return False

        if self._active_player == "RED" and current_piece != "R":
            return False

        new_piece = self.get_square_occupant(new_space)

        if new_piece != ".":
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

        if self._active_player == "BLACK":
            for direction in directions:
                captured_positions = self.traverse(new_row, new_column, direction, "B", "R")
                for row, column in captured_positions:
                    self._board[row][column] = "."


        elif self._active_player == "RED":
            for direction in directions:
                captured_positions = self.traverse(new_row, new_column, direction, "R", "B")
                for row, column in captured_positions:
                    self._board[row][column] = "."


        if self._active_player == "RED":
            self._active_player = "BLACK"
            captured = self.get_num_captured_pieces("BLACK")
            if captured <= 1:
                self._current_state = "RED_WON"

        else:
            self._active_player = "RED"
            captured = self.get_num_captured_pieces("RED")
            if captured <= 1:
                self._current_state = "BLACK_WON"

        return True

    def print_board(self):
        for row in self._board:
            print(*row)
        return


# game = HasamiShogiGame()
# game.print_board()
# print()
# print()

# moves = [
#     ("i1", "f1"),  # Black
#     ("a2", "f2"),  # Red
#     ("i3", "f3"),  # Black
# ]
#
# for move in moves:
#     current_space, new_space = move
#     game.make_move(current_space, new_space)
#     game.print_board()
#     print()
#     print()


# game = HasamiShogiGame()
# print(game.print_board())