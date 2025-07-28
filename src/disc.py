import pygame 
from config import *

class Disc:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.color = color

    def addVelo(self, ax, ay):
        self.vx += ax
        self.vy += ay
    
    def setVelo(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def tick(self): 
        self.x += self.vx
        self.y += self.vy


        
class Peg(Disc):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, radius, color)

def norm(x):
    if (0 < abs(x) and abs(x) < 0.3):
        return 0.3 * x / abs(x)
    return x

class Ball(Disc):
    gravity = GRAVITY
    damp = DAMP
    mid = MID

    def dampen(self):
        self.vx *= self.damp
        self.vy *= self.damp

    def tick(self):
        super().tick()
        super().addVelo(0, self.gravity)
        self.dampen()
        # self.vx = norm(self.vx)
        # self.vy = norm(self.vy)

    def bounce(self, peg):
        # check sub-step to avoid missing collision
        stepsize = 3
        for step in range(stepsize):
            x = self.x + self.vx * step / stepsize
            y = self.y + self.vy * step / stepsize
            dif = pygame.math.Vector2(x - peg.x, y - peg.y)

            if (dif.length() <= self.radius + peg.radius):
                vel = pygame.math.Vector2(self.vx, self.vy)
                newvel = vel.reflect(dif)

                (self.vx, self.vy) = (newvel.x, newvel.y)
                if ((self.mid - self.x) * self.vx < 0):
                    self.vx *= 0.65
                    if (abs(self.vx) < 1):
                        self.vx /= abs(self.vx)
                break

        


