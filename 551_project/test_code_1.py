from plane_sprites import *
class test_AvengersWar(object):
    def __init__(self):
        self.test__create__sprites()

    def test__create__sprites(self):
        self.hero = Hero('./551_project/picture/spiderman11.png')
        self.hero_group = pygame.sprite.Group(self.hero)

    def test_move(self):
        if True:
            self.move_right(True)

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

def test_sample():
    game = test_AvengersWar()
    x = game.hero.rect.centerx
    y = game.hero.rect.centery
    print(x,y)
    game.test_move()
    game.hero.update()

    x_new = game.hero.rect.centerx
    y_new = game.hero.rect.centery
    print(x_new, y_new)
    print(game.hero.speed)
    assert(x == (x_new - game.hero.speed) and y == y_new)

test_sample()
