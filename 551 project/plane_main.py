import random
import  pygame
from plane_sprites import *
score = 0
ENEMY_SCORE = 100
BOSSBORN = False
game_font_start = pygame.font.SysFont('arial',30,True)
game_font_over = pygame.font.SysFont('arial',50,True)

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        #print('init...')

        #1.创建游戏的窗口
        # pygame.display.set_caption('This is my first pygame-program')  # 设置窗口标题
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #2。创建游戏的时钟
        self.clock = pygame.time.Clock()
        #3。调用私有方法，精灵和精灵组的创建
        self.__create__sprites()

        #4.设置定时器事件-创建敌机 1s
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1500)
        pygame.time.set_timer(HERO_FIRE_EVENT,600)
        pygame.time.set_timer(CREATE_BOSS_EVENT,5000)
        pygame.time.set_timer(CREATE_BUBBLE_EVENT,5000)


    def create_background(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # )
        self.back_group.update()

    def __create__sprites(self):

        self.create_background()

        self.back_group.draw(self.screen)
        pygame.display.update()

        while True:
            keys_pressed = pygame.key.get_pressed()
            pygame.key.get_mods()
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
                # if keys_pressed[pygame.K_1]:
            if keys_pressed[pygame.K_2]:
                path = "./picture/ironmanm.png"
                break
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    PlaneGame.__game_over()

        #创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        #创建英雄的精灵和精灵组
        self.hero = Hero(path)
        self.hero_group = pygame.sprite.Group(self.hero)

        #创建子弹敌机碰撞精灵组
        self.enemyb_hit_group = pygame.sprite.Group()

        #创建boss精灵
        self.boss = Boss()
        self.boss_group = pygame.sprite.Group()

    def start_game(self):
        print('game starts')


        while True:

            #设置英雄毁灭时的帧率
            # if self.hero.mainexplode_index==5:
            #     FRAME_PER_SEC=60
            # else:
            #     FRAME_PER_SEC=60
            #设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            #事件监听
            self.event__handler()
            #碰撞检测
            self.__check_collider()
            #更新/绘制精灵组
            self.__update_sprites()
            #更新屏幕显示
            pygame.display.update()

    def event__handler(self):
        global BOSSBORN
        for event in pygame.event.get():
            #判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            if event.type == CREATE_ENEMY_EVENT and len(self.boss_group)==0:
                #print('emeny showtime')
                #创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            # elif event.type == pygame.KEYDOWN and event.key ==pygame.K_RIGHT:
            #     print(" move right")
            if event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            if event.type == CREATE_BOSS_EVENT and BOSSBORN == False:
                BOSSBORN = True
                self.boss_group.add(self.boss)
                self.boss.exist=True
            if self.boss.exist and event.type == CREATE_BUBBLE_EVENT:
                self.boss.bubble()

        #使用键盘提供的方法获取键盘按键
        keys_pressed = pygame.key.get_pressed()
        pygame.key.get_mods()
        #判断元组中对应的按键索引值
        self.move(keys_pressed)

    def move(self,keys_pressed):
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_DOWN] or keys_pressed[
            pygame.K_UP]:
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

        #1.子弹摧毁敌机
        #在敌机被消灭时显示爆炸过程
        #敌机与子弹相撞时先不移出敌机精灵
        enemy_bullet_hit_dict = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,False)
        global score
        global ENEMY_SCORE
        score += len(enemy_bullet_hit_dict)*ENEMY_SCORE
        self.enemyb_hit_group.add(enemy_bullet_hit_dict.values())
        # print(enemy_bullet_hit_dict.values())
        for enemy1 in self.enemyb_hit_group:
            if enemy1.explode_index ==0:
                #判断是否输出爆照效果图
                enemy1.explode_index = 1

                #判断在爆照效果图输完后删除精灵
            elif enemy1.explode_index == 4:
                self.enemyb_hit_group.remove_internal(enemy1)
                self.enemy_group.remove_internal(enemy1)

        #2.敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero,self.enemy_group,True)
        # 3.bubble撞毁英雄
        bubbles = pygame.sprite.spritecollide(self.hero, self.boss.weapons, True)
        #判断列表是否有内容

        if len(enemies) > 0 or len(bubbles)>0:
            for hero1 in self.hero_group:
                if self.hero.mainexplode_index == 0:
                    self.hero.mainexplode_index =1
        if self.hero.mainexplode_index == 4:
            self.hero.kill()
            # self.hero_group.remove_internal(self)
            self.__game_over()

        #4。子弹撞毁boss
        bullets_eating_onetime = len(pygame.sprite.groupcollide(self.boss_group,self.hero.bullets,False,True))
        self.boss.bulletseating += bullets_eating_onetime
        if self.boss.hp_left >= 0 and bullets_eating_onetime >= 0:
            self.boss.hp_left -= self.boss.dHP * bullets_eating_onetime
            print(self.boss.hp_left)
            pygame.draw.rect(self.boss.image, (0, 0, 0), (0, 0, self.boss.rect.width, 10), 10)
            pygame.draw.rect(self.boss.image, (0, 255, 0), (0, 0, self.boss.hp_left, 10), 10)
        #print(len(self.boss_group))
        # switch = False
            #print(boss1)
        if self.boss.bulletseating > BULLET_HIT_BOSS_TIMES:

            if self.boss.bossexplode_index ==0:
                self.boss.bossexplode_index =1
        if self.boss.bossexplode_index == 7:
            if len(self.boss_group) == 1 and self.boss.exist:
                score +=1000

            self.boss.kill()
            self.boss.exist=False
            self.__game_win()
            # switch = True
            # self.boss_group.remove_internal(boss1)
        # if switch:


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


    #@staticmethod
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

    #创建游戏对象
    game = PlaneGame()

    #启动游戏
    game.start_game()