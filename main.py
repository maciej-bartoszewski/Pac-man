import math
import sys
import copy
from boards_in_game import boards
from data import *
from classes import *


def check_win(board):
    dots_on_board = 0
    for row in board:
        dots_on_board += row.count(1)

    if dots_on_board:
        return False
    return True


def reset_game():
    GameData.LVL = 0
    GameData.POINTS = 0
    GameData.RUNNING = True
    GameData.TURN = 0
    GameData.LIVES = 3
    GameData.GAME_WON = False


def save_new_score():
    GameData.BEST_SCORE = GameData.POINTS

    with open("best_score", "wt") as file:
        file.write(str(GameData.POINTS))


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

    for live in range(GameData.LIVES):
        screen.blit(HEART, (770 - (live * 40), 830))

    score_text = font.render(f"Score: {GameData.POINTS}", True, 'white')
    screen.blit(score_text, (20, 830))

    best_score_text = font.render(f"Best score: {GameData.BEST_SCORE}", True, 'white')
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
                    if GameData.POINTS > GameData.BEST_SCORE:
                        save_new_score()
                    main_menu()
                if event.key == pygame.K_SPACE:
                    return

        pygame.display.update()


def game():
    ghosts = [13, 14, 15, 16]
    power_up = False
    start = True
    power_up_turns = 0
    pacman = Pacman(10, PACMAN_IMG_1)
    blue = Ghost(13, BLUE_GHOST)
    pink = Ghost(14, PINK_GHOST)
    red = Ghost(15, RED_GHOST)
    yellow = Ghost(16, YELLOW_GHOST)

    game_boards = copy.deepcopy(boards)

    while GameData.RUNNING:
        screen.fill("black")
        clock.tick(60)

        if not pacman.alive:
            pacman.alive = True

        lvl_board = game_boards[GameData.LVL]
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
                    blue.ghost_died(lvl_board)
                elif pacman.val == pink.id and power_up and pink.img == PU_GHOST:
                    pink.ghost_died(lvl_board)
                elif pacman.val == red.id and power_up and red.img == PU_GHOST:
                    red.ghost_died(lvl_board)
                elif pacman.val == yellow.id and power_up and yellow.img == PU_GHOST:
                    yellow.ghost_died(lvl_board)
                else:
                    pacman.pac_died(blue, pink, red, yellow, lvl_board)

            if pacman.val == 1:
                GameData.POINTS += 10

            # If pacman ate big circle, then run power up
            if pacman.val == 2:
                power_up = True
                power_up_turns = 0
                if not blue.is_ghost_in_prison():
                    blue.img = PU_GHOST
                if not pink.is_ghost_in_prison():
                    pink.img = PU_GHOST
                if not red.is_ghost_in_prison():
                    red.img = PU_GHOST
                if not yellow.is_ghost_in_prison():
                    yellow.img = PU_GHOST

            # Blue ghost moves or kills the pac man
            if pacman.alive:
                if GameData.TURN > 10:
                    # if function return false - pacman died
                    if not blue.ghost_make_move(lvl_board, power_up):
                        pacman.pac_died(blue, pink, red, yellow, lvl_board)

            # Pink ghost moves or kills the pac man
            if pacman.alive:
                if GameData.TURN > 20:
                    if not pink.ghost_make_move(lvl_board, power_up):
                        # if function return false - pacman died
                        pacman.pac_died(blue, pink, red, yellow, lvl_board)

            # Red ghost moves or kills the pac man
            if pacman.alive:
                if GameData.TURN > 40:
                    if not red.ghost_make_move(lvl_board, power_up):
                        # if function return false - pacman died
                        pacman.pac_died(blue, pink, red, yellow, lvl_board)

            # Yellow ghost moves or kills the pac man
            if pacman.alive:
                if GameData.TURN > 60:
                    if not yellow.ghost_make_move(lvl_board, power_up):
                        # if function return false - pacman died
                        pacman.pac_died(blue, pink, red, yellow, lvl_board)

            if GameData.LIVES == -1:
                break

            GameData.TURN += 1
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
            GameData.LVL += 1
            GameData.TURN = 0
            power_up = False
            pacman.set_default()
            blue.set_default()
            pink.set_default()
            red.set_default()
            yellow.set_default()

            if GameData.LVL == 2:
                GameData.RUNNING = False
                GameData.GAME_WON = True
                for live in range(GameData.LIVES):
                    GameData.POINTS += 200
            else:
                pause_or_next_lvl(NEXT_LVL)


def main_menu():
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
                if GameData.POINTS > GameData.BEST_SCORE:
                    save_new_score()
                if GameData.GAME_WON:
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
    with open("best_score", "rt") as file:
        try:
            GameData.BEST_SCORE = int(file.readline())
        except:
            pass

    main_menu()

    pygame.quit()
