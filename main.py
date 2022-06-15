import pygame, sys, math, otherstuff, random

pygame.init()

clock = pygame.time.Clock()

width = 1270
height = 620
screen = pygame.display.set_mode((width, height))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Base(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

def closest(thingy, list):
    closest = list[0]
    for e in list:
        if math.dist((thingy.rect.centerx, thingy.rect.centery), (e.rect.centerx, e.rect.centery)) < math.dist((thingy.rect.centerx, thingy.rect.centery), (closest.rect.centerx, closest.rect.centery)):
            closest = e
    return closest

class Dagger(Base):
    def __init__(self, x, y, enemy_group, dmg):
        super().__init__()
        self.enemy_group = enemy_group
        self.rect = pygame.Rect((x, y), (32, 32))
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.lifetime = 30 * 20
        self.dmg = dmg
        self.diewhenhit = False
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        if len(self.enemy_group) > 0:
            target = self.enemy_group.sprites()[0]
            rot = math.atan2(self.rect.centery - target.rect.centery, self.rect.centerx - target.rect.centerx)
            self.image = pygame.transform.scale(
                pygame.transform.rotate(pygame.image.load("images/dagger.png"), -270 - (rot * (180 / math.pi))),
                (64, 64))
            self.rect.centerx -= math.cos(rot) * 20
            self.rect.centery -= math.sin(rot) * 20
        else:
            self.kill()

class Wall(Base):
   def __init__(self, x, y, x_speed, y_speed, image, dmg):
        super().__init__()
        self.image = image
        self.rect = pygame.Rect((x,y), self.image.get_size())
        self.size = 20
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.dmg = dmg
        self.diewhenhit = False

   def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

class Spell(Base):
    def __init__(self, x, y, target, dmg, enemy_group):
        super().__init__()
        self.rect = pygame.Rect((x, y), (8, 8))
        self.image = pygame.transform.scale(pygame.image.load("images/spell.png"), (8, 8))
        self.target = target
        self.dmg = dmg
        self.diewhenhit = True
        self.enemy_group = enemy_group
    def update(self):
        if self.target in self.enemy_group.sprites():
            rot = math.atan2(self.rect.centery - self.target.rect.centery, self.rect.centerx - self.target.rect.centerx)
            self.rect.x -= math.cos(rot) * 10
            self.rect.y -= math.sin(rot) * 10
        else:
            self.kill()

class Button(Base):
    def __init__(self, x, y, width, height, img1, img2):
        self.rect = pygame.Rect((x - width/2, y - height/2), (width, height))
        self.image = img1
        self.image1 = img1
        self.image2 = img2
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        col = self.rect.collidepoint(mouse_pos)
        if col and pygame.mouse.get_pressed()[0]:
            return True
        elif col:
            self.image = self.image2
        else:
            self.image = self.image1


class Entity(Base):
    def __init__(self, x, y, width, height, x_sped, y_sped, damage, lifetime, image, centerx = 0, centery = 0):
        super().__init__()
        self.rect = pygame.Rect((x, y), (width, height))
        if centerx != 0:
            self.rect.centerx = centerx
            self.rect.centery = centery
        self.image = image
        self.x_sped = x_sped
        self.y_sped = y_sped
        self.dmg = damage
        self.lifetime = lifetime
        self.diewhenhit = False

    def update(self):
        if self.lifetime <= 0:
            self.kill()
        self.lifetime -= 1
        self.rect.x -= self.x_sped
        self.rect.y -= self.y_sped

class Tank:
    def __init__(self):
        self.cooldown_countere = 0
        self.cooldown_counterq = 0
        self.cooldown_counterr = 0
        self.cooldown_countercl = 0
        self.health = 10
    def update(self, player, enemy_group, entity_group):

        self.cooldown_countere -= 1
        self.cooldown_counterq -= 1
        self.cooldown_counterr -= 1
        self.cooldown_countercl -= 1

        mouse_pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()

        if self.cooldown_counterq >= 30 * 19:
            player.invic = True
        else:
            player.invic = False
        if self.cooldown_counterr > 30 * 5:
            player.att = 2
        elif self.cooldown_counterr == 30 * 5:
            player.att = 1
            player.speed /= 3

        if pygame.mouse.get_pressed()[0]:
            if self.cooldown_countercl <= 0:
                new_entity = Entity(player.rect.centerx - 50, player.rect.centery - 50, 100, 100, 0, 0, 10, 1, pygame.transform.scale(pygame.image.load("images/jump.png"), (100, 100)))
                entity_group.add(new_entity)
                self.cooldown_countercl = 10
        elif key[pygame.K_e]:
            if self.cooldown_countere <= 0:
                new_entity = Entity(player.rect.centerx - 200, player.rect.centery - 200, 400, 400, 0, 0, 10, 1, pygame.transform.scale(pygame.image.load("images/jump.png"), (400, 400)))
                entity_group.add(new_entity)
                self.cooldown_countere = 30 * 5
        elif key[pygame.K_q]:
            if self.cooldown_counterq <= 0:
                self.cooldown_counterq = 30 * 15
        elif key[pygame.K_r]:
            if self.cooldown_counterr <= 0:
                self.cooldown_counterr = 30 * 25
                player.speed *= 3


class Wizard:
    def __init__(self):
        self.cooldown_countere = 0
        self.cooldown_counterq = 0
        self.cooldown_counterr = 0
        self.cooldown_countercl = 0
        self.health = 3
    def update(self, player, enemy_group, entity_group):

        self.cooldown_countere -= 1
        self.cooldown_counterq -= 1
        self.cooldown_counterr -= 1
        self.cooldown_countercl -= 1

        mouse_pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        if pygame.mouse.get_pressed()[0]:
            if self.cooldown_countercl <= 0 and len(enemy_group) > 0:
                closestenem = closest(player, enemy_group.sprites())
                new_spell = Spell(player.rect.centerx, player.rect.centery, closestenem, 10, enemy_group)
                entity_group.add(new_spell)
                self.cooldown_countercl = 20
        elif key[pygame.K_e]:
            if self.cooldown_countere <= 0:
                new_entity = Entity(mouse_pos[0] - 30, mouse_pos[1] - 30, 60, 60, 0, 0, 50, 10, pygame.transform.scale(pygame.image.load("images/spell.png"), (60, 60)))
                entity_group.add(new_entity)
                self.cooldown_countere = 30 * 5
        elif key[pygame.K_q]:
            if self.cooldown_counterq <= 0:
                self.cooldown_counterr = self.cooldown_counterr//2
                self.cooldown_countere = self.cooldown_countere//2
                self.cooldown_counterq = 30 * 15
        elif key[pygame.K_r]:
            if self.cooldown_counterr <= 0 and len(enemy_group) > 0:
                new_dagger = Dagger(player.rect.centerx, player.rect.centery, enemy_group, 10)
                entity_group.add(new_dagger)
                self.cooldown_counterr = 30 * 25



class Swordsman:
    def __init__(self):
        self.cooldown_countere = 0
        self.cooldown_counterq = 0
        self.cooldown_counterr = 0
        self.cooldown_countercl = 0
        self.rot = 0
        self.health = 5
        self.side = 1
    def update(self, player, enemy_group, entity_group):

        self.cooldown_countere -= 1
        self.cooldown_counterq -= 1
        self.cooldown_counterr -= 1
        self.cooldown_countercl -= 1
        self.rot = (self.rot + math.pi/30) % (2 * math.pi)

        if self.cooldown_counterq == 30 * 5:
            player.speed /= 2
        if self.cooldown_counterr > 30 * 15:
            img = pygame.transform.rotozoom(pygame.image.load("images/spin.png"), self.cooldown_counterr/3, 2)
            new_entity = Entity(player.rect.centerx - 100, player.rect.centery - 100, 200, 200, 0, 0, 10, 1, img, player.rect.centerx, player.rect.centery)
            entity_group.add(new_entity)
        elif self.cooldown_counterr == 30 * 15:
            player.speed /= 1.2

        key = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        rot = math.atan2(player.rect.centery - mouse_pos[1], player.rect.centerx - mouse_pos[0])
        if self.cooldown_countercl > 0:
            if self.side == 1:
                if self.cooldown_countercl > 5 and self.cooldown_countercl < 15:
                    pygame.draw.line(screen, BLUE, (player.rect.centerx, player.rect.centery), (player.rect.centerx - (math.cos(rot - (math.pi/30 * (self.cooldown_countercl//2)))) * 100, player.rect.centery - (math.sin(rot - (math.pi/30 * (self.cooldown_countercl//2)))) * 100), 5)
                elif self.cooldown_countercl <= 5:
                    pygame.draw.line(screen, BLUE, (player.rect.centerx, player.rect.centery), (player.rect.centerx - (math.cos(rot + math.pi/6 - (math.pi/30 * self.cooldown_countercl))) * 100, player.rect.centery - (math.sin(rot + math.pi/6 - (math.pi/30 * self.cooldown_countercl))) * 100), 5)
            else:
                if self.cooldown_countercl > 5 and self.cooldown_countercl < 15:
                    pygame.draw.line(screen, BLUE, (player.rect.centerx, player.rect.centery), (player.rect.centerx - (math.cos(rot + (math.pi/30 * (self.cooldown_countercl//2)))) * 100, player.rect.centery - (math.sin(rot + (math.pi/30 * (self.cooldown_countercl//2)))) * 100), 5)
                elif self.cooldown_countercl <= 5:
                    pygame.draw.line(screen, BLUE, (player.rect.centerx, player.rect.centery), (player.rect.centerx - (math.cos(rot - math.pi/6 + (math.pi/30 * self.cooldown_countercl))) * 100, player.rect.centery - (math.sin(rot - math.pi/6 + (math.pi/30 * self.cooldown_countercl))) * 100), 5)
        if pygame.mouse.get_pressed()[0]:
            if self.cooldown_countercl <= 0:
                self.side = random.randint(1, 2)
                angle1 = rot - math.pi/6
                angle2 = rot + math.pi/6
                A = (player.rect.centerx, player.rect.centery)
                B = (player.rect.centerx - math.cos(angle1) * 100, player.rect.centery - math.sin(angle1) * 100)
                C = (player.rect.centerx - math.cos(angle2) * 100, player.rect.centery - math.sin(angle2) * 100)
                #pygame.draw.polygon(screen, WHITE, [A, B, C], 5)
                for e in enemy_group:
                    if otherstuff.iscol(A, B, C, (e.rect.centerx, e.rect.centery)):
                        e.hp -= 20 * player.att
                self.cooldown_countercl = 25
        elif key[pygame.K_e]:
            if self.cooldown_countere <= 0:
                image = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("images/slash.png"), -180 - (rot * (180/math.pi))), (64, 64))
                new_wall = Wall(player.rect.centerx - 32, player.rect.centery - 32, -math.cos(rot) * 10,
                                -math.sin(rot) * 10, image, 20)
                entity_group.add(new_wall)
                self.cooldown_countere = 30 * 5
        elif key[pygame.K_q]:
            if self.cooldown_counterq <= 0:
                player.speed *= 2
                self.cooldown_counterq = 30 * 15
        elif key[pygame.K_r]:
            if self.cooldown_counterr <= 0:
                player.speed *= 1.2
                self.cooldown_counterr = 30 * 25


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, values):
        super().__init__()
        self.rect = pygame.Rect((x, y), (16, 16))
        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)
        self.attcooldowncounter = 0
        self.hp = values[0]
        self.speed = values[1]
        self.attcooldown = values[2]

    def update(self, player, entity_group):
        rot = math.atan2(self.rect.centery - player.rect.centery, self.rect.centerx - player.rect.centerx)
        self.rect.centerx -= math.cos(rot) * self.speed
        self.rect.centery -= math.sin(rot) * self.speed
        col = pygame.sprite.spritecollide(self, entity_group, False)
        for e in col:
            self.hp -= e.dmg * player.att
            if e.diewhenhit:
                e.kill()
        if self.hp <= 0:
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, starttype):
        super().__init__()
        self.type = starttype
        self.rect = pygame.Rect((width/2, height/2), (32, 32))
        self.image = pygame.Surface((32, 32))
        self.image.fill(WHITE)
        self.speed = 2
        self.health = self.type.health
        self.dead = False
        self.att = 1
        self.invic = False

    def update(self, enemy_group, entity_group):
        key = pygame.key.get_pressed()
        self.type.update(self, enemy_group, entity_group)
        if key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        elif key[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif key[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed

        col = pygame.sprite.spritecollide(self, enemy_group, True)
        for e in col:
            if not self.invic:
                self.health -= 1

        if self.health <= 0:
            self.dead = True


def main():
    part = "intro"

    enemy_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()

    melee_enemy = [50, 2, 7]
    tank_enemy = [100, 1, 10]
    speed_enemy = [20, 5, 5]

    font = pygame.font.Font("fonts/fourside.ttf", 75)
    title = font.render("-- Game Title --", 1, WHITE)
    titlepos = title.get_rect()
    titlepos.centerx = width / 2
    titlepos.centery = height / 4
    font2 = pygame.font.Font("fonts/fourside.ttf", 35)
    click = font2.render("-- Click here to Play --", 1, WHITE)
    clickpos = click.get_rect()
    clickpos.centerx = width / 2
    clickpos.centery = height / 2
    title1 = font.render("-- Game Over --", 1, WHITE)
    titlepos1 = title.get_rect()
    titlepos1.centerx = width / 2
    titlepos1.centery = height / 4
    click1 = font2.render("-- Play Again --", 1, WHITE)
    clickpos1 = click.get_rect()
    clickpos1.centerx = width / 2 + 100
    clickpos1.centery = height / 2
    pause = font.render("-- Paused --", 1, WHITE)
    pausepos = pause.get_rect()
    pausepos.centerx = width / 2
    pausepos.centery = height / 4

    sword_Button = Button(width/4, height/2, 128, 64, pygame.transform.scale(pygame.image.load("images/sword_button.png"), (128, 64)), pygame.transform.scale(pygame.image.load("images/sword_button_pressed.png"), (128, 64)))
    tank_Button = Button(width / 2, height / 2, 128, 64, pygame.transform.scale(pygame.image.load("images/tank_button.png"), (128, 64)), pygame.transform.scale(pygame.image.load("images/tank_button_pressed.png"), (128, 64)))
    wizard_Button = Button(width - width / 4, height / 2, 128, 64, pygame.transform.scale(pygame.image.load("images/wizard_button.png"), (128, 64)), pygame.transform.scale(pygame.image.load("images/wizard_button_pressed.png"), (128, 64)))

    i = 0

    while True:
        screen.fill(BLACK)
        if part == "intro":
            screen.blit(title, titlepos)
            if i > 10:
                if i > 20:
                    i = 0
                screen.blit(click, clickpos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    i = 0
                    part = "classchoose"
            i += 1
        elif part == "classchoose":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if sword_Button.update():
                player = Player(Swordsman())
                part = "play"
            if tank_Button.update():
                player = Player(Tank())
                part = "play"
            if wizard_Button.update():
                player = Player(Wizard())
                part = "play"

            screen.blit(sword_Button.image, sword_Button.rect)
            screen.blit(tank_Button.image, tank_Button.rect)
            screen.blit(wizard_Button.image, wizard_Button.rect)
        elif part == "play":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        part = "menu"
            for i in range(player.health):
                rect = pygame.Rect(10 + i * 30, 10, 20, 20)
                h_img = pygame.Surface((16, 16))
                h_img.fill(RED)
                screen.blit(h_img, rect)
            font3 = pygame.font.Font("fonts/fourside.ttf", 25)
            clickcool = font3.render(str(round(max(min(1, player.type.cooldown_countercl/10), 0) * 100)), 1, WHITE)
            clickcoolpos = clickcool.get_rect()
            clickcoolpos.centerx = 50
            clickcoolpos.centery = 70
            clicke = font3.render(str(round(max(min(1, player.type.cooldown_countere / (30 * 5)), 0) * 100)), 1, WHITE)
            clickepos = clicke.get_rect()
            clickepos.centerx = 50
            clickepos.centery = 100
            clickq = font3.render(str(round(max(min(1, player.type.cooldown_counterq / (30 * 15)), 0) * 100)), 1, WHITE)
            clickqpos = clickq.get_rect()
            clickqpos.centerx = 50
            clickqpos.centery = 130
            clickr = font3.render(str(round(max(min(1, player.type.cooldown_counterr / (30 * 25)), 0) * 100)), 1, WHITE)
            clickrpos = clickr.get_rect()
            clickrpos.centerx = 50
            clickrpos.centery = 160
            screen.blit(clickcool, clickcoolpos)
            screen.blit(clicke, clickepos)
            screen.blit(clickq, clickqpos)
            screen.blit(clickr, clickrpos)
            if random.randint(1, 100) == 1:
                howmany = random.randint(0, 5)
                for i in range(howmany):
                    whichone = random.randint(1, 3)
                    num2 = random.randint(1, 4)
                    new_enemy = None
                    if num2 == 1:
                        if whichone == 1:
                            new_enemy = Enemy(-100, random.randint(0, height), melee_enemy)
                        elif whichone == 2:
                            new_enemy = Enemy(-100, random.randint(0, height), tank_enemy)
                        elif whichone == 3:
                            new_enemy = Enemy(-100, random.randint(0, height), speed_enemy)
                    elif num2 == 2:
                        if whichone == 1:
                            new_enemy = Enemy(width + 100, random.randint(0, height), melee_enemy)
                        elif whichone == 2:
                            new_enemy = Enemy(width + 100, random.randint(0, height), tank_enemy)
                        elif whichone == 3:
                            new_enemy = Enemy(width + 100, random.randint(0, height), speed_enemy)
                    elif num2 == 3:
                        if whichone == 1:
                            new_enemy = Enemy(random.randint(0, width), -100, melee_enemy)
                        elif whichone == 2:
                            new_enemy = Enemy(random.randint(0, width), -100, tank_enemy)
                        elif whichone == 3:
                            new_enemy = Enemy(random.randint(0, width), -100, speed_enemy)
                    elif num2 == 4:
                        if whichone == 1:
                            new_enemy = Enemy(random.randint(0, width), height + 100, melee_enemy)
                        elif whichone == 2:
                            new_enemy = Enemy(random.randint(0, width), height + 100, tank_enemy)
                        elif whichone == 3:
                            new_enemy = Enemy(random.randint(0, width), height + 100, speed_enemy)
                    enemy_group.add(new_enemy)

            player.update(enemy_group, entity_group)
            enemy_group.update(player, entity_group)
            entity_group.update()

            screen.blit(player.image, player.rect)
            enemy_group.draw(screen)
            entity_group.draw(screen)

            if player.dead:
                part = "outro"

        elif part == "menu":
            screen.blit(pause, pausepos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        part = "play"

        elif part == "outro":
            screen.blit(title1, titlepos1)
            if i > 10:
                if i > 20:
                    i = 0
                screen.blit(click1, clickpos1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    part = "intro"
                    for e in enemy_group:
                        e.kill()
            i += 1
        pygame.display.flip()
        clock.tick(60)

main()
