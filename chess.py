import PySimpleGUI as sg
import itertools
from logging.config import valid_ident
import pygame
import engine

pygame.mixer.init()
WIDTH = HEIGHT = 800
DIMENSIONS = 8
SQ_SIZE = HEIGHT//DIMENSIONS
MAX_FPS = 15
IMAGES = {}



def pieces():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR",
              "bP", "wP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"icons/{piece}.png").convert_alpha(),
            (SQ_SIZE, SQ_SIZE),
        )


def highlightSquares(screen, game_state, valid_moves, square_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.moveLog)) > 0:
        last_move = game_state.moveLog[-1]
        s = starting_square('red')
        screen.blit(s, (last_move.end_col * SQ_SIZE,
                    last_move.end_row * SQ_SIZE))

    if square_selected != ():
        row, col = square_selected
        # square_selected is a piece that can be moved
        if game_state.board[row][col][0] == ('w' if game_state.whiteToMove else 'b'):
            s = starting_square('red')
            screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))
            # highlight moves from that square
            s.fill(pygame.Color('blue'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * SQ_SIZE,
                                move.end_row * SQ_SIZE))


def starting_square(arg0):
    result = pygame.Surface((SQ_SIZE, SQ_SIZE))
    result.set_alpha(70)
    result.fill(pygame.Color(arg0))
    return result


def main(): 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    gs = engine.GameState()
    ValidMoves = gs.getValidMoves()
    moveMade = False
    pieces()
    running = True
    sqSelected = ()
    PlayerClicks = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                gs.undoMove()
                moveMade = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if len(PlayerClicks) == 0 and gs.board[row][col] == "--":
                    continue
                if sqSelected == (row, col):
                    sqSelected = ()
                    PlayerClicks = []
                else:
                    sqSelected = (row, col)
                    PlayerClicks.append(sqSelected)
                if len(PlayerClicks) == 2:
                    move = engine.move(
                        PlayerClicks[0], PlayerClicks[1], gs.board)
                    for i in range(len(ValidMoves)):
                        if move == ValidMoves[i]:
                            gs.makeMove(ValidMoves[i])
                            pygame.mixer.music.load('sounds\play.mp3')
                            pygame.mixer.music.play()
                            moveMade = True
                            PlayerClicks = []
                            sqSelected = ()
                        if not moveMade:
                            PlayerClicks = [sqSelected]
            if moveMade:
                ValidMoves = gs.getValidMoves()
                moveMade = False
            clock.tick(MAX_FPS)
            pygame.display.flip()


        Draw_gs(screen, gs, ValidMoves, sqSelected)


def Draw_gs(screen, gs, ValidMoves, sqSelected):
    Draw_board(screen)
    highlightSquares(screen, gs, ValidMoves, sqSelected)
    DrawPieces(screen, gs.board)


def Draw_board(screen):
    colors = [pygame.Color((118,150,85,255)), pygame.Color(238,238,210,255)]
    for r, c in itertools.product(range(DIMENSIONS), range(DIMENSIONS)):
        color = colors[(r+c) % 2]
        pygame.draw.rect(screen, color, pygame.Rect(
            c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def DrawPieces(screen, board):
    for r, c in itertools.product(range(DIMENSIONS), range(DIMENSIONS)):
        piece = board[r][c]
        if piece != "--":
            screen.blit(IMAGES[piece], pygame.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()
