# -*- encoding: utf-8 -*-

import pygame
import sys

pygame.init()

WIDTH = 1920
HEIGHT = 1080
cof = HEIGHT / 408

FPS = 60
CLOCK = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Errant')

FONT = pygame.font.Font('source/thintel.ttf', 36)
BIGFONT = pygame.font.Font('source/thintel.ttf', 72)

main_menu_bg = pygame.image.load('source/main_menu_bg.png')
main_menu_bg = pygame.transform.scale(main_menu_bg, (int(729 * cof), HEIGHT))
main_menu_bg_rect = main_menu_bg.get_rect()

BG_pic = pygame.image.load('source/main_bg.png')
BG_pic = pygame.transform.scale(BG_pic, (int(6648 * cof), HEIGHT))
hero_pic = pygame.image.load('source/sprites/gg_standing/gg_stand_1.png')
hero_pic = pygame.transform.scale(hero_pic, (int(70 * cof), int(70 * cof)))
first_npc_pic = pygame.image.load('source/sprites/npc1_sprite.png')
first_npc_pic = pygame.transform.scale(first_npc_pic, (int(61 * cof), int(78 * cof)))
second_npc_pic = pygame.image.load('source/sprites/npc2_sprite.png')
second_npc_pic = pygame.transform.scale(second_npc_pic, (int(70 * cof), int(80 * cof)))

all_sprites = pygame.sprite.Group()

first_dialogue = open('source/dialogues/first_dialogue.txt', 'r', encoding='utf-8').read()
second_dialogue = open('source/dialogues/second_dialogue.txt', 'r', encoding='utf-8').read()


class Hero(pygame.sprite.Sprite):
    """hero's class with stats and update"""

    def __init__(self, event):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_pic
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.direction = 1
        self.faith = 0
        self.event = event # doesn't work (why?)

    def update(self):
        # works only without game function cause of vision places (can't find local event)
        for event in self.event:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and self.direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = -1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = 1

        self.rect.x = 500
        self.rect.y = 752


class NPC(pygame.sprite.Sprite):
    """NPC class without dialogues"""

    def __init__(self, npc_picture, phrases):
        pygame.sprite.Sprite.__init__(self)
        self.image = npc_picture
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.phrases = phrases.split('\n')
        self.rect.x = 1920
        self.rect.y = 729

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_e] and 500 < self.rect.x <= 1250:
            dialogue = DialogueFrame(self.phrases, len(self.phrases))
            all_sprites.add(dialogue)
        if key_state[pygame.K_d]:
            self.rect.x -= 10
        if key_state[pygame.K_a]:
            self.rect.x += 10


class DialogueFrame(pygame.sprite.Sprite):
    """class for dialogue frame"""

    def __init__(self, dialogue, num_of_phrases):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((900, 100))
        self.image.fill((60, 60, 60))

        self.rect = self.image.get_rect()
        self.phrases = dialogue
        self.now_phrase = 0
        self.num_of_phrases = num_of_phrases
        self.rect.x = 520
        self.rect.y = 200

    def update(self):
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_SPACE] and self.now_phrase < len(self.phrases):
            if self.phrases[self.now_phrase][0] == '*':
                # здесь обрабатывается выбор ответа
                if key_state[pygame.K_e] and 500 < self.rect.x <= 1250:
                    pass
            self.image.fill((60, 60, 60))
            text = FONT.render(self.phrases[self.now_phrase], True, (200, 200, 200), (60, 60, 60))
            text_rect = text.get_rect()
            self.image.blit(text, (text_rect.x + 10, text_rect.y + 10))
            self.now_phrase += 1

        if self.now_phrase == self.num_of_phrases:
            self.kill()


class Background(pygame.sprite.Sprite):
    """background class (moves the person)"""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BG_pic
        self.rect = self.image.get_rect()
        self.speed_x = 0
        self.where = 0

    def update(self):
        self.speed_x = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.speed_x = 10
            self.where -= 1
        if key_state[pygame.K_d]:
            self.speed_x = -10
            self.where += 1
        if self.rect.x + self.speed_x < 0:
            self.rect.x += self.speed_x

        # first npc appears
        if self.where == 350:
            first_npc = NPC(first_npc_pic, first_dialogue)
            all_sprites.add(first_npc)

        # second npc appears
        if self.where == 650:
            second_npc = NPC(second_npc_pic, second_dialogue)
            all_sprites.add(second_npc)


class Button:

    def __init__(self, text, color, y, func, parameters = None):
        self.image = BIGFONT.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (1550, 550+y)
        self.func = func
        self.parameters = parameters

    # ПЕРЕДЕЛАТЬ ФУНКЦИЮ ИЗ СТАКОВЕРФЛОУ !!!!!
    def update(self):
        SCREEN.blit(self.image, self.rect)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.func(self.parameters)


# НЕ РАБОТАЕТ ЗАПУСК ПО КНОПКЕ !!!!!
def game(running=False):

    hero = Hero(pygame.event.get())
    bg = Background()
    all_sprites.add(bg, hero)

    while running:

        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        all_sprites.draw(SCREEN)

        pygame.display.flip()


def menu():

    start = Button("Start", (200, 200, 200), -10, game(True), True)
    end = Button("Exit", (200, 200, 200), 110, sys.exit)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(main_menu_bg, main_menu_bg_rect)
        start.update()
        end.update()

        pygame.display.flip()
        CLOCK.tick(FPS)


menu()
