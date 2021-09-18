"""
Play chess against an AI
"""
import random
import os
import sys
import time

# niklasf/python-chess is licensed under GPL-3.0
import chess
import pygame as pg
from pygame import gfxdraw
import termcolor

import chess50

# Screen size
SIZE = WIDTH, HEIGHT = 500, 600

# Fonts
REGULAR_FONT = os.path.join('assets', 'fonts', 'JetBrainsMono-Regular.ttf')
BOLD_FONT = os.path.join('assets', 'fonts', 'JetBrainsMono-Bold.ttf')

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
HIGHLIGHT = (16, 128, 255)

# Square constants
CORNER_RADIUS = 10
SQUARE_SIZE = 50
SQUARE_ORIGIN = (
    WIDTH / 2 - SQUARE_SIZE * 4,
    HEIGHT / 2 - SQUARE_SIZE * 4
)


def main():

    # Initialize pygame
    pg.init()
    pg.display.set_caption('chess50')
    screen = pg.display.set_mode(SIZE)

    # Font sizes
    label_font = pg.font.Font(BOLD_FONT, 12)
    message_font = pg.font.Font(REGULAR_FONT, 20)

    # Chess piece icons
    icon = {}
    for piece in 'PNBRQKpnbrqk':
        side = 'w' if piece.isupper() else 'b'
        path = os.path.join('assets', 'images', side + piece + '.svg')
        icon[piece] = pg.image.load(path)

    # Initialize players
    user = None
    ai = chess50.ChessAI()
    ai_turn = False

    # Set up chessboard
    board = chess.Board()

    selected_piece = None
    pawn_promoted = False
    game_over = False
    user_resigned = False

    while True:

        # Exit condition
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill(BLACK)

        # Let user choose a side
        if user is None:

            # Game title
            title = message_font.render("chess50", True, WHITE)
            title_rect = title.get_rect()
            title_rect.center = WIDTH / 2, HEIGHT * 11 / 12
            screen.blit(title, title_rect)

            # Play as White button
            play_white_button = pg.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT * 3 / 10), 32)
            draw_circle(screen, WHITE, (WIDTH / 2, HEIGHT * 3 / 10), 33)
            play_white = icon['K']
            play_white_rect = play_white.get_rect()
            play_white_rect.center = play_white_button.center
            screen.blit(play_white, play_white_rect)

            # Play as random side button
            play_random_button = pg.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), 49)
            draw_circle(screen, WHITE, (WIDTH / 2, HEIGHT / 2), 50)
            play_random = pg.image.load(os.path.join('assets', 'images', 'random.png'))
            play_random_rect = play_random.get_rect()
            play_random_rect.center = play_random_button.center
            screen.blit(play_random, play_random_rect)

            # Play as Black button
            play_black_button = pg.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT * 7 / 10), 32)
            draw_circle(screen, WHITE, (WIDTH / 2, HEIGHT * 7 / 10), 33)
            play_black = icon['k']
            play_black_rect = play_black.get_rect()
            play_black_rect.center = play_black_button.center
            screen.blit(play_black, play_black_rect)

            # Check which Play button was clicked
            if pg.mouse.get_pressed()[0]:
                mouse = pg.mouse.get_pos()
                if play_white_button.collidepoint(mouse):
                    time.sleep(0.2)
                    user = chess.WHITE
                elif play_random_button.collidepoint(mouse):
                    time.sleep(0.2)
                    user = random.randint(0, 1)
                elif play_black_button.collidepoint(mouse):
                    time.sleep(0.2)
                    user = chess.BLACK
                termcolor.cprint("If the text is green, the AI thinks it is winning;", 'green')
                termcolor.cprint("losing if it is red", 'red')
                print()
                print("Move  Value")

            # Flip the ranks and files depending on which side is the user
            if user == chess.WHITE:
                ranks = chess.RANK_NAMES[::-1]
                files = chess.FILE_NAMES
            else:
                ranks = chess.RANK_NAMES
                files = chess.FILE_NAMES[::-1]

        else:  # if the game has started

            squares = []
            occupied = board.piece_map()

            for i, rank in enumerate(ranks):
                row = []
                for j, file in enumerate(files):

                    # Squares
                    square_rect = pg.Rect(
                        SQUARE_ORIGIN[0] + SQUARE_SIZE * j,
                        SQUARE_ORIGIN[1] + SQUARE_SIZE * i,
                        SQUARE_SIZE,
                        SQUARE_SIZE
                    )

                    # Draw chessboard with rounded corners
                    square_color = (
                        HIGHLIGHT if selected_piece and selected_piece == file + rank else
                        WHITE if (i + j) % 2 == 0 else
                        GRAY
                    )
                    if i == 0 and j == 0:
                        pg.draw.rect(
                            screen,
                            square_color,
                            square_rect,
                            border_top_left_radius=CORNER_RADIUS
                        )
                    elif i == 0 and j == 7:
                        pg.draw.rect(
                            screen,
                            square_color,
                            square_rect,
                            border_top_right_radius=CORNER_RADIUS
                        )
                    elif i == 7 and j == 0:
                        pg.draw.rect(
                            screen,
                            square_color,
                            square_rect,
                            border_bottom_left_radius=CORNER_RADIUS
                        )
                    elif i == 7 and j == 7:
                        pg.draw.rect(
                            screen,
                            square_color,
                            square_rect,
                            border_bottom_right_radius=CORNER_RADIUS
                        )
                    else:
                        pg.draw.rect(
                            screen,
                            square_color,
                            square_rect
                        )

                    square = chess.parse_square(file + rank)

                    # Show legal moves visually after selecting a piece to move
                    if selected_piece:
                        if not selected_piece == file + rank:
                            try:
                                move = board.find_move(
                                    chess.parse_square(selected_piece),
                                    chess.parse_square(file + rank)
                                )

                                if move in board.legal_moves:

                                    # Legal moves to empty squares
                                    if square not in occupied:
                                        draw_circle(screen, HIGHLIGHT, square_rect.center, 7)

                                    # Pieces that can be captured and rooks in castling
                                    else:
                                        pg.draw.rect(screen, HIGHLIGHT, square_rect)
                                        pg.draw.rect(
                                            screen,
                                            WHITE if (i + j) % 2 == 0 else GRAY,
                                            square_rect,
                                            border_radius=15
                                        )
                            except ValueError:
                                pass

                    # Rank and file names
                    if j == 0:
                        rank_name = label_font.render(
                            rank, True,
                            GRAY if (i + j) % 2 == 0 else WHITE
                        )
                        rank_name_rect = rank_name.get_rect()
                        rank_name_rect.center = (
                            square_rect[0] + SQUARE_SIZE / 8,
                            square_rect[1] + SQUARE_SIZE / 5
                        )
                        screen.blit(rank_name, rank_name_rect)

                    if i == 7:
                        file_name = label_font.render(
                            file, True,
                            GRAY if (i + j) % 2 == 0 else WHITE
                        )
                        file_name_rect = file_name.get_rect()
                        file_name_rect.center = (
                            square_rect[0] + SQUARE_SIZE / 8,
                            square_rect[1] + SQUARE_SIZE * 4 / 5,
                        )
                        screen.blit(file_name, file_name_rect)

                    # Chess pieces
                    if square in occupied:
                        piece = occupied[square].symbol()
                        piece = icon[piece]
                        pieceRect = piece.get_rect()
                        pieceRect.center = square_rect.center
                        screen.blit(piece, pieceRect)

                    row.append(square_rect)

                squares.append(row)

            if not game_over:  # yet

                # If AI's turn
                if not board.turn == user:

                    # AI is thinking of a move
                    ai_thinking = message_font.render("AI is thinking...", True, WHITE)
                    ai_thinking_rect = ai_thinking.get_rect()
                    ai_thinking_rect.center = WIDTH / 2, HEIGHT / 12
                    screen.blit(ai_thinking, ai_thinking_rect)

                    if ai_turn:

                        time.sleep(0.5)

                        value, move = ai.minimax(board)
                        termcolor.cprint(
                            f"{move}  {value}",
                            'green' if (board.turn == chess.WHITE and value > 0) or (board.turn == chess.BLACK and value < 0) else
                            'white' if not value else
                            'red'
                        )
                        board.push(move)

                        ai_turn = False

                    else:
                        ai_turn = True

                else:  # if user's turn

                    # Handle pawn promotion
                    if pawn_promoted:

                        options = {}

                        for i, symbol in enumerate('QRBN' if user == chess.WHITE else 'qrbn'):
                            option_button = pg.draw.circle(screen, WHITE, (SQUARE_SIZE*2*(i+1), 50), 32)
                            draw_circle(screen, WHITE, (SQUARE_SIZE*2*(i+1), 50), 33)
                            option = icon[symbol]
                            option_rect = option.get_rect()
                            option_rect.center = option_button.center
                            screen.blit(option, option_rect)
                            options[symbol] = option_button

                        if pg.mouse.get_pressed()[0]:

                            for symbol in ('QRBN' if user == chess.WHITE else 'qrbn'):
                                if options[symbol].collidepoint(pg.mouse.get_pos()):
                                    time.sleep(0.2)
                                    board.push_san(move.uci()[:4] + symbol.lower())
                                    pawn_promoted = False

                            if pawn_promoted:
                                selected_piece = None
                                pawn_promoted = False

                    resign_button = pg.draw.circle(screen, WHITE, (WIDTH / 2, HEIGHT * 11 / 12), 24)
                    draw_circle(screen, WHITE, (WIDTH / 2, HEIGHT * 11 / 12), 25)
                    draw_circle(screen, BLACK, (WIDTH / 2, HEIGHT * 11 / 12), 22)
                    resign = pg.image.load(os.path.join('assets', 'images', 'flag.png'))
                    resign_rect = resign.get_rect()
                    resign_rect.center = WIDTH / 2 + 2, HEIGHT * 11 / 12 + 1
                    screen.blit(resign, resign_rect)

                    if pg.mouse.get_pressed()[0]:
                        if resign_button.collidepoint(pg.mouse.get_pos()):
                            time.sleep(0.2)
                            user_resigned = True

                    user_pieces = {
                        square
                        for square, piece in occupied.items()
                        if piece.color == user
                    }

                    # If user has clicked somewhere on the screen
                    if not pawn_promoted:
                        if pg.mouse.get_pressed()[0]:

                            for i, rank in enumerate(ranks):
                                for j, file in enumerate(files):

                                    # If user clicked one of the squares
                                    if squares[i][j].collidepoint(pg.mouse.get_pos()):

                                        time.sleep(0.2)

                                        # and one of user's pieces is on that square
                                        if chess.parse_square(file + rank) in user_pieces:

                                            # If user has already selected a piece
                                            # and clicked that piece again
                                            if selected_piece and file + rank == selected_piece:
                                                selected_piece = None

                                            # If user hasn't selected a piece to move yet
                                            else:
                                                selected_piece = file + rank

                                        # Else if a piece has already been chosen
                                        # and it's not another of user's pieces
                                        elif selected_piece:

                                            try:
                                                # Find a legal move
                                                move = board.find_move(
                                                    chess.parse_square(selected_piece),
                                                    chess.parse_square(file + rank)
                                                )
                                                # If move is not a pawn promotion
                                                if len(move.uci()) < 5:
                                                    board.push(move)
                                                else:
                                                    pawn_promoted = True
                                            except ValueError:
                                                pass
                                            selected_piece = None

            else:  # if the game is over

                result = (
                    "Draw" if winner == None else
                    "You win" if winner == user else
                    "AI wins"
                )
                result = message_font.render(result, True, WHITE)
                result_rect = result.get_rect()
                result_rect.center = WIDTH / 2, HEIGHT / 12
                screen.blit(result, result_rect)

                # Draw Play Again button
                again_button = pg.Rect(WIDTH / 2, HEIGHT / 2, WIDTH / 3, 56)
                again_button.center = WIDTH / 2, HEIGHT - HEIGHT / 12
                pg.draw.rect(screen, WHITE, again_button, border_radius=CORNER_RADIUS)

                again = message_font.render("PLAY AGAIN", True, BLACK)
                again_rect = again.get_rect()
                again_rect.center = again_button.center
                screen.blit(again, again_rect)

                if pg.mouse.get_pressed()[0]:
                    if again_button.collidepoint(pg.mouse.get_pos()):
                        time.sleep(0.2)
                        board.reset()
                        user = None
                        ai_turn = False
                        game_over = False
                        selected_piece = False
                        pawn_promoted = False
                        user_resigned = False

        # User resigns
        if user_resigned:
            selected_piece = False
            game_over = True
            winner = not user

        # Game is over not due to user resigning
        elif game_over := board.outcome():
            winner = game_over.winner

        pg.display.flip()


def draw_circle(surface, color, center, radius):
    """
    Draw an antialiased circle
    Instructions from https://www.pygame.org/docs/ref/gfxdraw.html
    """
    x, y = int(center[0]), int(center[1])

    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


if __name__ == '__main__':
    main()
