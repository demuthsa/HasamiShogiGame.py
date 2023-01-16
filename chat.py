import pygame
from pygame.locals import *
import HasamiShogiGame
import math
import sys


# Constants
window_width = 700
window_height = 700
SQUARE_SIZE = 60
gap = 70


# Calculate the number of rows and columns on the board
num_rows = 10
num_columns = 10

# Initialize Pygame
pygame.init()

# Window caption
screen = pygame.display.set_mode([window_width, window_height])
pygame.display.set_caption("Hasami Shogi")

# Create a list to store the Rect objects representing each square on the board
squares = []

# Initialize the Rect objects and add them to the list
for row in range(num_rows):
    for column in range(num_columns):
        # Calculate the x coordinate to center the board
        x = (window_width - num_columns * SQUARE_SIZE) // 2 + column * SQUARE_SIZE
        y = row * SQUARE_SIZE + gap
        rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        squares.append(rect)

# Create a HasamiShogiGame object and retrieve the game board
game = HasamiShogiGame.HasamiShogiGame()
board = game.get_board()

# Variables to store the position of the selected piece and the square it is being moved to
selected_piece = None
target_square = None

# Set up the font for drawing labels
font = pygame.font.Font(None, 36)

# Set the window size and create a display surface
window_size = (window_width, window_height)
display_surface = pygame.display.set_mode(window_size)


def mouse_pos_to_square(position):
    """Converts pygame's mouse click selection to a valid index for
    HasamiShogiGame.py
    Args:
        position (tuple): pygame's mouse position event
    Returns:
        str: the square's index that is selected
    """

    col = (position[0] -110) // SQUARE_SIZE
    row = (position[1] - 130) // SQUARE_SIZE
    print('row', row, 'col', col)

    mouse_y = (position[0] - 110) // SQUARE_SIZE
    mouse_x = (position[1] - 130) // SQUARE_SIZE
    return str(mouse_x) + str(mouse_y)

# Main game loop
def main():
    game = HasamiShogiGame.HasamiShogiGame()

    # Create a list to store the Rect objects representing each square on the board
    clicks = []
    while game.get_game_state() == "UNFINISHED":

        # Initialize the Rect objects and add them to the list
        for row in range(num_rows):
            for column in range(num_columns):
                # Calculate the x coordinate to center the board
                x = (window_width - num_columns * SQUARE_SIZE) // 2 + column * SQUARE_SIZE
                y = row * SQUARE_SIZE + gap
                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                squares.append(rect)

        for event in pygame.event.get():
            # Exits if the user clicks on the Exit window button.
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Background color
            display_surface.fill((252, 242, 183))

            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = (mouse_pos_to_square(event.pos))
                allowed_sq = game.index_to_move(selection)
                if len(clicks) == 0 and game.get_square_occupant(allowed_sq) == game.get_active_player():
                    clicks.append(selection)
                    # ACTION: Add highlighted square for desired piece to be moved. Would also require removal.
                    # pygame.draw.rect(screen, HIGHLIGHT, pygame.rect(SQUARE_SIZE * int(selection[0]),  SQUARE_SIZE, SQUARE_SIZE * int(selection[0]) + .5 * SQUARE_SIZE), .4 * SQUARE_SIZE, 1)
                    # pygame.draw.rect(screen, HIGHLIGHT, pygame.Rect(50, 50, 100, 100), 5)
                elif len(clicks) == 1 and game.get_square_occupant(allowed_sq) == "NONE":
                    clicks.append(selection)
                    source = game.index_to_move(clicks[0])
                    destination = game.index_to_move(clicks[1])
                    print(f"Move attempt: {source} → {destination}")
                    move = game.make_move(source, destination)
                    print(move)
                    if move == True:
                        print(f"Moving {source} → {destination}")
                        pygame.draw.circle(display_surface, (0, 0, 0), rect.center, SQUARE_SIZE // 2 - 10)
                    clicks = []

        # Iterate through the list of squares and draw each one
        for rect in squares:
            pygame.draw.rect(display_surface, (0, 0, 0), rect, 1)

            # Calculate the x coordinate to center the labels
            x = (window_width - num_columns * SQUARE_SIZE) // 2 + SQUARE_SIZE // 2

            # Display the labels in the first column inside the squares
            for i in range(1, num_rows):
                text = font.render(chr(ord('a') + i - 1), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = squares[i * num_columns].center
                display_surface.blit(text, text_rect)

            # Display the labels in the first row inside the squares
            for i in range(num_columns - 1):
                text = font.render(str(i + 1), True, (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = squares[i + 1].center
                display_surface.blit(text, text_rect)

            # Iterate through the game board and draw the pieces at the correct positions
            for row_index, row in enumerate(board):
                for column_index, piece in enumerate(row):
                    # Get the Rect object corresponding to the current square
                    rect = squares[row_index * num_columns + column_index]
                    space = str(row_index) + str(column_index)
                    # Draw the piece at the center of the square
                    if piece == "R":
                        pygame.draw.circle(display_surface, (255, 0, 0), rect.center, SQUARE_SIZE // 2 - 10)
                    elif piece == "B":
                        pygame.draw.circle(display_surface, (0, 0, 0), rect.center, SQUARE_SIZE // 2 - 10)

                        # Display the current player at the top of the board
                        color = (0, 0, 0)

                        # win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                        player_text = font.render(game.get_active_player(), True, color)
                        screen.blit(player_text, ((screen.get_width() - player_text.get_width()) // 2, 15))

                        # Display the total number of pieces for Black
                        black_remaining = font.render(f"Black: {9 - game.get_num_captured_pieces('BLACK')}", True, color)
                        screen.blit(black_remaining, (20, 25))

                        # Display the total number of pieces for Red
                        red_remaining = font.render(f"Red: {9 - game.get_num_captured_pieces('RED')}", True, color)
                        screen.blit(red_remaining, (screen.get_width() - red_remaining.get_width() - 20, 25))


        # Displays the match winner
        if game.get_game_state() == "RED_WON":
            showText(screen, fontName, "RED WINS", RED)

        elif game.get_game_state() == "BLACK_WON":
            showText(screen, fontName, "BLACK WINS", BLACK)

        # Update the display surface
        pygame.display.update()


    print("Thank you for playing! The game will be closing shortly.")
    pygame.time.wait(4000)
    pygame.quit()

if __name__ == "__main__":
    main()
