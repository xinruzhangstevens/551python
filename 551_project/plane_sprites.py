import random
import pygame
# constant
# Screen size
SCREEN_RECT = pygame.Rect(0,0,1200,800)
# Frame rate
FRAME_PER_SEC = 60
# Enemy timer
CREATE_ENEMY_EVENT = pygame.USEREVENT
# Launch bullets
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# Boss timer
CREATE_BOSS_EVENT =pygame.USEREVENT+2
# Bubble timer
CREATE_BUBBLE_EVENT = pygame.USEREVENT +3
# Bullet_hit_boss
BULLET_HIT_BOSS_TIMES = 20
# Boss blood
HPFULL = 500
# Enemy_hit_dict
enemy_hit_dict = dict()

# Font
pygame.init()
game_font = pygame.font.SysFont('arial',16,True)

class GameSprite(pygame.sprite.Sprite):
    """Sprites"""

    def __init__(self, image_name, speed = 2,speedy = 0):

        # call Father class init
        super().__init__()

        # Define the attribute
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.speedy = speedy

    def update(self):

        # Move in vertical direction
        self.rect.y +=self.speed

class Background(GameSprite):
    """Background Sprite"""
    def __init__(self,is_alt= False):
        # 1.Call Father class init
        super().__init__('./picture/background4.png')
        # Judge whether it is the same picture. If so, set the initial location
        if is_alt:
            self.rect.x = -self.rect.width

    def update(self):

        # 1.Call Father class init
        # super().update()
        self.rect.x +=self.speed
        # 2.Judge whether the picture is out of the screen. If so, put the picture above the screen.
        if self.rect.x>=SCREEN_RECT.width:
            self.rect.x = -self.rect.width

class Enemy(GameSprite):
    """Enemy sprite"""

    def __init__(self):

        #1.Call Father class init,set image and speed
        super().__init__('./picture/ufo1.png')
        #2.set random speed
        self.speed = random.randint(1,6)
        #3.set random location
        self.rect.bottom = 0
        self.explode_index = 0

        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):

        #1.
        super().update()
        #2.Judge whether the picture is out of the screen.
        if self.rect.y>=SCREEN_RECT.height:
            #print('fly out of the screen ,delete it.')
            self.kill()


        #enemy explosion
        if self.explode_index!= 0 and self.explode_index <  4:
            new_rect = self.rect
            super().__init__('./picture/bomb1%d.png'% self.explode_index)
            self.explode_index += 1
            self.rect = new_rect


    def __del__(self):

        pass

class Hero(GameSprite):
    """Hero Sprite"""
    def __init__(self,path):

        # 1.Call Father class init,set image and speed
        super().__init__(path, 0)
        # 2. Set hero initial location
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom-120
        # 3.Create bullets sprite
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.mainexplode_index =0

    def update(self):
        # move in horizontal direction
        self.rect.x += self.speed
        self.rect.y +=self.speedy
        # Judge whether the picture is out of the screen. If so, put the picture above the screen.
        if self.rect.x < 0 :
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        if self.rect.y < 0 :
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

        # Explosion
        if self.mainexplode_index !=0 and self.mainexplode_index <4:
            new_rect = self.rect
            super().__init__('./picture/bomb1%d.png'% self.mainexplode_index)
            self.rect.centerx = new_rect.centerx
            self.rect.bottom = new_rect.bottom
            self.mainexplode_index += 1
            self.rect = new_rect

    def fire(self):
        for i in (0,1,2):
            # 1.Create bullet sprite
            bullet= Bullet()
            if self.mainexplode_index ==4:
                bullet.kill()
            # 2.Set the initial location
            bullet.rect.centerx = self.rect.centerx+30
            bullet.rect.centery = self.rect.centery-140+i*40
            # 3. Add bullets sprite into sprite group
            self.bullets.add(bullet)

class Bullet(GameSprite):
    """Bullet Sprite"""
    def __init__(self):
        # Call Father class init,set image and speed
        super().__init__('./images/bullet1.png',-2)

    def update(self):
        # Call Father class update
        super().update()
        # Judge whether the picture is out of the screen.
        if self.rect.bottom<0:
            self.kill()


    def __del__(self):
        pass

class Boss(GameSprite):
    """boss sprite
    """
    def __init__(self):
        # 1.Call Father class init,set image
        super().__init__('./picture/thanos1.png')
        # 2.Set initial location
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.top = SCREEN_RECT.top+20
        # 3. Create weapon sprite
        self.weapons = pygame.sprite.Group()
        self.exist = False
        self.bossexplode_index = 0
        self.bulletseating = 0
        self.hp_left = self.rect.width
        HPFULL = self.rect.width
        self.dHP = HPFULL / BULLET_HIT_BOSS_TIMES
        self.oldpercent = 0

    def update(self):
        self.rect.x +=self.speed
        if self.rect.x < 0 :
            self.rect.x = 0
            self.speed=-self.speed
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
            self.speed=-self.speed
        if self.exist == False:
            self.weapons.empty()

        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.rect.width, 10), 1)


        # boss explosion
        if self.bossexplode_index !=0 and self.bossexplode_index < 7:
            new_rect = self.rect
            super().__init__('./picture/bossbomb%d.png' % self.bossexplode_index)
            self.rect.centerx = new_rect.centerx
            self.rect.bottom = new_rect.bottom
            self.bossexplode_index += 1
            self.rect = new_rect

    def bubble(self):
        for i in (0,1):
            weapon = Weapon()
            weapon.rect.bottom = self.rect.bottom+50
            weapon.rect.centerx = self.rect.centerx+20-i*20
            self.weapons.add(weapon)

class Weapon(GameSprite):
    """weapon sprite"""
    def __init__(self):
<<<<<<< HEAD
        super().__init__('./images/weapon.png',10)
        
=======
        super().__init__('./picture/weapon.png',10)
>>>>>>> 7e7f493267f8a22025806a6c4eaea0e8856ec82c
    def update(self):
        super().update()
        if self.rect.y>SCREEN_RECT.height:
            self.kill()

    def __del__(self):
        #print('weapon delete')
        pass

