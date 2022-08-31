"""
    /* -----------------------------------------------
    /* Author : MONJA  - monja.sesame@gmail.com
    /* GitHub : github.com/monja119/danger_snake
    /* How to use Check the GitHub README
    /* v1.0.0
    /* ----------------------------------------------- */

"""

from random import *

from pygame.locals import *

from body import *
from game import Game, width, height

pygame.init()

clock = pygame.time.Clock()
text = pygame.font.SysFont('Georgia', 15)
msg = text.render('Game Over ! (Enter)', True, 'red')


class Run:
    def __init__(self):
        self.index = None
        self.player_rect = ''
        self.player_surface = ''
        self.player_new = ''
        self.apple_pos = (0, 0)
        self.snake_pos = (0, 0)
        self.apple_rect = ''
        self.apple_y = 0
        self.apple_x = 0
        self.running = True
        self.bg = Game()
        self.body = Body
        # snake
        self.snake_pos0 = (250, 200)
        self.apple_size = (10, 10)
        self.speed = 10
        self.moves = 0

        self.x, self.y = self.snake_pos0[0], self.snake_pos0[1]

        self.snake_body = [(self.x, self.y)]
        self.move()

        # apple
        self.apple()
        self.apple_color = 'red'
        self.apple_surface = pygame.Surface((10, 10))
        self.apple_surface.fill(self.apple_color)

        # running
        self.error= 0
        self.status = 'ready'
        self.step = 1
        self.catch = 0
        self.level = 1

        # sounds effect
        try:
            self.snack_sound = pygame.mixer.Sound('folder/sounds/snake.mp3')
            self.catching_sound = pygame.mixer.Sound('folder/sounds/catching/{}.wav'.format(randint(1, 5)))
        except FileNotFoundError:
            self.error_message = 'Sound Effects Not found !'
            self.error = 1
        except pygame.error:
            pass
        # music
        self.music = 0
        self.volume = 10

    def text(self, font, size, color, value, x, y):
        my_text = pygame.font.SysFont(font, size)
        text_render = my_text.render(value, True, color)
        self.bg.window.blit(text_render, (x, y))

    def load_body(self, x, y):
        self.bg.window.blit(self.body(x, y).surface, self.body(x, y).rect)

    def apple(self):
        self.apple_x = choice(range(0, 390, 10))
        while self.apple_x in self.snake_body:
            self.apple_x = choice(range(0, 390, 10))

        self.apple_y = choice(range(30, 390, 10))
        while self.apple_y in self.snake_body:
            self.apple_y = choice(range(30, 390, 10))

    def load_apple(self):
        self.apple_rect = pygame.Rect((self.apple_x, self.apple_y), self.apple_size)
        self.bg.window.blit(self.apple_surface, self.apple_rect)

    def move(self):
        self.body(self.x, self.y)

    def catching(self):
        self.snake_pos = (self.x, self.y)
        self.apple_pos = (self.apple_x, self.apple_y)
        if self.apple_pos == self.snake_pos:
            self.catch += 1
            self.level += 1
            if self.error != 1:
                self.catching_sound.play()
            self.snake_body.append(self.snake_pos)
            self.apple()
            self.load_apple()

    def game_over(self):

        if self.x >= width or self.x < 0 or self.y >= height or self.y < 0 or (self.x, self.y) in self.snake_body[
                                                                                   0:-1] and self.status != 'stop':
            if self.error != 1:
                pygame.mixer.music.stop()
                pygame.mixer.Sound('folder/sounds/game_over/1.wav').play()
            self.status = 'stop'
            app.text('Joker Man', 25, 'red', 'Game Over !', (width / 2) - 70, (height / 2) - 20)
            pygame.display.flip()

    def set_level(self, x):
        x = self.step + self.catch + 1
        self.level = x

    def initial(self):
        self.x, self.y = self.snake_pos0[0], self.snake_pos0[1]
        self.snake_body = [(self.x, self.y)]
        self.level = 3
        self.catch = 0
        self.status = 'running'
        self.moves = 0
        app.music += 1
        if self.error != 1:
            self.catching_sound = pygame.mixer.Sound('folder/sounds/catching/{}.wav'.format(randint(1, 5)))
        self.apple()
        self.load_apple()
        self.move()
        self.load_game()

    def change_music(self):
        self.index = randint(1, 5)
        try:
            pygame.mixer.music.load('folder/sounds/music/{}.mp3'.format(self.index))
            pygame.mixer.music.play()
        except FileNotFoundError:
            self.error_message = 'Sound Effects Not found !'
            self.error = 1
        except pygame.error:
            pass

    def set_volume(self, x):
        x = x / 10
        pygame.mixer.music.set_volume(x)

    def load_game(self):

        if running and self.status == 'running':
            self.bg.window.fill('black')
            # effect sonorous
            if self.moves % 50 == 0 and self.error != 1:
                self.snack_sound.play()

            # load Apple
            self.load_apple()

            # load snack
            for i in range(len(self.snake_body)):
                if i == len(self.snake_body) - 1:
                    head = self.body(self.snake_body[i][0], self.snake_body[i][1]).surface
                    head.fill('green')
                    self.bg.window.blit(head, self.body(self.snake_body[i][0], self.snake_body[i][1]).rect)
                else:
                    x = self.snake_body[i][0]
                    y = self.snake_body[i][1]
                    self.load_body(x, y)
            self.set_level(self.catch)

            self.text('Joker man', 15, 'white', str(self.catch), (width / 2) - 15, 10)
            self.text('monospace', 10, 'white', 'MONJA@2022', width - 7 - 60, height - 10)
            pygame.display.flip()


app = Run()
running = True
last_pos = (0, 0)
new_pos = (0, 0)
axe = 'coord'
once = 0

while running:
    # timing
    clock.tick(app.level)
    app.moves += 1

    # music
    if app.music % 2 == 0 and app.error != 1:
        app.change_music()
        app.music += 1
    else:
        pass

    # axis manager
    snake = app.snake_body

    # guiding

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # gestion de status
            if app.status == 'ready':
                app.status = 'running'
                app.music += 1
                if app.error != 1:
                    app.snack_sound.play()
                    pygame.mixer.music.set_volume(0.75)
            if app.status == 'stop':
                app.initial()

            # gestion de touches
            # MOVEMENTS
            if axe == 'abs':
                if event.key == K_DOWN:
                    app.speed = abs(app.speed)
                    axe = 'coord'
                if event.key == K_UP:
                    app.speed = -abs(app.speed)
                    axe = 'coord'
            else:
                if event.key == K_RIGHT:
                    app.speed = abs(app.speed)
                    axe = 'abs'
                if event.key == K_LEFT:
                    app.speed = -abs(app.speed)
                    axe = 'abs'

            if event.key == K_SPACE:
                if app.status == 'pause':
                    app.status = 'running'
                    if app.error != 1:
                        pygame.mixer.unpause()
                else:
                    app.status = 'pause'
                    if app.error != 1:
                        pygame.mixer.pause()
            if event.key == K_F1 and app.error != 1:
                if app.volume == 0:
                    app.set_volume(0)
                else:
                    app.volume -= 1
                    app.set_volume(app.volume)
            if event.key == K_F2 and app.error != 1:
                if app.volume == 10:
                    pass
                else:
                    app.volume += 1
                    app.set_volume(app.volume)
            if event.key == K_ESCAPE:
                running = False
                app.text('Times New Romain', 25, 'white', 'Thank you', (width / 2) - 40, (height / 2) - 100)
                pygame.display.flip()
                pygame.time.wait(2000)
                pygame.quit()

    # Homepage
    if app.status == 'ready':

        app.bg.window.fill('black')
        first = pygame.Surface((10, 10))
        first.fill('green')
        app.bg.window.blit(first, pygame.Rect((width / 2 - 27, height / 2 - 10), (10, 10)))

        # instructions
        app.text('Joker man', 55, 'green', 'Danger Snake', 50, 50)
        app.text('Joker man', 25, 'red', 'Ready ?', (width / 2) - 60, (height / 2))
        app.text('monospace', 13, 'white', '(Press Any Key)', (width / 2) - 70, (height / 2) + 50)
        app.text('Times New Roman', 13, 'white', 'Movement : key up, down, right and right', 10, (height / 2) + 100)
        app.text('Times New Roman', 13, 'white', 'Pause : Space', 10, (height / 2) + 115)
        app.text('Times New Roman', 13, 'white', 'Quit : Escape', 10, (height / 2) + 130)
        # error
        if app.error == 1:
            app.text('Times New Roman', 13, 'red', str(app.error_message), width/2- 70, 15)
            if once != 1:
                print("La musique n'est pas prête, Veuillez l'avoir sur github")
            once = 1

        # contact
        app.text('Times New Roman', 13, 'white', 'monja.sesame@gmail.com', 10, height - 20)
        app.text('Times New Roman', 13, 'white', 'https://github.com/monja119', 190, height - 20)
        app.text('Times New Roman', 13, 'white', '+261 34 08 612 63', 390, height - 20)
        pygame.display.flip()
    elif app.status == 'pause' or app.status == 'stop':
        pass
    else:
        # multiplying
        if axe == 'abs':
            app.x += app.speed
        else:
            app.y += app.speed
        app.catching()
        app.game_over()
        if app.status != 0:
            m = len(snake)
            last_pos = snake[m-1]
            for k in range(len(app.snake_body) - 1):
                app.snake_body[k] = app.snake_body[k + 1]
            app.snake_body[len(app.snake_body) - 1] = (app.x, app.y)
            new_pos = (app.x, app.y)
            app.load_game()


