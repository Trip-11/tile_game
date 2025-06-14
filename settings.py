import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# game settings
WIDTH = 768   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 576  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Game"
BGCOLOR = LIGHTGREY

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_SPEED = 300
PLAYER_ROT_SPEED=250
PLAYER_HIT_RECT = pg.Rect(0, 0, 36, 36)
PLAYER_HEALTH = 100

BARREL_OFFSET = vec(30,0)
BULLET_RATE = 150
BULLET_LIFETIME = 500

MOB_SPEED=100
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_KNOCKBACK = 20
MOB_DAMAGE = 10
MOB_HEALTH = 100
AVOID_RADIUS = 50

BULLET_SPEED = 500
BULLET_DAMAGE = 10