import pygame, sys
import random as rd
from config import *
from pygame.locals import *
from disc import *

# Init game
pygame.init()

FPS = 60
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# .Rect(x position, y position, width, height)
DROP_BUTTON = pygame.Rect(20, 20, 200, 100)

font = pygame.font.Font(None, 36)  # None = default font, 36 = size
TEXT_SURF = font.render("Drop", True, BLACK)  # True = anti-aliasing

TEXT_RECT = TEXT_SURF.get_rect(center=DROP_BUTTON.center)

def drawCircle(disc):
    pygame.draw.circle(screen, disc.color, (disc.x, disc.y), disc.radius, width=0)

def generateBall(s):
    x = rd.uniform(LEFT, RIGHT)
    y = START_HEIGHT

    s.add(Ball(x, y, BALL_SIZE, BALL_COLOR))

def removeBall(s):
    for ball in s.copy():
        if (ball.y >= END_HEIGHT):
            s.remove(ball)

ballList = set()
pegList = set()

def generatePeglist():
    y = START_HEIGHT + 100
    l = LEFT - 10
    r = RIGHT + 10
    xdif = (r - l) // 2
    ydif = 40
    for numball in range(3, 18):
        for x in range(l, r + 1, xdif):
            pegList.add(Peg(x = x, y = y, radius = PEG_SIZE, color = PEG_COLOR))
        l -= xdif // 2
        r += xdif // 2
        y += ydif

generatePeglist()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and DROP_BUTTON.collidepoint(event.pos):
                generateBall(ballList)

    # Limit tick rate
    clock.tick(FPS)

    # redraw new screen
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BUTTON_COLOR, DROP_BUTTON, width = 0)
    screen.blit(TEXT_SURF, TEXT_RECT)

    # draw discs
    for ball in ballList:
        drawCircle(ball)

    for peg in pegList:
        drawCircle(peg)

    # move one tick
    for ball in ballList:
        ball.tick()

    for ball in ballList:
        for peg in pegList:
            ball.bounce(peg)

    # remove balls
    removeBall(ballList)

    pygame.display.flip()

