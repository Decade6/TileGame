"""

Name: Declan Murphy
Date: 02/04/24
Assignment: Assignment #5 Implement Adversarial Search
Due Date: 02/04/24
About this project: Implement applications that utilize classical Artificial Intelligence techniques, such as search algorithms, minimax algorithm, and greedy algorithms to solve problems
Assumptions: N/A
All work below was performed by Declan Murphy

"""

import pygame
import sys
import random
import pygame.time
from pygame.locals import *

# Function to create text surface with specified parameters
def make_text(text, color, bgcolor, top, left):
    text_surf = BASICFONT.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect

# Constants for the game
BOARDWIDTH = 3  # Number of columns in the board
BOARDHEIGHT = 3  # Number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = (0, 50, 255)
DARKTURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
LIGHTGRAY = (200, 200, 200)
# Define colors for the game
BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

# Initialize pygame and set up the display
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('3 in a Row Slide Puzzle')
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

# Store the option buttons and their rectangles
RESET_SURF, RESET_RECT = make_text('Restart', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = make_text('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
QUIT_SURF, QUIT_RECT = make_text('Quit', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

# Define directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Generate a new puzzle board by shuffling the tiles
def generateNewPuzzle(numShuffles):
    board = [[(i + j * BOARDWIDTH) % (BOARDWIDTH * BOARDHEIGHT) for i in range(BOARDWIDTH)] for j in range(BOARDHEIGHT)]
    blankx = BOARDWIDTH - 1
    blanky = BOARDHEIGHT - 1
    for i in range(numShuffles):
        move = random.choice([UP, DOWN, LEFT, RIGHT])
        blankx, blanky = makeMove(board, move, blankx, blanky)
    return board, []

# Calculate the top-left coordinates of a box on the game board
def leftTopCoordsOfBox(col, row):
    left = col * TILESIZE
    top = row * TILESIZE
    return left, top

def drawBoard(board, msg):
    DISPLAYSURF.fill(BGCOLOR)

    # Center the game board on the screen
    board_width = BOARDWIDTH * TILESIZE
    board_height = BOARDHEIGHT * TILESIZE
    board_left = (WINDOWWIDTH - board_width) // 2
    board_top = (WINDOWHEIGHT - board_height) // 2

    if msg:
        # Display message at the top of the screen
        textSurf, textRect = make_text(msg, MESSAGECOLOR, BGCOLOR, (WINDOWWIDTH - BASICFONT.size(msg)[0]) // 2, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            left, top = leftTopCoordsOfBox(col, row)
            pygame.draw.rect(DISPLAYSURF, TILECOLOR, (board_left + left, board_top + top, TILESIZE, TILESIZE))
            pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (board_left + left, board_top + top, TILESIZE, TILESIZE), 5)  # Draw border

            if board[row][col]:
                # Calculate the center coordinates of the cell
                center_x = board_left + left + TILESIZE // 2
                center_y = board_top + top + TILESIZE // 2

                # Get text size to properly center it
                textSurf, textRect = make_text(str(board[row][col]), TEXTCOLOR, TILECOLOR, 0, 0)
                textRect.center = (center_x, center_y)
                DISPLAYSURF.blit(textSurf, textRect)

# Make a move to move the blank tile to the specified position
def moveBlankToPosition(board, dest_row, dest_col):
    blank_row, blank_col = getBlankPosition(board)
    path = findShortestPath(board, (blank_row, blank_col), (dest_row, dest_col))
    for move in path:
        makeMove(board, move, *getBlankPosition(board))

# Make a move on the board
def makeMove(board, move, blankx, blanky):
    if move == UP and blanky != len(board) - 1:
        board[blanky][blankx], board[blanky + 1][blankx] = board[blanky + 1][blankx], board[blanky][blankx]
        return blankx, blanky + 1
    elif move == DOWN and blanky != 0:
        board[blanky][blankx], board[blanky - 1][blankx] = board[blanky - 1][blankx], board[blanky][blankx]
        return blankx, blanky - 1
    elif move == LEFT and blankx != len(board[0]) - 1:
        board[blanky][blankx], board[blanky][blankx + 1] = board[blanky][blankx + 1], board[blanky][blankx]
        return blankx + 1, blanky
    elif move == RIGHT and blankx != 0:
        board[blanky][blankx], board[blanky][blankx - 1] = board[blanky][blankx - 1], board[blanky][blankx]
        return blankx - 1, blanky
    return blankx, blanky

# Get the position of the blank tile
def getBlankPosition(board):
    for row in range(BOARDHEIGHT):
        for col in range(BOARDWIDTH):
            if board[row][col] == BLANK:
                return row, col
    # Return -1, -1 if no blank tile is found
    return -1, -1

# Check if the game is over
def game_over(board):
    current_value = 0
    for row in board:
        for tile in row:
            if tile is not None:
                if tile != current_value + 1:
                    return False
                current_value += 1
    return True

# Check if a move is valid
def is_valid_move(board, move, blank_row, blank_col):
    if move is None:
        return 0 <= blank_row < BOARDHEIGHT and 0 <= blank_col < BOARDWIDTH
    elif move == UP:
        return blank_row < BOARDHEIGHT - 1
    elif move == DOWN:
        return blank_row > 0
    elif move == LEFT:
        return blank_col < BOARDWIDTH - 1
    elif move == RIGHT:
        return blank_col > 0

# Find the shortest path between two positions using Breadth-First Search (BFS)
def findShortestPath(board, start_pos, dest_pos):
    queue = [(start_pos, [])]
    visited = set()
    while queue:
        current_pos, path = queue.pop(0)
        if current_pos == dest_pos:
            return path
        if current_pos in visited:
            continue
        visited.add(current_pos)
        for move in [UP, DOWN, LEFT, RIGHT]:
            new_pos = makeMove(board, move, *current_pos)
            if new_pos:
                queue.append((new_pos, path + [move]))
    return []


# Store the option buttons and their rectangles
RESTART_SURF, RESTART_RECT = make_text('Restart', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
NEW_SURF, NEW_RECT = make_text('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
QUIT_SURF, QUIT_RECT = make_text('Quit', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)


def main():
    mainBoard, solutionSeq = generateNewPuzzle(80)
    solved = False
    UserTurn = False  # Set to False initially to ensure computer starts first
    pygame.time.delay(1500)  # Delay before the game starts (1.5 seconds)

    while True:  # Main game loop
        slideTo = None  # The direction, if any, a tile should slide
        if UserTurn:
            msg = 'Your Turn'  # Message to show in the upper left corner
        else:
            msg = 'Computer\'s Turn'  # Message to show in the upper left corner

        # Check for game over or solved state
        if game_over(mainBoard):
            if UserTurn:
                msg = 'Congratulations! You won!!'
            else:
                msg = 'Computer won!!'
            solved = True

        if not solved:
            if not UserTurn:
                # Computer's turn
                msg = 'Computer\'s Turn'  # Update message
                valid_moves = [UP, DOWN, LEFT, RIGHT]
                move = random.choice(valid_moves)
                makeMove(mainBoard, move, *getBlankPosition(mainBoard))
                UserTurn = True
            else:
                # User's turn
                msg = 'Your Turn'  # Update message
                for event in pygame.event.get():  # Event handling loop
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        mousex, mousey = event.pos
                        if RESTART_RECT.collidepoint(mousex, mousey):
                            mainBoard, solutionSeq = generateNewPuzzle(80)
                            solved = False
                            UserTurn = True
                        elif NEW_RECT.collidepoint(mousex, mousey):
                            mainBoard, solutionSeq = generateNewPuzzle(80)
                            solved = False
                            UserTurn = True
                        elif QUIT_RECT.collidepoint(mousex, mousey):
                            pygame.quit()
                            sys.exit()
                        else:
                            col = mousex // TILESIZE
                            row = mousey // TILESIZE
                            if is_valid_move(mainBoard, None, row, col):
                                moveBlankToPosition(mainBoard, row, col)
                                UserTurn = False
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            moveBlankToPosition(mainBoard, getBlankPosition(mainBoard)[0] + 1,
                                                getBlankPosition(mainBoard)[1])
                            UserTurn = False
                        elif event.key == K_DOWN:
                            moveBlankToPosition(mainBoard, getBlankPosition(mainBoard)[0] - 1,
                                                getBlankPosition(mainBoard)[1])
                            UserTurn = False
                        elif event.key == K_LEFT:
                            moveBlankToPosition(mainBoard, getBlankPosition(mainBoard)[0],
                                                getBlankPosition(mainBoard)[1] + 1)
                            UserTurn = False
                        elif event.key == K_RIGHT:
                            moveBlankToPosition(mainBoard, getBlankPosition(mainBoard)[0],
                                                getBlankPosition(mainBoard)[1] - 1)
                            UserTurn = False

        # Draw the game board
        drawBoard(mainBoard, msg)

        # Draw the buttons
        DISPLAYSURF.blit(RESTART_SURF, RESTART_RECT)
        DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
        DISPLAYSURF.blit(QUIT_SURF, QUIT_RECT)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Run the main function
if __name__ == '__main__':
    main()
