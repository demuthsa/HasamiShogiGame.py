import os
import pygame
import HasamiShogiGame1
import math

# CONSTANTS
WINDOW_WIDTH = 630
WINDOW_HEIGHT = 700
HEIGHT_DIFF = WINDOW_HEIGHT - WINDOW_WIDTH
ROWS, COLS = 9, 9
SQUARE_SIZE = WINDOW_WIDTH / ROWS
RED = (180, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (252, 242, 183)
HIGHLIGHT = (0, 255, 255)
FPS = 80
# TITLE_FONT_SIZE = WINDOW_WIDTH // 7

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
pygame.display.set_caption("Hasami Shogi ")

sourceFileDir = os.path.dirname(os.path.abspath(__file__))
red_piece_og = pygame.image.load(os.path.join(sourceFileDir, "icons", "red_shogi.png"))
black_piece_og = pygame.image.load(os.path.join(sourceFileDir, "icons", "black_shogi.png"))
# Game Piece Images, scaled to fit the square size
# red_piece_og = pygame.image.load("/icons/red_shogi.png")
red_piece = pygame.transform.scale(red_piece_og, (SQUARE_SIZE, SQUARE_SIZE))


# black_piece_og = pygame.image.load("\icons\black_shogi.png")
black_piece = pygame.transform.scale(black_piece_og, (SQUARE_SIZE, SQUARE_SIZE))


# def showText(display_surface, fontName, textToDisplay, textColor):
#     """Displays the text on the surface of the pygame window
#     Args:
#         display_surface (_type_): the pygame surface to be drawn on
#         textToDisplay (str): desired text to be displayed
#         textColor (tuple): RGB colors (0~255, 0~255, 0~255)
#     """
    # custom_font = pygame.font.Font(fontName, TITLE_FONT_SIZE)
    # title_text = custom_font.render(textToDisplay, True, textColor)
    # title_text_rect = title_text.get_rect()
    # title_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    # display_surface.blit(title_text, title_text_rect)
    # pygame.display.update()


def mouse_pos_to_square(position):
    """Converts pygame's mouse click selection to a valid index for
    HasamiShogiGame.py
    Args:
        position (tuple): pygame's mouse position event
    Returns:
        str: the square's index that is selected
    """
    # mouse_x = math.floor(position[0] / (WINDOW_WIDTH / ROWS))
    # mouse_y = math.floor(position[1] / (WINDOW_HEIGHT / COLS)) + HEIGHT_DIFF
    #
    # return str(mouse_x) + str(mouse_y)
    mouse_x = math.floor(position[0] / (WINDOW_WIDTH / COLS))
    mouse_y = math.floor((position[1] - HEIGHT_DIFF) / ((WINDOW_HEIGHT - HEIGHT_DIFF) / ROWS))
    return str(mouse_x) + str(mouse_y)


def main():
    game = HasamiShogiGame1.HasamiShogiGame()
    clock = pygame.time.Clock()
    fontName = os.path.join(sourceFileDir, "font", "Kamikaze.ttf")
    # showText(screen, fontName, "HASAMI SHOGI", WHITE)
    pygame.time.wait(2500)

    clicks = []
    move_started = False
    while game.get_game_state() == "UNFINISHED":
        clock.tick(FPS)

        for event in pygame.event.get():
            # Exits if the user clicks on the Exit window button.
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = (mouse_pos_to_square(event.pos))
                if selection[1] == "-":
                    continue
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
                    # if move == True:
                    # print(f"Moving {source} → {destination}")
                    clicks = []

        # Fill the background with BOARD_COLOR
        screen.fill(BOARD_COLOR)

        # Draws the grid lines of the board
        for col in range(0, COLS):
            x = col * WINDOW_WIDTH // COLS
            pygame.draw.line(screen, (0, 0, 0), (x, HEIGHT_DIFF), (x, WINDOW_HEIGHT), width=2)
        for row in range(0, ROWS):
            y = row * WINDOW_HEIGHT // ROWS
            pygame.draw.line(screen, (0, 0, 0), (0, y + HEIGHT_DIFF), (WINDOW_WIDTH, y+HEIGHT_DIFF), width=2)

        # Displays the pieces on the game board
        for row in range(ROWS):
            for col in range(COLS):
                space = str(row) + str(col)
                if game.get_square_occupant(game.index_to_move(space)) == "RED":
                    # pygame.draw.circle(screen, RED, (SQUARE_SIZE * col + .5 * SQUARE_SIZE, SQUARE_SIZE * row + .5 * SQUARE_SIZE), .4 * SQUARE_SIZE, 40)
                    # BLIT the red piece surface object in the correct square
                    screen.blit(red_piece, (SQUARE_SIZE * col, SQUARE_SIZE * row + HEIGHT_DIFF))
                    # pygame.draw.circle(screen, RED, (SQUARE_SIZE * row, SQUARE_SIZE * col), 75)

                elif game.get_square_occupant(game.index_to_move(space)) == "BLACK":
                    # pygame.draw.circle(screen, BLACK, (SQUARE_SIZE * col + .5 * SQUARE_SIZE, SQUARE_SIZE * row + .5 * SQUARE_SIZE), .4 * SQUARE_SIZE, 40)
                    screen.blit(black_piece, (SQUARE_SIZE * col, SQUARE_SIZE * row + HEIGHT_DIFF))
                else:
                    pass

            # Display the current player at the top of the board
            font = pygame.font.SysFont(None, 40)
            color = (0,0,0)
            # win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

            player_text = font.render(game.get_active_player(), True, color)
            screen.blit(
                player_text,
                ((screen.get_width() - player_text.get_width()) // 2, 15)
            )
            # Display the total number of pieces for Black
            # font = pygame.font.SysFont(None, 40)
            black_remaining = font.render(f"Black: {9 - game.get_num_captured_pieces('BLACK')}", True, color)
            screen.blit(
                black_remaining,
                (20, 25)
            )
            # Display the total number of pieces for Red
            red_remaining = font.render(f"Red: {9 - game.get_num_captured_pieces('RED')}", True, color)
            screen.blit(
                red_remaining,
                (screen.get_width() - red_remaining.get_width() - 20, 25)
            )


        # Displays the match winner
        if game.get_game_state() == "RED_WON":
            showText(screen, fontName, "RED WINS", RED)
        elif game.get_game_state() == "BLACK_WON":
            showText(screen, fontName, "BLACK WINS", BLACK)


        # Updates the game screen
        pygame.display.update()
        # pygame.time.wait(60)

    print("Thank you for playing! The game will be closing shortly.")
    pygame.time.wait(4000)
    pygame.quit()



if __name__ == "__main__":
    main()