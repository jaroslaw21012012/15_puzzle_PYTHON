# PUZZLE GAME
# BY yarik21yt
# RaNdOm ChAoS!

import pygame
import sys
from pygame.locals import *
import time
import random
from colors import *


#generted chaos: WOOOOOOOW
# ВЫЛОЖИТЬ В ГИТХАБ. ПОИГРАТЬ В 2048


pygame.init()


WIDTH = 600
HEIGHT = 500
FPS = 30
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PUZZLE_GAME")

BOARD_WIDTH = 4
BOARD_HEIGHT = 4
SEED = 0
from texts import *
SIZE_BOX = 80
GAP_BOX = 10

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

#modes
GAME = "game"
WIN = "win"
MENU = "menu"

swipe_snd = pygame.mixer.Sound("source/sounds/swipe.wav")
swipe_snd.set_volume(0.2)


game_time_start = time.time()

font = pygame.font.Font("source/fonts/TitilliumWeb-Regular.ttf", 25)
def draw_seed():
    seed_text_surf = font.render(f"Current seed: {SEED}", True, WHITE)
    seed_text_rect = seed_text_surf.get_rect()
    seed_text_rect.topleft = (10, 10)
    DISPLAY.blit(seed_text_surf, seed_text_rect)


def draw_time_text():
    all_seconds = int(time.time() - game_time_start)
    minutes = all_seconds // 60
    seconds = all_seconds - (minutes * 60)
    time_text_surf = font.render(f"Time : {minutes}:{seconds}", True, WHITE)
    time_text_rect = time_text_surf.get_rect()
    time_text_rect.topright = (590, 10)
    DISPLAY.blit(time_text_surf, time_text_rect)


def draw_win_text():
    win_text_surf = font.render("Congratulations! You won!", True, WHITE)
    win_text_rect = win_text_surf.get_rect()
    win_text_rect.midtop = (WIDTH / 2, 10)
    DISPLAY.blit(win_text_surf, win_text_rect)


def restart_btn():
    surf = font.render("Restart", True, BG)
    rect = surf.get_rect()
    rect.midbottom = (WIDTH / 2, HEIGHT -10)
    DISPLAY.blit(surf, rect)


def draw_title_text():
    font_title = pygame.font.Font("source/fonts/TitilliumWeb-Regular.ttf", 40)
    surf = font_title.render("15 PUZZLE", True, WHITE)
    rect = surf.get_rect()
    rect.midtop = (WIDTH / 2, 15)
    DISPLAY.blit(surf, rect)


def draw_input_seed(text):
    surf = font.render(str(text), True, WHITE)
    rect = surf.get_rect()
    rect.center = (WIDTH / 2, HEIGHT / 2)
    DISPLAY.blit(surf, rect)


def draw_input_text():
    font_title = pygame.font.Font("source/fonts/TitilliumWeb-Regular.ttf", 20)
    surf = font_title.render("Enter seed:", True, WHITE)
    rect = surf.get_rect()
    rect.center = (WIDTH / 2, HEIGHT / 2 - 40)
    DISPLAY.blit(surf, rect)


def draw_start_game():
    surf = font.render("START", True, BG)
    rect = surf.get_rect()
    rect.center = (WIDTH / 2, HEIGHT / 4 * 3)
    DISPLAY.blit(surf, rect)


def generate_map(seed):
    board = []
    numbers = list(range(16))
    random.seed(seed)
    for y in range(BOARD_HEIGHT):
        row = []
        for x in range(BOARD_WIDTH):
            number = random.choice(numbers)
            row.append(number)
            numbers.remove(number)
        board.append(row)
    return board


def generate_win_board():
    board = []
    numbers = list(range(1, 17))
    for y in range(BOARD_HEIGHT):
        row = []
        for x in range(BOARD_WIDTH):
            row.append(numbers[0])
            numbers.remove(numbers[0])
        board.append(row)
    board[-1][-1] = 0
    return board



def draw_board(board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            left = x * (SIZE_BOX + GAP_BOX) + 120
            top = y * (SIZE_BOX + GAP_BOX) + 80
            if board[y][x] != 0:
                pygame.draw.rect(DISPLAY, BOX, (left, top, SIZE_BOX, SIZE_BOX))
                surf = font.render(str(board[y][x]),  True, BG)
                surf_rect = surf.get_rect()
                surf_rect.centerx = left + SIZE_BOX // 2
                surf_rect.centery = top + SIZE_BOX // 2
                DISPLAY.blit(surf, surf_rect)

    pygame.draw.rect(DISPLAY, BORDER, (110, 70, 370, 370), 4)



def check_move(board, key):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] == 0:
                box_y = y
                box_x = x
    if key == UP and box_y == BOARD_HEIGHT - 1:
        return False
    elif key == DOWN and box_y == 0:
        return False
    elif key == LEFT and box_x == BOARD_WIDTH - 1:
        return False
    elif key == RIGHT and box_x == 0:
        return False
    return True




def move_box(board, key):
    if not check_move(board, key):
        return False
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[y][x] == 0:
                box_y = y
                box_x = x
    if key == UP:
        board[box_y][box_x] = board[box_y + 1][box_x]
        board[box_y + 1][box_x] = 0
        swipe_snd.play()
    if key == DOWN:
        board[box_y][box_x] = board[box_y - 1][box_x]
        board[box_y - 1][box_x] = 0
        swipe_snd.play()
    if key == LEFT:
        board[box_y][box_x] = board[box_y][box_x + 1]
        board[box_y][box_x + 1] = 0
        swipe_snd.play()
    if key == RIGHT:
        board[box_y][box_x] = board[box_y][box_x - 1]
        board[box_y][box_x - 1] = 0
        swipe_snd.play()







mode = MENU
board = generate_map(SEED)
win_board = generate_win_board()
btn_restart = pygame.Rect(240, HEIGHT - 45, 120, 30)
btn_start = pygame.Rect(250, HEIGHT / 4 * 3 - 20, 100, 50)
text = str(1234567890)

while True:
    DISPLAY.fill(BG)
    if mode == MENU:
        draw_title_text()
        pygame.draw.rect(DISPLAY, WHITE, (215, 232, 170, 40),width=3, border_radius=5)
        draw_input_seed(text)
        draw_input_text()
        pygame.draw.rect(DISPLAY, WHITE, (250, HEIGHT / 4 * 3 - 20, 100, 50), border_radius=5)
        draw_start_game()
    elif mode == GAME:
        draw_board(board)
        draw_seed()
        draw_time_text()
        if board == win_board:
            mode = WIN
    elif mode == WIN:
        draw_board(win_board)
        draw_win_text()
        pygame.draw.rect(DISPLAY, BORDER, (240, HEIGHT -45, 120, 30), border_radius=5)
        restart_btn()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if mode == MENU:
                if event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0):
                    if len(text) <= 9:
                        text += event.unicode
                elif event.key == K_BACKSPACE:
                    text = text[:-1]
            elif mode == GAME:
                if event.key in (K_s, K_DOWN):
                    move_box(board, DOWN)
                elif event.key in (K_w, K_UP):
                    move_box(board, UP)
                elif event.key in (K_a, K_LEFT):
                    move_box(board, LEFT)
                elif event.key in (K_d, K_RIGHT):
                    move_box(board, RIGHT)
        elif event.type == MOUSEBUTTONUP:
            if mode == WIN:
                if btn_restart.collidepoint(event.pos[0], event.pos[1]):
                    mode = MENU
            elif mode == MENU:
                if btn_start.collidepoint(event.pos[0], event.pos[1]):
                    if len(text) != 0:
                        SEED = int(text)
                        game_time_start = time.time()
                        board = generate_map(SEED)
                        mode = GAME






    pygame.display.update()
    pygame.time.Clock().tick(FPS)