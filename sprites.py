import pygame as pg
from tilemap import collide_hit_rect
from settings import *
vec=pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False,collide_hit_rect)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False,collide_hit_rect)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos,dir):
        self.groups = game.all_sprites,game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir.rotate(10)*BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()
    def update(self):
        self.pos += self.vel *self.game.dt
        self.rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time>BULLET_LIFETIME:
            self.kill()
        if pg.sprite.spritecollideany(self,self.game.walls):
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.image = pg.image.load('wizard4.png')
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.player_img=self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.last_shot = 0
        self.health = 100
        # self.vx, self.vy = 0, 0
        # self.x = x * TILESIZE
        # self.y = y * TILESIZE
        self.vel=vec(0,0)
        self.pos=vec(x,y)* TILESIZE
        self.rot=0

    def get_keys(self):
        self.rot_speed=0
        self.vel=vec(0,0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel =vec(PLAYER_SPEED,0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED/2).rotate(-self.rot)
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot >BULLET_RATE:
                self.last_shot = now
                dir = vec(1,0).rotate(-self.rot)
                pos = self.pos+BARREL_OFFSET.rotate(-self.rot)
                Bullet(self.game,pos,dir)

            # self.vy = PLAYER_SPEED
        # if self.vx != 0 and self.vy != 0:
        #     self.vx *= 0.7071
        #     self.vy *= 0.7071



    def update(self):
        self.get_keys()
        self.rot=(self.rot+self.rot_speed*self.game.dt)%360
        self.image=pg.transform.rotate(self.player_img,self.rot)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos
        self.pos+=self.vel*self.game.dt
        self.hit_rect.centerx=self.pos.x
        collide_with_walls(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self,self.game.walls,'y')
        self.rect.center = self.hit_rect.center


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image= pg.image.load('slime_monster_preview.png')
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.mob_img = self.image.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos=vec(x,y)* TILESIZE
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.rect.center=self.pos
        self.rot=0
        self.health = 100

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos -mob.pos
                if 0<dist.length()<AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.rot=(self.game.player.pos -self.pos). angle_to(vec(1,0))
        self.image=pg.transform.rotate(self.mob_img, self.rot)
        self.rect=self.image.get_rect()
        self.rect.center=self.pos

        self.acc=vec(1,0).rotate(-self.rot)
        self.avoid_mobs()
        self.acc.scale_to_length(MOB_SPEED)
        self.acc+= self.vel*-1
        self.vel+=self.acc*self.game.dt
        self.pos+=self.vel*self.game.dt+.5*self.acc*self.game.dt**2
        self.hit_rect.centerx=self.pos.x
        collide_with_walls(self,self.game.walls,'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,type):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        if self.type == 1:
            self.image=pg.image.load("bluewall.png")
            # self.image = pg.image.load('ChatGPT Image May 19, 2025, 12_00_06 PM.png')
        if self.type == 2:
            self.image = pg.image.load('May 19, 2025, 11_59_56 AM.png')
        if self.type == 3:
            self.image = pg.image.load('portal.png')
        self.image = pg.transform.scale(self.image,(TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
