# Author: Sam
# Date: 24 Nov 2021
# Description: Write a class named HasamiShogiGame for playing an abstract board game called hasami shogi. We'll be using
#              the rules for "Variant 1" on the Wikipedia page, including the diagram of the starting position. Custodian
#              captures may be made on multiple sides (up to 3 sides) of the moved piece. For example if the black piece on
#              square h6 in the diagram below moves to square c6, then the red pieces at c4, c5, and b6 would be captured.
#              If instead, the black piece at h6 moves to h1, then the red pieces at e1, f1, g1, and i1 would be captured.
#              Locations on the board will be specified using "algebraic notation", with rows labeled a-i and rows labeled 1-9


class HasamiShogiGame:
    """A class to represent Hasami Shogi game, played by two players. Black always starts first. Returns True if a move is valid, otherwise returns False. """

    def __init__(self):
        """Constructor for HasamiShogiGame class. Takes no parameters. Initializes the required data members: board, current state of game, and active player. All data members are private."""
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
        """A method that returns the game board"""
        return self._board

    def get_game_state(self):
        """A method that returns the game state"""
        return self._current_state

    def set_game_state(self):
        """A method that sets the game state"""
        captured = self.get_num_captured_pieces("BLACK")
        if captured >= 8:
            self._current_state = "RED_WON"
        else:
            captured = self.get_num_captured_pieces("RED")
            if captured >= 8:
                self._current_state = "BLACK_WON"


    def get_active_player(self):
        """A method that returns the active player"""
        return self._active_player

    def set_active_player(self):
        """A method that sets the active player"""
        if self._active_player == "BLACK":
            self._active_player = "RED"
        elif self._active_player == "RED":
            self._active_player = "BLACK"


    def get_num_captured_pieces(self, color):
        """A method that takes as a parameter a color and returns the number of captured pieces for that color"""
        count = 0

        if color == "BLACK":
            for row in self.get_board():
                count += row.count("B")
        elif color == "RED":
            for row in self.get_board():
                count += row.count("R")
        return 9 - count

    def get_row_column(self, space):
        """A method that returns the row and column of a given space"""
        # Return None if the space parameter is None
        if space is None:
            return None, None
        # Check if the space parameter is a valid square on the board
        if len(space) != 2 or space[0] not in "abcdefghi" or space[1] not in "123456789":
            return None, None
        # Parse the row and column indices from the space parameter
        row = ord(space[0]) - ord("a")
        column = int(space[1]) - 1
        return row, column

    # def get_square_occupant(self, space):
    #     """A method that returns the occupant of a given space"""
    #     index = self.move_to_index(space)
    #     row = int(index[0])
    #     column = int(index[1])
    #     # row, column = self.get_row_column(space)
    #     # Return None if the row and column indices are None
    #     if row is None or column is None:
    #         return None
    #     if self.get_board()[row][column] == "R":
    #         return "RED"
    #     elif self.get_board()[row][column] == "B":
    #         return "Black"
    #     else:
    #         return None

    def set_square_occupant(self, space, piece):
        """A method that takes as a parameter a space and piece and sets the occupant of a given space"""

        row, column = self.get_row_column(space)

        self.get_board()[row][column] = piece

    def traverse(self, row, column, direction, player, opponent):
        """A method that takes as a parameter a row, column, direction, player, and opponent. This method is used to check for captured pieces"""
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

        #Check corner captures
        if self.get_board()[1][2] == "B" and self.get_board()[2][1] == "B":
                if self.get_board()[1][1] == "R":
                    result.append(self.get_board()[1][1])
                    self.get_board()[1][1] = "."
        if self.get_board()[1][2] == "R" and self.get_board()[2][1] == "R":
                if self.get_board()[1][1] == "B":
                    result.append(self.get_board()[1][1])
                    self.get_board()[1][1] = "."
        if self.get_board()[1][8] == "B" and self.get_board()[2][9] == "B":
                if self.get_board()[1][9] == "R":
                    result.append(self.get_board()[1][9])
                    self.get_board()[1][9] = "."
        if self.get_board()[1][2] == "R" and self.get_board()[2][1] == "R":
                if self.get_board()[1][1] == "B":
                    result.append(self.get_board()[1][9])
                    self.get_board()[1][9] = "."
        if self.get_board()[8][1] == "B" and self.get_board()[9][2] == "B":
                if self.get_board()[9][1] == "R":
                    result.append(self.get_board()[9][1])
                    self.get_board()[9][1] = "."
        if self.get_board()[8][1] == "R" and self.get_board()[9][2] == "R":
                if self.get_board()[9][1] == "B":
                    result.append(self.get_board()[9][1])
                    self.get_board()[9][1] = "."
        if self.get_board()[8][9] == "B" and self.get_board()[9][8] == "B":
                if self.get_board()[9][9] == "R":
                    result.append(self.get_board()[9][9])
                    self.get_board()[9][9] = "."
        if self.get_board()[8][9] == "R" and self.get_board()[9][8] == "R":
                if self.get_board()[9][9] == "B":
                    result.append(self.get_board()[9][9])
                    self.get_board()[9][9] = "."

        return []

    def current_piece(self, position): #mouse_pos_to_square):
        #space = mouse_pos_to_square(position)
        row, column = self.get_row_column(position)#space)
        return self.get_board()[row][column]



    def make_move(self, current_space, new_space):
        """A method that takes as a parameter current space and new space. This method is used to make an active move. If a move is invalid it will return False"""
        current_piece = self.current_piece(current_space)

        # if self.get_active_player() == "BLACK" and current_piece != "B":
        #     return False
        #
        # if self.get_active_player() == "RED" and current_piece != "R":
        #     return False

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

        # Register invalid move if pieces in the way

        # piece = current_space
        current_column = int(current_space[1])
        current_row = ord(current_space[0]) - ord("a") + 1
        new_column = int(new_space[1])
        new_row = ord(new_space[0]) - ord("a") + 1

        if current_column > new_column and current_row == new_row:  # Left
            for i in range(current_column-1, new_column-1, -1):
                if self.get_board()[current_row][i] != ".":
                    return False
        if current_column < new_column and current_row == new_row:  # Right
            for i in range(current_column+1, new_column+1, 1):
                if self.get_board()[current_row][i] != ".":
                    return False
        if current_row < new_row and current_column == new_column: # Up
            for i in range(current_row+1, new_row+1, 1):
                if self.get_board()[i][current_column] != ".":
                    return False
        if current_row > new_row and current_column == new_column:  # Down
            for i in range(current_row-1, new_row-1, -1):
                if self.get_board()[i][current_column] != ".":
                    return False
        # moving the piece

        self.set_square_occupant(current_space, ".")
        self.set_square_occupant(new_space, current_piece)

        # Check if captured

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
                self.set_game_state()

        else:
            self.set_active_player()
            captured = self.get_num_captured_pieces("RED")
            if captured >= 8:
                self.set_game_state()
        return True
    def index_to_move(self, index):
        """Converts the index to a move for the _game_board's list parameters
        allowing for spaces of a-i and 1-9.

        Returns:
            move (str): the game board space as a string
        """
        allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
        row = int(index[0])
        row = allowed[row]
        column = int(index[1]) + 1
        # print(f"the row is {row}, and the column is {column}")
        move = row + str(column)
        return move

    def get_square_occupant(self, square=""):
        """Determines if the square is occupied or not. Note: Needs to be "indexed" first.
        Use function move_to_index() prior to using this function.
        Returns:
            "RED":   if square is occupied by a "R" piece
            "BLACK": if square is occupied by a "B" piece
            "NONE":  if square is empty; occupied by a "_"
        Args:
            square (str, optional): array index (0-8)(0-8). Defaults to "".
        """
        print(f"Square being checked for occupant: {square}")
        print(f"board: {self._board}")
        index = self.move_to_index(square)
        row_index = int(index[0])
        print({row_index})
        col_index = int(index[1])+1
        print({col_index})
        print({self._board[row_index][col_index]})
        if self._board[row_index][col_index] == "B":
            print(f"Black occupies {square}")
            return "BLACK"
        elif self._board[row_index][col_index] == "R":
            print(f"Red occupies {square}")
            return "RED"
        elif self._board[row_index][col_index] == ".":
            print(f"...its empty...")
            return "NONE"
        else:
            print("Something is wrong in get_square_occupant")
            return False

    def move_to_index(self, move):
        """Converts the move to an index for the _game_board's list parameters
        allowing for spaces of a-i and 1-9.
        Returns:
            False: an invalid square is being requested
            Index (str):   string for the list of lists
        """
        allowed = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

        if len(move) != 2:
            print("INVALID SQUARE, outside of limits")
            return False
        if int(move[1]) not in range(1, 10):
            print("INVALID SQUARE, outside of limits")
            return False
        if move[0].lower() not in allowed:
            print("INVALID SQUARE, outside of limits")
            return False
        for i in range(len(allowed)):
            if allowed[i] == move[0].lower():
                # print(i+1, move[1])
                index = str(i) + str(int(move[1]) - 1)
                # print(f"The converted index is now: {index}")
                return index
        # print("Reached end where its false")
        return False


    def print_board(self):
        """A method used to print the game board"""
        for row in self.get_board():
            print(*row)



game = HasamiShogiGame()
game.print_board()
print()
print()


move_result = game.make_move('i2', 'b2') # Black
game.print_board()
print(move_result)
print()
move_result = game.make_move('a1', 'b1') # Red
game.print_board()
print(move_result)
print()
# move_result = game.make_move('i3', 'h3') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('b1', 'b3') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('i8', 'h8') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a8', 'i8') # Red
# game.print_board()
# print(move_result)
# print()
# print(game.get_num_captured_pieces("RED"))
# print(game.get_num_captured_pieces("BLACK"))
# move_result = game.make_move('i4', 'a4') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a6', 'f6') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('i6', 'a6') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('e1', 'e2') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('i5', 'f5') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a8', 'f8') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('i9', 'f9') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a7', 'b7') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('i7', 'f7') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('e2', 'b2') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('f1', 'f2') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('b7', 'e7') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('f2', 'c2') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a9', 'b9') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a6', 'd6') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('b9', 'a9') # Red
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('d6', 'd7') # Black
# game.print_board()
# print(move_result)
# print()
# move_result = game.make_move('a9', 'a8') # Red
# game.print_board()
# print(move_result)
# print()
#

#
#
#
# print(game.get_active_player())
# print(game.get_game_state())
# print(game.get_num_captured_pieces("RED"))

# print(game.get_active_player())
# print(game.get_square_occupant('a4'))
# print(game.get_game_state())