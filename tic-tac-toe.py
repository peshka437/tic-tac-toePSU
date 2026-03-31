import pygame
import sys
import time

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Крестики-нолики")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
X_COLOR = (200, 50, 50)
O_COLOR = (50, 50, 200)
BG_COLOR = (240, 240, 240)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER = (150, 255, 150)

font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

board = [" " for _ in range(9)]
current_player = "X"
game_mode = None
game_over = False
winner = None

CELL_SIZE = WINDOW_WIDTH // 3
OFFSET_Y = 100

def draw_board():
    screen.fill(BG_COLOR)

    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, OFFSET_Y), (i * CELL_SIZE, WINDOW_HEIGHT), 5)
        pygame.draw.line(screen, LINE_COLOR, (0, OFFSET_Y + i * CELL_SIZE), (WINDOW_WIDTH, OFFSET_Y + i * CELL_SIZE), 5)

    for i in range(9):
        row = i // 3
        col = i % 3
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2

        if board[i] == "X":
            pygame.draw.line(screen, X_COLOR, (x - 50, y - 50), (x + 50, y + 50), 8)
            pygame.draw.line(screen, X_COLOR, (x + 50, y - 50), (x - 50, y + 50), 8)
        elif board[i] == "O":
            pygame.draw.circle(screen, O_COLOR, (x, y), 50, 8)

def draw_text(text, font, color, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_menu():
    screen.fill(BG_COLOR)
    draw_text("Крестики-нолики", font_large, BLACK, WINDOW_WIDTH//2, 150)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    btn1_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, 250, 400, 80)
    color1 = BUTTON_HOVER if btn1_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color1, btn1_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, btn1_rect, 3, border_radius=15)
    draw_text("Друг против друга", font_medium, BLACK, WINDOW_WIDTH//2, 290)

    btn2_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, 370, 400, 80)
    color2 = BUTTON_HOVER if btn2_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR
    pygame.draw.rect(screen, color2, btn2_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, btn2_rect, 3, border_radius=15)
    draw_text("Против компьютера", font_medium, BLACK, WINDOW_WIDTH//2, 410)

    btn3_rect = pygame.Rect(WINDOW_WIDTH//2 - 200, 490, 400, 80)
    color3 = (255, 100, 100) if btn3_rect.collidepoint(mouse_x, mouse_y) else (200, 100, 100)
    pygame.draw.rect(screen, color3, btn3_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, btn3_rect, 3, border_radius=15)
    draw_text("Выход", font_medium, BLACK, WINDOW_WIDTH//2, 530)

    return btn1_rect, btn2_rect, btn3_rect

def handle_menu_click(pos, btn1, btn2, btn3):
    global game_mode, board, current_player, game_over, winner
    if btn1.collidepoint(pos):
        game_mode = "pvp"
        board = [" " for _ in range(9)]
        current_player = "X"
        game_over = False
        winner = None
        return True
    elif btn2.collidepoint(pos):
        game_mode = "ai"
        board = [" " for _ in range(9)]
        current_player = "X"
        game_over = False
        winner = None
        return True
    elif btn3.collidepoint(pos):
        pygame.quit()
        sys.exit()
    return False

def get_cell_from_mouse(pos):
    x, y = pos
    if y < OFFSET_Y or y > WINDOW_HEIGHT:
        return None
    col = x // CELL_SIZE
    row = (y - OFFSET_Y) // CELL_SIZE
    if 0 <= col < 3 and 0 <= row < 3:
        return row * 3 + col
    return None

def check_winner(board, player):
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    return any(all(board[i] == player for i in combo) for combo in wins)

def is_draw(board):
    return " " not in board

def minimax(board, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_mode is None:
                btn1, btn2, btn3 = draw_menu()
                if handle_menu_click(event.pos, btn1, btn2, btn3):
                    pass
            else:
                if not game_over:
                    cell = get_cell_from_mouse(event.pos)
                    if cell is not None and board[cell] == " ":
                        board[cell] = current_player

                        if check_winner(board, current_player):
                            winner = current_player
                            game_over = True
                        elif is_draw(board):
                            game_over = True
                            winner = "draw"

                        current_player = "O" if current_player == "X" else "X"

                        if game_mode == "ai" and current_player == "O" and not game_over:
                            comp_move = best_move(board)
                            board[comp_move] = "O"
                            if check_winner(board, "O"):
                                winner = "O"
                                game_over = True
                            elif is_draw(board):
                                game_over = True
                                winner = "draw"
                            current_player = "X"
                else:
                    game_mode = None

    if game_mode is None:
        draw_menu()
    else:
        draw_board()

        if game_over:
            if winner == "X":
                text = "Победил X! "
            elif winner == "O":
                text = "Победил O! " if game_mode == "pvp" else "Компьютер победил! "
            elif winner == "draw":
                text = "Ничья! "
            else:
                text = ""
            draw_text(text, font_medium, BLACK, WINDOW_WIDTH//2, 50)
            draw_text("Нажмите в любом месте для меню", font_small, BLACK, WINDOW_WIDTH//2, WINDOW_HEIGHT - 30)
        else:
            if game_mode == "ai":
                player_text = "Твой ход (X)" if current_player == "X" else "Компьютер думает..."
            else:
                player_text = f"Ход игрока {current_player}"
            draw_text(player_text, font_medium, BLACK, WINDOW_WIDTH//2, 40)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
