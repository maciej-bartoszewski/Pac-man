import math
import random
import sys
import copy
import pygame
from boards_in_game import boards

# Board and screen sizes
DELAY = 3  # By increasing the DELAY you can slow down the game or speed it up by decreasing it
WIDTH = 810
HEIGHT = 864
B_WIDTH = WIDTH // 30
B_HEIGHT = (HEIGHT - 50) // 32

# Heroes images
PACMAN_IMG_1 = pygame.transform.scale(pygame.image.load("images/pacman_1.png"), (35, 35))
PACMAN_IMG_2 = pygame.transform.scale(pygame.image.load("images/pacman_2.png"), (35, 35))
BLUE_GHOST = pygame.transform.scale(pygame.image.load("images/blue.png"), (35, 35))
PINK_GHOST = pygame.transform.scale(pygame.image.load("images/pink.png"), (35, 35))
RED_GHOST = pygame.transform.scale(pygame.image.load("images/red.png"), (35, 35))
YELLOW_GHOST = pygame.transform.scale(pygame.image.load("images/yellow.png"), (35, 35))
PU_GHOST = pygame.transform.scale(pygame.image.load("images/pu_ghost.png"), (35, 35))
HEART = pygame.transform.scale(pygame.image.load("images/heart.png"), (35, 35))

# Screen images
MAIN_IMG = pygame.transform.scale(pygame.image.load("images/theme.png"), (800, 800))
START_BUTTON = pygame.transform.scale(pygame.image.load("images/start.png"), (150, 100))
EXIT_BUTTON = pygame.transform.scale(pygame.image.load("images/exit.png"), (150, 100))
WON_IMG = pygame.transform.scale(pygame.image.load("images/won.png"), (800, 800))
LOST_IMG = pygame.transform.scale(pygame.image.load("images/lost.png"), (800, 800))
PAUSE = pygame.transform.scale(pygame.image.load("images/pause.png"), (800, 800))
NEXT_LVL = pygame.transform.scale(pygame.image.load("images/next_lvl.png"), (800, 800))

# Global game variables
LIVES = 3
POINTS = 0
BEST_SCORE = 0
LVL = 0
TURN = 0
RUNNING = True
GAME_WON = False


class Hero:
    def __init__(self, h_id, photo):
        self.id = h_id
        self.img = photo
        self.alive = True
        self.main_img = photo
        self.rotate_direction = 3
        self.move = 3
        self.prev_move = 0
        self.turns_to_wait = 0
        self.starting_x = 0
        self.starting_y = 0
        self.x = 0
        self.y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.val = 0
        self.prev_val = 0
        self.possible_moves = [True, True, True, True, True]
        self.draw_x = 0
        self.draw_y = 0

    def position(self, board):
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == self.id:
                    self.x = col
                    self.y = row
                    return

    def find_possible_moves(self, board):
        # 0 - up, 1 - down, 2 - left, 3 - right, 4 - stay
        hero_moves = [True, True, True, True, True]
        if self.id == 10:
            allowed_moves = [0, 1, 2, 11, 12, 13, 14, 15, 16]
        else:
            allowed_moves = [0, 1, 2, 9, 10]
            if not is_ghost_in_prison(self.x, self.y):
                allowed_moves.remove(9)

        if board[self.y + 1][self.x] not in allowed_moves:
            hero_moves[0] = False
        if board[self.y - 1][self.x] not in allowed_moves:
            hero_moves[1] = False
        if self.x != 0:
            if board[self.y][self.x - 1] not in allowed_moves:
                hero_moves[2] = False
        if self.x != 29:
            if board[self.y][self.x + 1] not in allowed_moves:
                hero_moves[3] = False

        self.possible_moves = hero_moves

    def change_position(self, board):
        self.prev_x = self.x
        self.prev_y = self.y

        # 0 - up, 1 - down, 2 - left, 3 - right
        if self.move == 0:
            if self.possible_moves[0]:
                self.y += 1

        elif self.move == 1:
            if self.possible_moves[1]:
                self.y -= 1

        elif self.move == 2:
            if self.possible_moves[2]:
                if self.x != 0:
                    self.x -= 1

        elif self.move == 3:
            if self.possible_moves[3]:
                if self.x != 29:
                    self.x += 1

        board[self.prev_y][self.prev_x] = self.prev_val
        self.val = board[self.y][self.x]
        if self.id != 10:
            self.prev_val = self.val

        if self.id == 10:
            if board[self.y][self.x] == 11:
                self.x = 28
            if board[self.y][self.x] == 12:
                self.x = 1

        if board[self.y][self.x] != 10:
            board[self.y][self.x] = self.id

    def rotate_img(self, image, move):
        self.img = image
        if move == 0:
            self.img = pygame.transform.rotate(self.img, -90)
        if move == 1:
            self.img = pygame.transform.rotate(self.img, 90)
        if move == 2:
            self.img = pygame.transform.flip(self.img, True, False)

    def set_starting_cords_on_other(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.prev_x = self.starting_x
        self.prev_y = self.starting_y

    def set_default_stats(self):
        self.val = 0
        self.prev_val = 0
        self.move = 3
        self.prev_move = 3
        self.turns_to_wait = 0
        self.img = self.main_img

    def set_default(self):
        self.set_starting_cords_on_other()
        self.set_default_stats()

    def draw(self, i):
        draw_x = self.x * B_WIDTH
        draw_y = self.y * B_HEIGHT
        if self.x != self.prev_x or self.y != self.prev_y:
            if self.prev_x == self.x:
                draw_x = self.prev_x * B_WIDTH
                if self.y > self.prev_y:
                    draw_y = self.prev_y * B_HEIGHT + i
                else:
                    draw_y = self.prev_y * B_HEIGHT - i

            if self.prev_y == self.y:
                draw_y = self.prev_y * B_HEIGHT
                if self.x == 28 and self.prev_x == 1:
                    draw_x = self.prev_x * B_WIDTH - i
                elif self.x == 1 and self.prev_x == 28:
                    draw_x = self.prev_x * B_WIDTH + i
                else:
                    if self.x > self.prev_x:
                        draw_x = self.prev_x * B_WIDTH + i
                    else:
                        draw_x = self.prev_x * B_WIDTH - i
        screen.blit(self.img, (draw_x, draw_y))


def draw_board_and_score(board):
    for row in range(len(board)):
        for col in range(len(board[1])):
            point = board[row][col]
            # little dot
            if point == 1:
                pygame.draw.circle(screen, "white",
                                   (col * B_WIDTH + (0.5 * B_WIDTH),
                                    row * B_HEIGHT + (0.5 * B_HEIGHT)), 4)
            # big dot
            if point == 2:
                pygame.draw.circle(screen, "white",
                                   (col * B_WIDTH + (0.5 * B_WIDTH),
                                    row * B_HEIGHT + (0.5 * B_HEIGHT)), 10)
            # vertical line
            if point == 3:
                pygame.draw.line(screen, "blue",
                                 (col * B_WIDTH + (0.5 * B_WIDTH), row * B_HEIGHT),
                                 (col * B_WIDTH + (0.5 * B_WIDTH), (row + 1) * B_HEIGHT), 4)
            # horizontal line
            if point == 4:
                pygame.draw.line(screen, "blue",
                                 (col * B_WIDTH, row * B_HEIGHT + (0.5 * B_HEIGHT)),
                                 ((col + 1) * B_WIDTH, row * B_HEIGHT + (0.5 * B_HEIGHT)), 4)
            # top right
            if point == 5:
                pygame.draw.arc(screen, "blue",
                                [(col * B_WIDTH - (B_WIDTH * 0.4)) - 1.1, (row * B_HEIGHT + (0.5 * B_HEIGHT)),
                                 B_WIDTH, B_HEIGHT], 0, math.pi / 2, 4)
            # top left
            if point == 6:
                pygame.draw.arc(screen, "blue",
                                [(col * B_WIDTH + (B_WIDTH * 0.5)), (row * B_HEIGHT + (0.5 * B_HEIGHT)),
                                 B_WIDTH, B_HEIGHT], math.pi / 2, math.pi, 4)
            # bottom left
            if point == 7:
                pygame.draw.arc(screen, "blue",
                                [(col * B_WIDTH + (B_WIDTH * 0.5)), (row * B_HEIGHT - (0.4 * B_HEIGHT)) - 1.1,
                                 B_WIDTH, B_HEIGHT], math.pi, 3 * math.pi / 2, 4)
            # bottom right
            if point == 8:
                pygame.draw.arc(screen, "blue",
                                [(col * B_WIDTH - (B_WIDTH * 0.4)) - 1.1, (row * B_HEIGHT - (0.4 * B_HEIGHT)) - 1.1,
                                 B_WIDTH, B_HEIGHT], 3 * math.pi / 2, 2 * math.pi, 4)
            # gate
            if point == 9:
                pygame.draw.line(screen, "white",
                                 (col * B_WIDTH, row * B_HEIGHT + (0.5 * B_HEIGHT)),
                                 ((col + 1) * B_WIDTH, row * B_HEIGHT + (0.5 * B_HEIGHT)), 4)

    for live in range(LIVES):
        screen.blit(HEART, (770 - (live * 40), 830))

    score_text = font.render(f"Score: {POINTS}", True, 'white')
    screen.blit(score_text, (20, 830))

    best_score_text = font.render(f"Best score: {BEST_SCORE}", True, 'white')
    screen.blit(best_score_text, (340, 830))


def show_game(pacman, blue, pink, red, yellow, lvl_board):
    pygame.time.wait(DELAY)

    # B_WIDTH == B_HEIGHT
    for i in range(B_HEIGHT):
        screen.fill("black")

        if i == 13:
            pacman.rotate_img(PACMAN_IMG_2, pacman.rotate_direction)

        blue.draw(i)
        pink.draw(i)
        red.draw(i)
        yellow.draw(i)
        pacman.draw(i)

        draw_board_and_score(lvl_board)
        pygame.display.update()

        pygame.time.wait(DELAY)

    pacman.rotate_img(PACMAN_IMG_1, pacman.rotate_direction)


def is_ghost_in_prison(x, y):
    if LVL == 0:
        if 11 < x < 18:
            if 13 < y < 17:
                return True
        return False

    elif LVL == 1:
        if 12 < x < 17:
            if 13 < y < 16:
                return True
        return False

    else:
        return False


def ghost_way(ghost):
    if is_ghost_in_prison(ghost.x, ghost.y):
        # choose move when ghost is in prison
        new_move = 1
        if not ghost.possible_moves[1]:
            if not ghost.possible_moves[2]:
                new_move = 3
            elif not ghost.possible_moves[3]:
                new_move = 2
            else:
                new_move = ghost.prev_move
    else:
        if True not in ghost.possible_moves[0:4]:
            new_move = 4
        else:
            # choose move when ghost isn't in prison
            allowed_without_coming_back = []
            for move_id in range(len(ghost.possible_moves) - 1):
                if ghost.possible_moves[move_id]:
                    allowed_without_coming_back.append(move_id)
            if ghost.move == 0 and 1 in allowed_without_coming_back:
                allowed_without_coming_back.remove(1)
            if ghost.move == 1 and 0 in allowed_without_coming_back:
                allowed_without_coming_back.remove(0)
            if ghost.move == 2 and 3 in allowed_without_coming_back:
                allowed_without_coming_back.remove(3)
            if ghost.move == 3 and 2 in allowed_without_coming_back:
                allowed_without_coming_back.remove(2)

            if len(allowed_without_coming_back) == 0:
                new_move = 4
            else:
                new_move = random.choice(allowed_without_coming_back)

    return new_move


def ghost_make_move(ghost, board, power_up):
    global POINTS

    if ghost.turns_to_wait == 0:
        ghost.find_possible_moves(board)
        ghost.prev_move = ghost.move
        ghost.move = ghost_way(ghost)
        ghost.change_position(board)
        if ghost.val == 10:
            # if ghost is on the same coordinates as the pacman, kill pacman or ghost
            if power_up and ghost.img == PU_GHOST:
                board[ghost.y][ghost.x] = 0
                ghost_died(ghost, board)
                ghost.turns_to_wait = 30
                POINTS += 200
            else:
                # returning false - pacman died
                return False
    # returning true - pacman is alive
    return True


def pac_died(pacman, blue, pink, red, yellow, board):
    global LIVES, TURN, RUNNING

    pacman.alive = False
    TURN = 0

    board[pacman.y][pacman.x] = 0
    if blue.prev_val != 10:
        board[blue.y][blue.x] = blue.prev_val
    if pink.prev_val != 10:
        board[pink.y][pink.x] = pink.prev_val
    if red.prev_val != 10:
        board[red.y][red.x] = red.prev_val
    if yellow.prev_val != 10:
        board[yellow.y][yellow.x] = yellow.prev_val

    board[blue.starting_y][blue.starting_x] = 13
    board[pink.starting_y][pink.starting_x] = 14
    board[red.starting_y][red.starting_x] = 15
    board[yellow.starting_y][yellow.starting_x] = 16
    board[pacman.starting_y][pacman.starting_x] = 10

    pacman.set_default()
    blue.set_default()
    pink.set_default()
    red.set_default()
    yellow.set_default()

    if LIVES == 0:
        RUNNING = False
    LIVES -= 1

    pacman.rotate_img(PACMAN_IMG_1, 3)


def ghost_died(ghost, board):
    global POINTS

    POINTS += 200
    board[ghost.starting_y][ghost.starting_x] = ghost.id
    ghost.set_default()
    ghost.turns_to_wait = 30


def check_win(board):
    dots_on_board = 0
    for row in board:
        dots_on_board += row.count(1)

    if dots_on_board:
        return False
    return True


def reset_game():
    global LVL, POINTS, RUNNING, TURN, LIVES, GAME_WON

    LVL = 0
    POINTS = 0
    RUNNING = True
    TURN = 0
    LIVES = 3
    GAME_WON = False


def save_new_score():
    global POINTS, BEST_SCORE

    BEST_SCORE = POINTS

    with open("best_score", "wt") as file:
        file.write(str(POINTS))


def game_over(image):
    while True:
        screen.fill("black")

        screen.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


def pause_or_next_lvl(image):
    while True:
        screen.fill("black")

        screen.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if POINTS > BEST_SCORE:
                        save_new_score()
                    main_menu()
                if event.key == pygame.K_SPACE:
                    return

        pygame.display.update()


def game():
    global LVL, POINTS, RUNNING, TURN, LIVES, GAME_WON

    ghosts = [13, 14, 15, 16]
    power_up = False
    start = True
    power_up_turns = 0
    pacman = Hero(10, PACMAN_IMG_1)
    blue = Hero(13, BLUE_GHOST)
    pink = Hero(14, PINK_GHOST)
    red = Hero(15, RED_GHOST)
    yellow = Hero(16, YELLOW_GHOST)

    game_boards = copy.deepcopy(boards)

    while RUNNING:
        screen.fill("black")
        clock.tick(60)

        if not pacman.alive:
            pacman.alive = True

        lvl_board = game_boards[LVL]
        if start:
            # Set starting values if game is starting
            pacman.position(lvl_board)
            pacman.starting_x, pacman.starting_y = pacman.x, pacman.y
            blue.position(lvl_board)
            blue.starting_x, blue.starting_y = blue.x, blue.y
            pink.position(lvl_board)
            pink.starting_x, pink.starting_y = pink.x, pink.y
            red.position(lvl_board)
            red.starting_x, red.starting_y = red.x, red.y
            yellow.position(lvl_board)
            yellow.starting_x, yellow.starting_y = yellow.x, yellow.y

            pacman.set_starting_cords_on_other()
            blue.set_starting_cords_on_other()
            pink.set_starting_cords_on_other()
            red.set_starting_cords_on_other()
            yellow.set_starting_cords_on_other()

            show_game(pacman, blue, pink, red, yellow, lvl_board)
            start = False
        else:
            # Change power up variables
            if power_up:
                power_up_turns += 1
            if blue.turns_to_wait != 0:
                blue.turns_to_wait -= 1
            if pink.turns_to_wait != 0:
                pink.turns_to_wait -= 1
            if red.turns_to_wait != 0:
                red.turns_to_wait -= 1
            if yellow.turns_to_wait != 0:
                yellow.turns_to_wait -= 1

            # Reading move
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        pacman.prev_move = pacman.move
                        pacman.move = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        pacman.prev_move = pacman.move
                        pacman.move = 1
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        pacman.prev_move = pacman.move
                        pacman.move = 2
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        pacman.prev_move = pacman.move
                        pacman.move = 3
                    elif event.key == pygame.K_ESCAPE:
                        pause_or_next_lvl(PAUSE)

            # Pacman moves
            pacman.find_possible_moves(lvl_board)
            pacman.change_position(lvl_board)

            if pacman.y != pacman.prev_y or pacman.x != pacman.prev_x:
                pacman.prev_move = pacman.move
            if pacman.x == pacman.prev_x and pacman.y == pacman.prev_y:
                move_to_remember = pacman.move
                pacman.move = pacman.prev_move
                pacman.change_position(lvl_board)
                pacman.move = move_to_remember
            else:
                pacman.rotate_direction = pacman.move
                pacman.rotate_img(PACMAN_IMG_1, pacman.move)

            # Check if pacman is on the same coordinates as the ghost, if yes, kill pacman or ghost
            if pacman.val in ghosts:
                if pacman.val == blue.id and power_up and blue.img == PU_GHOST:
                    ghost_died(blue, lvl_board)
                elif pacman.val == pink.id and power_up and pink.img == PU_GHOST:
                    ghost_died(pink, lvl_board)
                elif pacman.val == red.id and power_up and red.img == PU_GHOST:
                    ghost_died(red, lvl_board)
                elif pacman.val == yellow.id and power_up and yellow.img == PU_GHOST:
                    ghost_died(yellow, lvl_board)
                else:
                    pac_died(pacman, blue, pink, red, yellow, lvl_board)

            if pacman.val == 1:
                POINTS += 10

            # If pacman ate big circle, then run power up
            if pacman.val == 2:
                power_up = True
                power_up_turns = 0
                if not is_ghost_in_prison(blue.x, blue.y):
                    blue.img = PU_GHOST
                if not is_ghost_in_prison(pink.x, pink.y):
                    pink.img = PU_GHOST
                if not is_ghost_in_prison(red.x, red.y):
                    red.img = PU_GHOST
                if not is_ghost_in_prison(yellow.x, yellow.y):
                    yellow.img = PU_GHOST

            # Blue ghost moves or kills the pac man
            if pacman.alive:
                if TURN > 10:
                    # if function return false - pacman died
                    if not ghost_make_move(blue, lvl_board, power_up):
                        pac_died(pacman, blue, pink, red, yellow, lvl_board)

            # Pink ghost moves or kills the pac man
            if pacman.alive:
                if TURN > 20:
                    if not ghost_make_move(pink, lvl_board, power_up):
                        # if function return false - pacman died
                        pac_died(pacman, blue, pink, red, yellow, lvl_board)

            # Red ghost moves or kills the pac man
            if pacman.alive:
                if TURN > 40:
                    if not ghost_make_move(red, lvl_board, power_up):
                        # if function return false - pacman died
                        pac_died(pacman, blue, pink, red, yellow, lvl_board)

            # Yellow ghost moves or kills the pac man
            if pacman.alive:
                if TURN > 60:
                    if not ghost_make_move(yellow, lvl_board, power_up):
                        # if function return false - pacman died
                        pac_died(pacman, blue, pink, red, yellow, lvl_board)

            if LIVES == -1:
                break

            TURN += 1
            show_game(pacman, blue, pink, red, yellow, lvl_board)

        # Disable power up and reset ghosts images
        if power_up_turns == 50:
            power_up = False
            blue.img = blue.main_img
            pink.img = pink.main_img
            red.img = red.main_img
            yellow.img = yellow.main_img

        # Check if pacman ate all little circles, if yes, then set starting values and change level
        if check_win(lvl_board):
            pacman.rotate_img(PACMAN_IMG_1, 3)
            start = True
            LVL += 1
            TURN = 0
            power_up = False
            pacman.set_default()
            blue.set_default()
            pink.set_default()
            red.set_default()
            yellow.set_default()

            if LVL == 2:
                RUNNING = False
                GAME_WON = True
                for live in range(LIVES):
                    POINTS += 200
            else:
                pause_or_next_lvl(NEXT_LVL)


def main_menu():
    global GAME_WON

    while True:
        screen.fill("black")

        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.blit(MAIN_IMG, (0, 0))

        start_button = START_BUTTON.get_rect(topleft=(327, 443))
        screen.blit(START_BUTTON, start_button)

        exit_button = EXIT_BUTTON.get_rect(topleft=(327, 543))
        screen.blit(EXIT_BUTTON, exit_button)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if start_button.collidepoint((mouse_x, mouse_y)):
            if click:
                game()
                if POINTS > BEST_SCORE:
                    save_new_score()
                if GAME_WON:
                    image = WON_IMG
                else:
                    image = LOST_IMG
                game_over(image)
                reset_game()

        if exit_button.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 20)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    with open("best_score", "rt") as file:
        try:
            BEST_SCORE = int(file.readline())
        except:
            pass

    main_menu()

    pygame.quit()
