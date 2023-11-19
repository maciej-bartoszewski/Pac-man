import pygame


class GameData:
    # Global game variables
    POINTS = 0
    BEST_SCORE = 0
    LVL = 0
    TURN = 0
    RUNNING = True
    GAME_WON = False
    LIVES = 3


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

# Pygame settings
pygame.init()
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
