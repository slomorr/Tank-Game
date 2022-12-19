import pygame
from random import randint
from config import *

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tank Game")
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
Arial_50 = pygame.font.SysFont('arial', 50)

save = open('save.txt')

levelsPass = save.readline()


pygame.mixer.music.load('sound/menu(Undertale).mp3')
pygame.mixer.music.play(-1)



shoot = pygame.mixer.Sound('sound/shoot.ogg')
death1 = pygame.mixer.Sound('sound/death/death.ogg')
death2 = pygame.mixer.Sound('sound/death/acolytewhat1.ogg')
death3 = pygame.mixer.Sound('sound/death/arthasyes4.ogg')
death4 = pygame.mixer.Sound('sound/death/arthasyesattack1.ogg')
death5 = pygame.mixer.Sound('sound/death/banditdeath1.ogg')
death6 = pygame.mixer.Sound('sound/death/buildingplacement.ogg')
death7 = pygame.mixer.Sound('sound/death/druidoftheclawdeath1.ogg')
death8 = pygame.mixer.Sound('sound/death/frazy-yunitov-iz-warcraft-3.ogg')
death9 = pygame.mixer.Sound('sound/death/goldminedeath1.ogg')
death10 = pygame.mixer.Sound('sound/death/gruntherodies1.ogg')
death11 = pygame.mixer.Sound('sound/death/peasantdeath.ogg')
death12 = pygame.mixer.Sound('sound/death/peasantwhat3.ogg')
win = pygame.mixer.Sound('sound/win.ogg')
death = [death1, death2, death3, death4, death5, death6, death7, death8, death9, death10, death11, death12]
sounds = [win, shoot]
for dead in death:
    sounds.append(dead)
musicVolume = float(save.readline())
soundVolume = float(save.readline())
pygame.mixer.music.set_volume(musicVolume)
for sound in sounds:
    sound.set_volume(soundVolume)



imgBrick1 = pygame.image.load('image/pixil-frame-0.png')
imgBrick2 = pygame.image.load('image/pixil-frame-1.png')
imgTank = pygame.image.load('image/tank.png')
imgBoom = [pygame.image.load('image/boom1.png'),
           pygame.image.load('image/boom2.png'),
           pygame.image.load('image/boom3.png')]
imgHeart = pygame.image.load('image/heart.png')

scenes = []


def print_message(message, x, y, font_color=(255, 255, 255), font_type='arial', font_size=30):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    window.blit(text, (x, y))


class Scene:
    def __init__(self, map):
        scenes.append(self)
        self.map = map
        self.sceneType = 'Scene'
        self.game = 'pause'
        self.type = 'pause'
        self.value = 0
        self.haveEnemy = 0
        self.LevelPass = int(levelsPass[len(scenes)-1])
        self.deathSound = death[randint(0, len(death))-1]

    def generate(self):
        if self.value < 1:
            self.value += 1
            if self.type == 'play':
                for i, row in enumerate(self.map):
                    for j, column in enumerate(row):
                        if column == "B":
                            Block(j * 32, (i + 1) * 32, TILE)
                        if column == "T":
                            Tank(j * 32, (i + 1) * 32, randint(0, 4))
                        if column == "E":
                            Enemy(j * 32, (i + 1) * 32, randint(0, 4))
                            self.haveEnemy += 1

    def work(self):

        if self.game == 'play':
            for obj in objects:
                obj.update()
                if obj.type == 'tank':
                    if obj.health <= 0:
                        self.death()
                    if obj.score == self.haveEnemy and obj.health > 0:
                        self.win()

            for bullet in bullets: bullet.update()

        window.fill('black')

        if self.game == 'pause':
            print_message('Press "Enter" for start/pause',200, 300)
            print_message('or "R" for restart', 250, 350)

        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()
        ui.draw()
        if keys[pygame.K_r]:
            self.reset()
        if keys[pygame.K_ESCAPE]:
            self.death()




    def death(self):
        self.game = 'pause'
        self.type = 'pause'
        for obj in objects:
            if obj.type == 'tank' and obj.health <= 0:
                self.deathSound.play()
        objects.clear()
        bullets.clear()
        self.value = 0
        self.haveEnemy = 0


    def win(self):
        self.game = 'pause'
        self.type = 'pause'
        objects.clear()
        bullets.clear()
        self.value = 0
        self.haveEnemy = 0
        self.LevelPass = 1
        win.play()

    def reset(self):
        objects.clear()
        bullets.clear()
        self.value = 0
        self.haveEnemy = 0
        self.generate()

class Sandbox:
    def __init__(self):
        scenes.append(self)
        self.sceneType = 'sandbox'
        self.game = 'pause'
        self.type = 'pause'
        self.value = 0
        self.haveEnemy = 0
        self.LevelPass = 0
        self.timer = 0
        self.deathSound = death[randint(0, len(death)-1)]

    def generate(self):
        for _ in range(randint(10, 260)):
            while True:
                x = randint(0, WIDTH // TILE - 1) * TILE
                y = randint(1, HEIGHT // TILE - 1) * TILE
                rect = pygame.Rect(x, y, TILE, TILE)
                fined = False
                for obj in objects:
                    if rect.colliderect(obj.rect):
                        fined = True
                if not fined:
                    break
            Block(x, y, TILE)

        for _ in range(randint(1, 2)):
            while True:
                x = randint(0, WIDTH // TILE - 1) * TILE
                y = randint(1, HEIGHT // TILE - 1) * TILE
                rect = pygame.Rect(x, y, TILE, TILE)
                fined = False
                for obj in objects:
                    if rect.colliderect(obj.rect):
                        fined = True
                if not fined:
                    break
            Enemy(x, y, randint(0, 3))
            self.haveEnemy += 1
        while True:
            x = randint(0, WIDTH // TILE - 1) * TILE
            y = randint(1, HEIGHT // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    fined = True
            if not fined:
                break
        Tank(x, y, randint(0, 3))

    def work(self):

        self.timer += 1
        if self.game == 'play':
            for obj in objects:
                obj.update()
                if obj.type == 'tank':
                    if obj.health <= 0:
                        self.death()
                    if obj.score == self.haveEnemy and obj.health > 0:
                        for _ in range(randint(0, 3)):
                            while True:
                                x = randint(0, WIDTH // TILE - 1) * TILE
                                y = randint(1, HEIGHT // TILE - 1) * TILE
                                rect = pygame.Rect(x, y, TILE, TILE)
                                fined = False
                                for obj in objects:
                                    if obj.type == 'tank' or obj.type == 'block' or  obj.type == 'enemy':
                                        if rect.colliderect(obj.rect):
                                            fined = True
                                if not fined:
                                    break
                            Enemy(x, y, randint(0, 4))
                            for obj in objects:
                                if obj.type == 'tank':
                                    obj.health += 1
                            self.haveEnemy += 1

            for bullet in bullets: bullet.update()

        window.fill('black')

        for bullet in bullets: bullet.draw()
        for obj in objects: obj.draw()
        ui.draw()
        if keys[pygame.K_r]:
            self.reset()
        if keys[pygame.K_ESCAPE]:
            self.death()

        if self.timer == 1800:
            for _ in range(randint(0, 10)):
                while True:
                    x = randint(0, WIDTH // TILE - 1) * TILE
                    y = randint(1, HEIGHT // TILE - 1) * TILE
                    rect = pygame.Rect(x, y, TILE, TILE)
                    fined = False
                    for obj in objects:
                        if obj.type == 'tank' or obj.type == 'block' or obj.type == 'enemy':
                            if rect.colliderect(obj.rect):
                                fined = True
                    if not fined:
                        break
                Block(x, y, TILE)
            self.timer = 0


    def death(self):
        self.game = 'pause'
        self.type = 'pause'
        for obj in objects:
            if obj.type == 'tank' and obj.health <= 0:
                self.deathSound.play()
        objects.clear()
        bullets.clear()
        self.value = 0
        self.haveEnemy = 0

    def reset(self):
        objects.clear()
        bullets.clear()
        self.value = 0
        self.haveEnemy = 0
        self.generate()



class Button:
    def __init__(self, width, height, x, y, message, actionType=None, actionValue=None):
        self.width = width
        self.height = height
        self.inactive_color = (181, 0, 1)
        self.active_color = (212, 0, 1)
        self.x = x
        self.y = y
        self.message = message
        self.actionType = actionType
        self.actionValue = actionValue


    def draw(self):
        global musicVolume
        global soundVolume
        global play
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.actionType == 'scene':
            if scenes[self.actionValue].LevelPass == 1:
                self.inactive_color = (0, 150, 1)
                self.active_color = (0, 217, 1)
            else:
                self.inactive_color = (181, 0, 1)
                self.active_color = (212, 0, 1)


        if self.x < mouse[0] < self.x + self.width and self.y < mouse[1] < self.y + self.height:
            pygame.draw.rect(window, self.inactive_color, (self.x, self.y, self.width, self.height))

            if click[0] == 1:
                pygame.time.wait(300)
                if self.actionType == 'scene':
                    self.startLevel(self.actionValue)
                elif self.actionType == 'switch':
                    menu.page = self.actionValue
                elif self.actionType == 'sandbox':
                    for scene in scenes:
                        if scene.sceneType == 'sandbox':
                            scene.type = 'play'
                            scene.generate()
                elif self.actionType == 'music':
                    musicVolume += self.actionValue
                    pygame.mixer.music.set_volume(musicVolume)
                elif self.actionType == 'sound':
                    soundVolume += self.actionValue
                    for sound in sounds:
                        sound.set_volume(soundVolume)
                elif self.actionType == 'reset':
                    for scene in scenes:
                        if scene.sceneType == 'Scene':
                            scene.LevelPass = 0
                elif self.actionType == 'quit':
                    play = False

        else:
            pygame.draw.rect(window, self.active_color, (self.x, self.y, self.width, self.height))
        print_message(self.message, self.x + 10, self.y + 10)

    def startLevel(self, levelNom):
        scenes[levelNom].type = 'play'
        scenes[levelNom].generate()


class Menu:

    def __init__(self):
        self.background = pygame.image.load('image/background.jpg')
        self.level_button = Button(135, 55, 336, 100, '  Levels', 'switch', 1)
        self.sandbox = Button(135, 55, 336, 200, 'Sandbox', 'sandbox')
        self.level1 = Button(110, 55, 336, 150, 'Level 1', 'scene', 0)
        self.level2 = Button(110, 55, 336, 250, 'Level 2', 'scene', 1)
        self.level3 = Button(110, 55, 336, 350, 'Level 3', 'scene', 2)
        self.levelback = Button(110, 55, 336, 450, ' Back', 'switch', 0)
        self.option = Button(135, 55, 336, 300, '  Option', 'switch', 2)
        self.musicDown = Button(55, 55, 300, 100, None, 'music', -0.1)
        self.musicUp = Button(55, 55, 450, 100, None, 'music', 0.1)
        self.soundDown = Button(55, 55, 300, 200, None, 'sound', -0.1)
        self.soundUp = Button(55, 55, 450, 200, None, 'sound', 0.1)
        self.quit = Button(135, 55, 336, 400, '   Quit', 'quit')
        self.reset = Button(135, 55, 325, 350, '  Reset', 'reset')

        self.page = 0

    def draw(self):
        window.blit(self.background, (0, 0))
        if self.page == 0:
            self.level_button.draw()
            self.sandbox.draw()
            self.option.draw()
            self.quit.draw()
        if self.page == 1:
            self.level1.draw()
            self.level2.draw()
            self.level3.draw()
            self.levelback.draw()
        if self.page == 2:
            self.musicDown.draw()
            self.musicUp.draw()
            self.levelback.draw()
            self.soundUp.draw()
            self.soundDown.draw()
            self.reset.draw()
            print_message('-   Music    +', 325, 110)
            print_message('-   Sound   +', 325, 210)
        if keys[pygame.K_ESCAPE]:
            self.page = 0


class UI:
    def __init__(self):
        self.imageHeart = imgHeart
        self.poz = (1, 1, 1, 1)

    def draw(self):
        for obj in objects:
            if obj.type == 'tank':
                window.blit(self.imageHeart, self.poz)

                text = fontUI.render(str(obj.health), True, 'white')
                rect = text.get_rect(center=(5 + 32, 5 + 17))
                window.blit(text, rect)

                stext = fontUI.render('score: ', True, 'white')
                srect = text.get_rect(center=(35 + 32, 5 + 17))
                window.blit(stext, srect)
                score = fontUI.render(str(obj.score), True, 'white')
                scoreRect = stext.get_rect(center=(160, 22))
                window.blit(score, scoreRect)


class Tank:
    def __init__(self, px, py, direct):
        objects.append(self)
        self.type = 'tank'
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.health = 5
        self.score = 0

        self.keyList = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SPACE]

        self.shotTimer = 0
        self.shotReload = 90
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = self.keyList[0]
        self.keyRIGHT = self.keyList[1]
        self.keyUP = self.keyList[2]
        self.keyDOWN = self.keyList[3]
        self.keySHOT = self.keyList[4]

        self.image = pygame.transform.rotate(imgTank, -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTank, -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
        elif keys[self.keySHOT] and self.shotTimer == 0:
            shoot.play()
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotReload

        for obj in objects:
            if obj != self and (obj.type == 'block' or obj.type == 'enemy') and self.rect.colliderect(obj):
                self.rect.topleft = oldX, oldY
        if self.rect.x < 0 or self.rect.x > WIDTH - 23 or self.rect.y < 0 or self.rect.y > HEIGHT - 23:
            self.rect.topleft = oldX, oldY

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def damage(self, value):
        self.health -= value

    def draw(self):
        window.blit(self.image, self.rect)


class Enemy:
    def __init__(self, px, py, direct):

        self.oldPositionY = 0
        self.oldPositionX = 0
        self.oldPosTime = 60

        objects.append(self)
        self.type = 'enemy'
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 16
        self.moveSetTime = 60
        self.health = 5

        self.shotTimer = 0
        self.shotReload = 90
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.image = pygame.transform.rotate(imgTank, -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTank, -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (TILE - 3, TILE - 3))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft

        for obj in objects:
            if obj.type == 'tank':
                playerPos = [obj.rect.x, obj.rect.y]
        if self.oldPosTime == 60:
            self.oldPositionX = self.rect.x
            self.oldPositionY = self.rect.y
        if (playerPos[1] < self.rect.y) and (
                (self.rect.y - playerPos[1] >= 14) or (playerPos[1] - self.rect.y >= 14)) and self.moveSetTime == 0:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            self.moveSetTime = 60
        if playerPos[1] > self.rect.y and (
                (self.rect.y - playerPos[1] >= 14) or (playerPos[1] - self.rect.y >= 14)) and self.moveSetTime == 0:
            self.rect.y += self.moveSpeed
            self.direct = 2
            self.moveSetTime = 60

        if playerPos[0] < self.rect.x and (
                (self.rect.x - playerPos[0] >= 14) or (playerPos[0] - self.rect.x >= 14)) and self.moveSetTime == 0:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            self.moveSetTime = 60

        if playerPos[0] > self.rect.x and (
                (self.rect.x - playerPos[0] >= 14) or (playerPos[0] - self.rect.x >= 14)) and self.moveSetTime == 0:
            self.rect.x += self.moveSpeed
            self.direct = 1
            self.moveSetTime = 60

        if ((14 >= self.rect.y - playerPos[1] >= -14) or (14 >= self.rect.x - playerPos[0] >= -14)) and (
                self.shotTimer == 0) or self.shotTimer == 0 and self.oldPosTime == 0 and (
                self.rect.x == self.oldPositionX and self.rect.y == self.oldPositionY):
            if 0 <= self.direct <= 3:
                shoot.play()
                dx = DIRECTS[self.direct][0] * self.bulletSpeed
                dy = DIRECTS[self.direct][1] * self.bulletSpeed
                Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
                self.shotTimer = self.shotReload

        if self.moveSetTime > 0:
            self.moveSetTime -= 2
        if self.oldPosTime > 0:
            self.oldPosTime -= 2
        elif self.oldPosTime == 0:
            self.oldPosTime = 60
        if self.shotTimer > 0:
            self.shotTimer -= 1

        for obj in objects:
            if obj != self and (
                    obj.type == 'block' or obj.type == 'tank' or obj.type == 'enemy') and self.rect.colliderect(obj):
                self.rect.topleft = oldX, oldY

    def damage(self, value):
        self.health -= value
        if self.health <= 0:
            death[randint(0, len(death))-1].play()
            objects.remove(self)
            for obj in objects:
                if obj.type == 'tank':
                    obj.score += 1

    def draw(self):
        window.blit(self.image, self.rect)


class Boom:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'boom'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.3
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBoom[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
        self.parent = parent

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'boom':
                    if obj.rect.collidepoint(self.px, self.py):
                        bullets.remove(self)
                        obj.damage(self.damage)
                        Boom(self.px, self.py)
                        break

    def draw(self):
        pygame.draw.circle(window, 'orange', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'
        self.rand = randint(0, 1)

        self.rect = pygame.Rect(px, py, size, size)
        self.health = 1

    def update(self):
        pass

    def damage(self, value):
        self.health -= value
        if self.health <= 0:
            objects.remove(self)

    def draw(self):
        if self.rand == 0:
            window.blit(imgBrick1, self.rect)
        else:
            window.blit(imgBrick2, self.rect)


objects = []
bullets = []

ui = UI()

play = True



Scene(Level1)
Scene(Level2)
Scene(Level3)
Sandbox()

menu = Menu()

game_played = False
count = 0

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if game_played == True:
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_RETURN] and played_scene.game == 'play':
                    played_scene.game = 'pause'
                elif pygame.key.get_pressed()[pygame.K_RETURN] and played_scene.game == 'pause':
                    played_scene.game = 'play'

    keys = pygame.key.get_pressed()

    if game_played is False:
        menu.draw()
        for scene in scenes:
            if scene.type == 'play':
                game_played = True
    else:
        count = 0
        for scene in scenes:
            if scene.type == 'play':
                played_scene = scene
                scene.work()
            else:
                count += 1
        if count == 4:
            game_played = False
            count = 0

    pygame.display.update()
    clock.tick(FPS)
save = open('save.txt', 'w')
levelsPassSave = str()
for scene in scenes:
    if scene.sceneType == 'Scene':
        levelsPassSave += str(scene.LevelPass)
save.write(str(levelsPassSave) + '\n')
if 0 < musicVolume < 1:
    save.writelines(str(musicVolume) + '\n')
else:
    save.writelines('0' + '\n')
if 0 < soundVolume < 1:
    save.write(str(soundVolume) + '\n')
else:
    save.write('0' + '\n')
pygame.quit()
