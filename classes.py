import random
import pygame
from data import B_WIDTH, B_HEIGHT, PACMAN_IMG_1, PU_GHOST, GameData, screen


class Hero:
    def __init__(self, h_id, photo):
        self.id = h_id
        self.img = photo
        self.main_img = photo
        self.move = 3
        self.prev_move = 0
        self.starting_x = 0
        self.starting_y = 0
        self.x = 0
        self.y = 0
        self.allowed_moves = []
        self.prev_x = 0
        self.prev_y = 0
        self.val = 0
        self.prev_val = 0
        self.possible_moves = [True, True, True, True, True]
        self.draw_x = 0
        self.draw_y = 0

    def set_default(self):
        self.set_starting_cords_on_other()
        self.val = 0
        self.prev_val = 0
        self.move = 3
        self.prev_move = 3
        self.img = self.main_img

    def check_position(self, board):
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == self.id:
                    self.x = col
                    self.y = row
                    return

    def find_possible_moves(self, board):
        hero_moves = [True, True, True, True, True]

        if board[self.y + 1][self.x] not in self.allowed_moves:
            hero_moves[0] = False
        if board[self.y - 1][self.x] not in self.allowed_moves:
            hero_moves[1] = False
        if self.x != 0:
            if board[self.y][self.x - 1] not in self.allowed_moves:
                hero_moves[2] = False
        if self.x != 29:
            if board[self.y][self.x + 1] not in self.allowed_moves:
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

    def set_starting_cords_on_other(self):
        self.x = self.starting_x
        self.y = self.starting_y
        self.prev_x = self.starting_x
        self.prev_y = self.starting_y

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


class Pacman(Hero):
    def __init__(self, h_id, photo):
        super().__init__(h_id, photo)
        self.alive = True
        self.rotate_direction = 3

    def rotate_img(self, image, move):
        self.img = image
        if move == 0:
            self.img = pygame.transform.rotate(self.img, -90)
        if move == 1:
            self.img = pygame.transform.rotate(self.img, 90)
        if move == 2:
            self.img = pygame.transform.flip(self.img, True, False)

    def find_possible_moves(self, board):
        self.allowed_moves = [0, 1, 2, 11, 12, 13, 14, 15, 16]
        super().find_possible_moves(board)

    def pac_died(self, blue, pink, red, yellow, board):
        self.alive = False
        GameData.turn = 0

        board[self.y][self.x] = 0
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
        board[self.starting_y][self.starting_x] = 10

        self.set_default()
        blue.set_default()
        pink.set_default()
        red.set_default()
        yellow.set_default()

        if GameData.lives == 0:
            GameData.running = False
        GameData.lives -= 1

        self.rotate_img(PACMAN_IMG_1, 3)


class Ghost(Hero):
    def __init__(self, h_id, photo):
        super().__init__(h_id, photo)
        self.turns_to_wait = 0

    def set_default(self):
        super().set_default()
        self.turns_to_wait = 0

    def in_prison(self):
        if GameData.lvl == 0:
            if 11 < self.x < 18:
                if 13 < self.y < 17:
                    return True
            return False

        elif GameData.lvl == 1:
            if 12 < self.x < 17:
                if 13 < self.y < 16:
                    return True
            return False

        else:
            return False

    def find_possible_moves(self, board):
        self.allowed_moves = [0, 1, 2, 9, 10]
        if not self.in_prison():
            self.allowed_moves.remove(9)
        super().find_possible_moves(board)

    def next_move(self):
        if self.in_prison():
            # choose move when ghost is in prison
            new_move = 1
            if not self.possible_moves[1]:
                if not self.possible_moves[2]:
                    new_move = 3
                elif not self.possible_moves[3]:
                    new_move = 2
                else:
                    new_move = self.prev_move
        else:
            if True not in self.possible_moves[0:4]:
                new_move = 4
            else:
                # choose move when ghost isn't in prison
                allowed_without_coming_back = []
                for move_id in range(len(self.possible_moves) - 1):
                    if self.possible_moves[move_id]:
                        allowed_without_coming_back.append(move_id)
                if self.move == 0 and 1 in allowed_without_coming_back:
                    allowed_without_coming_back.remove(1)
                if self.move == 1 and 0 in allowed_without_coming_back:
                    allowed_without_coming_back.remove(0)
                if self.move == 2 and 3 in allowed_without_coming_back:
                    allowed_without_coming_back.remove(3)
                if self.move == 3 and 2 in allowed_without_coming_back:
                    allowed_without_coming_back.remove(2)

                if len(allowed_without_coming_back) == 0:
                    new_move = 4
                else:
                    new_move = random.choice(allowed_without_coming_back)

        return new_move

    def make_move(self, board, power_up):
        if self.turns_to_wait == 0:
            self.find_possible_moves(board)
            self.prev_move = self.move
            self.move = self.next_move()
            self.change_position(board)
            if self.val == 10:
                # if ghost is on the same coordinates as the pacman, kill pacman or ghost
                if power_up and self.img == PU_GHOST:
                    board[self.y][self.x] = 0
                    self.ghost_died(board)
                    self.turns_to_wait = 30
                    GameData.points += 200
                else:
                    # returning false - pacman died
                    return False
        # returning true - pacman is alive
        return True

    def ghost_died(self, board):
        GameData.points += 200
        board[self.starting_y][self.starting_x] = self.id
        self.set_default()
        self.turns_to_wait = 30
