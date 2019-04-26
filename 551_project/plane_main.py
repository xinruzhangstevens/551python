import random
import  pygame
from plane_sprites import *
score = 0
ENEMY_SCORE = 100
BOSSBORN = False
game_font_start = pygame.font.SysFont('arial',30,True)
game_font_over = pygame.font.SysFont('arial',50,True)


class AvengersWar(object):
    """main_avengers_war"""

    def __init__(self):
        # 1. Build a window_screen
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. Set time_clock
        self.clock = pygame.time.Clock()
        # 3.Call private methods and create sprites_Groups
        self.__create__sprites()

        # 4.Set timer events
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1500)
        pygame.time.set_timer(HERO_FIRE_EVENT,200)
        pygame.time.set_timer(CREATE_BOSS_EVENT,15000)
        pygame.time.set_timer(CREATE_BUBBLE_EVENT,3000)

    def create_background(self):
        # Create background sprite ans corresponding sprite_Group
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        self.back_group.update()

    def __create__sprites(self):

        self.create_background()
        self.back_group.draw(self.screen)
        pygame.display.update()

        while True:
            # There are two superheroes that the players can select.Press 1: Spiderman. Press 2: Ironman
            keys_pressed = pygame.key.get_pressed()
            pygame.key.get_mods()
            self.screen.blit(game_font_over.render(u'AvengersWar' , True, [255, 0, 0]), [450, 100])
            self.screen.blit(game_font_start.render(u'Choose your favorite superhero' , True, [0, 255, 0]), [400, 250])
            bg = pygame.image.load("./picture/spiderman11.png")
            self.screen.blit(game_font_start.render(u'Press 1' , True, [0, 255, 0]), [300, 400])
            bg1 = pygame.image.load("./picture/ironmanm.png")
            self.screen.blit(game_font_start.render(u'Press 2' , True, [0, 255, 0]), [900, 400])

            self.screen.blit(bg, (150, 300))
            self.screen.blit(bg1, (750, 300))
            pygame.display.update()
            if keys_pressed[pygame.K_1]:
                path = "./picture/spiderman11.png"
                break
            if keys_pressed[pygame.K_2]:
                path = "./picture/ironmanm.png"
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    AvengersWar.__game_over()

        # Create an enemies--UFOs sprite Group
        self.enemy_group = pygame.sprite.Group()

        # Create a superheroes sprite Group
        self.hero = Hero(path)
        self.hero_group = pygame.sprite.Group(self.hero)

        # Create an enemy_bullets_hit sprite Group
        self.enemyb_hit_group = pygame.sprite.Group()

        # Create a boss sprite Group
        self.boss = Boss()
        self.boss_group = pygame.sprite.Group()

    def start_game(self):
        print('game starts')


        while True:

            self.clock.tick(FRAME_PER_SEC)
            self.event__handler()
            self.__check_collider()
            self.__update_sprites()
            pygame.display.update()

    def event__handler(self):
        global BOSSBORN
        for event in pygame.event.get():
            # Judge quit or not
            if event.type == pygame.QUIT:
                AvengersWar.__game_over()

            if event.type == CREATE_ENEMY_EVENT and len(self.boss_group)==0:
                # Instantiate enemy
                enemy = Enemy()
                # Add Enemy sprite to Enemy_Group
                self.enemy_group.add(enemy)

            if event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            if event.type == CREATE_BOSS_EVENT and BOSSBORN == False:
                BOSSBORN = True
                self.boss_group.add(self.boss)
                self.boss.exist=True

            if self.boss.exist and event.type == CREATE_BUBBLE_EVENT:
                self.boss.bubble()

        # Get key_pressed
        keys_pressed = pygame.key.get_pressed()
        pygame.key.get_mods()
        # Judge the corresponding index
        self.move(keys_pressed)

    def move(self,keys_pressed):
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_UP]:
            self.move_right(keys_pressed[pygame.K_RIGHT])
            self.move_left(keys_pressed[pygame.K_LEFT])
            self.move_up(keys_pressed[pygame.K_UP])
            self.move_down(keys_pressed[pygame.K_DOWN])
        elif pygame.KEYUP:
            self.hero.speed = 0
            self.hero.speedy = 0

    def move_right(self,keys_pressed):
        if keys_pressed:
            self.hero.speed = 10

    def move_left(self,keys_pressed):
        if keys_pressed:
            self.hero.speed = -10

    def move_down(self, keys_pressed):
        if keys_pressed:
            self.hero.speedy = 10

    def move_up(self, keys_pressed):
        if keys_pressed:
            self.hero.speedy = -10

    def __check_collider(self):

        # 1.enemy_bullet_hit
        # Show the explosion.
        enemy_bullet_hit_dict = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,False)
        global score
        global ENEMY_SCORE
        score += len(enemy_bullet_hit_dict)*ENEMY_SCORE
        self.enemyb_hit_group.add(enemy_bullet_hit_dict.values())
        # print(enemy_bullet_hit_dict.values())
        for enemy1 in self.enemyb_hit_group:
            if enemy1.explode_index ==0:
                # The index that call the explosion pictures method
                enemy1.explode_index = 1

                # The index that delete the spirte
            elif enemy1.explode_index == 4:
                self.enemyb_hit_group.remove_internal(enemy1)
                self.enemy_group.remove_internal(enemy1)

        # 2. ememies_hero_hit
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        # 3.bubbles_hero_hit
        bubbles = pygame.sprite.spritecollide(self.hero, self.boss.weapons, True)
        #If exists collider_event(enemies or bubles), delete the superhero.

        if len(enemies) > 0 or len(bubbles)>0:
            for hero1 in self.hero_group:
                if self.hero.mainexplode_index == 0:
                    self.hero.mainexplode_index =1
        if self.hero.mainexplode_index == 4:
            self.hero.kill()
            self.__game_over()

        # 4. bullets_boss_hit
        bullets_eating_onetime = len(pygame.sprite.groupcollide(self.boss_group,self.hero.bullets,False,True))
        self.boss.bulletseating += bullets_eating_onetime
        if self.boss.hp_left >= 0 and bullets_eating_onetime >= 0:
            self.boss.hp_left -= self.boss.dHP * bullets_eating_onetime
            #print(self.boss.hp_left)
            pygame.draw.rect(self.boss.image, (0, 0, 0), (0, 0, self.boss.rect.width, 10), 10)
            pygame.draw.rect(self.boss.image, (0, 255, 0), (0, 0, self.boss.hp_left, 10), 10)
        if self.boss.bulletseating > BULLET_HIT_BOSS_TIMES:

            if self.boss.bossexplode_index ==0:
                self.boss.bossexplode_index =1
        if self.boss.bossexplode_index == 7:
            if len(self.boss_group) == 1 and self.boss.exist:
                score +=1000

            self.boss.kill()
            self.boss.exist=False
            self.__game_win()

    def __update_sprites(self):
        self.screen.blit(game_font.render(u'score: %d' % score, True, [255, 0, 0]), [20, 20])
        pygame.display.update()

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.boss_group.update()
        self.boss_group.draw(self.screen)

        self.boss.weapons.update()
        self.boss.weapons.draw(self.screen)

    def __game_over(self):
        keys_pressed = pygame.key.get_pressed()
        pygame.key.get_mods()
        self.screen.blit(game_font_over.render(u'Game Over.', True, [255, 0, 0]), [500, 300])
        self.screen.blit(game_font_over.render(u'Congratulations! Earth is gone ^-^', True, [255, 0, 0]), [300, 400])
        self.screen.blit(game_font_start.render(u'Press Esc to exit', True, [0, 255, 0]), [980, 750])
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    def __game_win(self):
        keys_pressed = pygame.key.get_pressed()
        pygame.key.get_mods()
        self.screen.blit(game_font_over.render(u'Earth is safe now!!!', True, [255, 0, 0]), [500, 400])
        self.screen.blit(game_font_start.render(u'Press Esc to exit', True, [0, 255, 0]), [980, 750])
        if keys_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

if __name__ == '__main__':

    game = AvengersWar()
    game.start_game()
