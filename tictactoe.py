import sys
import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
gray = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Sizes
width = 300
height = 300
line_width = 5
board_cols = 3
board_rows = 3
square = width // board_cols
circle_radius = square // 3
circle_width = 15
cross_width = 25

# Screen setup
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(black)

# Board setup
board = np.zeros((board_rows, board_cols))

def draw_lines(color=white):
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, start_pos=(0, square * i), end_pos=(width, square * i), width=line_width)
        pygame.draw.line(screen, color, start_pos=(square * i, 0), end_pos=(square * i, height), width=line_width)

def draw_figures(color=white):
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * square + square // 2), int(row * square + square // 2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                # Draw cross
                pygame.draw.line(screen, color, start_pos=(col * square + square // 4, row * square + square // 4), end_pos=(col * square + 3 * square // 4, row * square + 3 * square // 4), width=cross_width)
                pygame.draw.line(screen, color, start_pos=(col * square + square // 4, row * square + 3 * square // 4), end_pos=(col * square + 3 * square // 4, row * square + square // 4), width=cross_width)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0 

def is_board_full(check_board=board):
    return not np.any(check_board == 0)

def check_win(player, check_board=board):
    for col in range(board_cols):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(board_rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True
    
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(player=2, check_board=minimax_board):
        return float('inf')
    elif check_win(player=1, check_board=minimax_board):
        return float('-inf')
    elif is_board_full(check_board=minimax_board):
        return 0
    
    if is_maximizing:
        best_score = float('-inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, is_maximizing=False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(board_rows):
            for col in range(board_cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, is_maximizing=True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = float('-inf')
    move = (-1, -1)
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, depth=0, is_maximizing=False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], player=2)
        return True
    return False

def restart_game():
    screen.fill(black)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // square
            mouseY = event.pos[1] // square

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(green)
            draw_lines(green)
        elif check_win(2):
            draw_figures(red)
            draw_lines(red)
        else:
            draw_lines(gray)
            draw_figures(gray)

    pygame.display.update()
