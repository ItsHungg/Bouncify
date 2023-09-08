import threading
import pygame
import random
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

WIDTH = 500
HEIGHT = 700

GAME_WIDTH = 500
GAME_HEIGHT = 600
BACKGROUND_COLOR = '#edebf2'
BACKGROUND_IMAGE = pygame.image.load('assets\\textures\\background.png')

SCORE = 0
LEVEL = 0
HEALTH = 100

__project__ = 'Bouncify'
__version__ = '1.0.0'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f' {__project__} {__version__}')

pygame.display.set_icon(pygame.image.load('assets\\icon\\icon.png'))
pygame.mouse.set_cursor(pygame.cursors.arrow)
clock = pygame.time.Clock()
running = True


class Utilities:
    def __init__(self):
        pass

    @staticmethod
    class Write:
        def __init__(self, surface: pygame.display.set_mode, text: str, coordinates: tuple | list,
                     color: str | tuple = 'black',
                     font: str = pygame.font.get_default_font(), font_type='normal', size: int = 30,
                     anchor: str = 'normal'):
            self.surface = surface
            self.text = text
            self.coordinates = coordinates
            self.color = color
            self.font = font
            self.size = size
            self.anchor = anchor
            self.font_type = font_type

            self.text_object, self.text_rect = None, None

        def write(self):
            if self.font_type != 'system':
                text_object = pygame.font.Font(self.font, self.size).render(self.text, True, self.color)
            else:
                text_object = pygame.font.SysFont(self.font, self.size).render(self.text, True, self.color)

            text_rect = text_object.get_rect()
            if self.anchor in ['normal']:
                text_rect.x, text_rect.y = self.coordinates
            elif self.anchor in ['center']:
                text_rect.center = self.coordinates

            self.surface.blit(text_object, text_rect)
            self.text_object, self.text_rect = text_object, text_rect
            return text_object, text_rect

        def get(self):
            return self.text_object, self.text_rect

    class Widget:
        class Progressbar:
            def __init__(self, self_surface, outer_color: tuple | str, inner_color: tuple | str, position: tuple | list,
                         width: int, height: int, progress: int = 0, border_size: int = 3, border_radius: int = 0,
                         **kwargs):
                self.surface = self_surface
                self.outer_color = outer_color
                self.inner_color = inner_color
                self.x, self.y = position
                self.width = width
                self.height = height
                self.progress = progress
                self.border_size = border_size
                self.border_radius = border_radius

                self.other = kwargs

                self.outer_object, self.inner_object = self.get()

            def display(self):
                Utilities.Write(**self.other).write() if self.other else None
                self.outer_object, self.inner_object = self.get()

            def get(self):
                if self.progress <= 0:
                    self.progress = 0
                elif self.progress >= self.width:
                    self.progress = self.width
                return pygame.draw.rect(self.surface, self.outer_color,
                                        pygame.Rect(self.x, self.y, self.width + self.border_size,
                                                    self.height + self.border_size),
                                        border_radius=self.border_radius), pygame.draw.rect(self.surface,
                                                                                            self.inner_color,
                                                                                            pygame.Rect(
                                                                                                self.x,
                                                                                                self.y,
                                                                                                self.progress,
                                                                                                self.height),
                                                                                            border_radius=self.border_radius)

        class Button:
            def __init__(self, self_surface, outer_color: tuple | str, inner_color: tuple | str, position: tuple | list,
                         width: int, height: int, border_size: int = 3, border_radius: int = 0,
                         texts=None):
                if texts is None:
                    texts = []

                self.surface = self_surface
                self.outer_color = outer_color
                self.inner_color = inner_color
                self.x, self.y = position
                self.width = width
                self.height = height
                self.border_size = border_size
                self.border_radius = border_radius
                self.text_list = texts

                self.outer_object, self.inner_object = self.get()

            def display(self):
                self.outer_object, self.inner_object = self.get()
                for text in self.text_list:
                    text.write()

            def get(self):
                return pygame.draw.rect(self.surface, self.outer_color,
                                        pygame.Rect(self.x, self.y, self.width + self.border_size * 2,
                                                    self.height + self.border_size * 2),
                                        border_radius=self.border_radius), pygame.draw.rect(self.surface,
                                                                                            self.inner_color,
                                                                                            pygame.Rect(
                                                                                                self.x + self.border_size,
                                                                                                self.y + self.border_size,
                                                                                                self.width,
                                                                                                self.height),
                                                                                            border_radius=self.border_radius)

    @staticmethod
    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    class Storage:
        class Mechanics:
            @staticmethod
            def jump(sound: bool = True):
                if energy_bar.progress >= Utilities.Storage.Game.Increasement.JUMP_ENERGY:
                    if sound:
                        pygame.mixer.Sound('assets\\sounds\\jumping.mp3').play()
                    energy_bar.progress -= Utilities.Storage.Game.Increasement.JUMP_ENERGY if HEALTH > 0 else 0
                    player.velocity_y -= Utilities.Storage.Game.Increasement.JUMP_VELOCITY if energy_bar.progress >= 50 else Utilities.Storage.Game.Increasement.JUMP_VELOCITY - 2.5 if 25 < energy_bar.progress < 50 else Utilities.Storage.Game.Increasement.JUMP_VELOCITY - 5

            @staticmethod
            def upgrade_sound(path: str = 'assets\\sounds\\upgrade.mp3', is_random: bool = True):
                if is_random:
                    path = random.choices([path, 'assets\\sounds\\upgrade2.mp3'], weights=[1000, 1])[0]
                pygame.mixer.Sound(path).play()

            @staticmethod
            def play_music(path: str = 'assets\\sounds\\background.mp3', loop: int = 0, fade: int = 0):
                pygame.mixer.music.unload()
                pygame.mixer.music.load(path)
                if fade > 0:
                    pygame.mixer.music.set_volume(0)
                pygame.mixer.music.play(loop)
                if fade > 0:
                    def fade_in():
                        nonlocal fade
                        for _ in range(int(fade / 0.1)):
                            pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)
                            time.sleep(0.1)

                    threading.Thread(target=fade_in).start()

        class Mouse:
            is_cursor = False

        class Game:
            class Variable:
                loading = True
                playing = False
                paused = False

            class Chance:
                HEART = 20
                ENERGY = 20

            class Increasement:
                ENERGY = 0.15
                HEALTH = 0.003
                SCORE = 1

                JUMP_ENERGY = 5
                JUMP_VELOCITY = 17.5

            def reset(self):
                self.Chance.HEART = 20
                self.Chance.ENERGY = 1

                self.Increasement.ENERGY = 0.15
                self.Increasement.HEALTH = 0.003
                self.Increasement.SCORE = 1
                self.Increasement.JUMP_ENERGY = 5
                self.Increasement.JUMP_VELOCITY = 17.5

        class SpecialObject:
            class Menu:
                def __init__(self, **kwargs):
                    self.other = kwargs
                    self.objects = self.get()

                def display(self):
                    self.objects = self.get()

                def get(self):
                    if self.other:
                        return pygame.draw.rect(**self.other)
                    return pygame.draw.rect(screen, BACKGROUND_COLOR, pygame.rect.Rect(0, GAME_HEIGHT + 5, GAME_WIDTH,
                                                                                       HEIGHT - GAME_HEIGHT)), pygame.draw.rect(
                        screen, 'black', pygame.rect.Rect(0, GAME_HEIGHT + 5, GAME_WIDTH, 3))

            class Button:
                def __init__(self, self_surface, outer_color: tuple | str, inner_color: tuple | str,
                             position: tuple | list,
                             width: int, height: int, cost: int = 0, border_size: int = 3, border_radius: int = 0,
                             texts=None):
                    if texts is None:
                        texts = []

                    self.surface = self_surface
                    self.outer_color = outer_color
                    self.inner_color = inner_color
                    self.x, self.y = position
                    self.width = width
                    self.height = height
                    self.border_size = border_size
                    self.border_radius = border_radius
                    self.text_list = texts

                    self.cost = cost

                    self.outer_object, self.inner_object = self.get()

                def display(self):
                    self.outer_object, self.inner_object = self.get()
                    for text in self.text_list:
                        text.write()

                def get(self):
                    return pygame.draw.rect(self.surface, self.outer_color,
                                            pygame.Rect(self.x, self.y, self.width + self.border_size * 2,
                                                        self.height + self.border_size * 2),
                                            border_radius=self.border_radius), pygame.draw.rect(self.surface,
                                                                                                self.inner_color,
                                                                                                pygame.Rect(
                                                                                                    self.x + self.border_size,
                                                                                                    self.y + self.border_size,
                                                                                                    self.width,
                                                                                                    self.height),
                                                                                                border_radius=self.border_radius)

            class Loading:
                def __init__(self):
                    self.screen = pygame.Surface((WIDTH, HEIGHT))

                    self.headerText = Utilities.Write(self.screen, f'{__project__}', (WIDTH / 2, HEIGHT / 2 - 75),
                                                      anchor='center', size=50)
                    self.versionText = Utilities.Write(self.screen, f'v{__version__}', (WIDTH / 2, HEIGHT / 2 - 45),
                                                       anchor='center',
                                                       size=15)

                    self.frame = pygame.draw.rect(self.screen, 'white', pygame.rect.Rect(0, 0, WIDTH, HEIGHT))
                    self.loadingProgressbar = Utilities.Widget.Progressbar(self.screen, 'black', 'green',
                                                                           (WIDTH / 2 - 150, HEIGHT / 2 + 10), 300, 20,
                                                                           border_radius=3, progress=0,
                                                                           surface=self.screen,
                                                                           text='Loading...', size=15, coordinates=(
                            WIDTH / 2 - 150, HEIGHT / 2 - 10))
                    self.progress = self.loadingProgressbar.progress

                    self.showTips = Utilities.Write(self.screen, f'', (WIDTH / 2, HEIGHT - 10), size=15,
                                                    anchor='center')

                    self.endscreen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    self.endalpha = 1
                    self.endalpha_up = 5

                    self.background_image = BACKGROUND_IMAGE.copy()
                    self.background_image.set_alpha(1)

                def display(self):
                    screen.blit(self.screen, (0, 0)) if self.progress <= 400 else None

                    self.frame = pygame.draw.rect(self.screen, 'white', pygame.rect.Rect(0, 0, WIDTH, HEIGHT))
                    self.screen.blit(self.background_image, (0, 0))

                    self.headerText.write()
                    self.versionText.write()

                    self.loadingProgressbar.display()
                    self.showTips.write() if self.progress < self.loadingProgressbar.width else None

                    if random.randint(1, 2) == random.randint(1, 2):
                        self.progress += 1
                        self.loadingProgressbar.progress = self.progress
                        self.background_image.set_alpha(
                            self.loadingProgressbar.progress) if self.progress <= self.loadingProgressbar.width else None

                        if self.progress == self.loadingProgressbar.width:
                            self.loadingProgressbar = Utilities.Widget.Progressbar(self.screen, 'black', 'green',
                                                                                   (WIDTH / 2 - 150, HEIGHT / 2 + 10),
                                                                                   300, 20, border_radius=3,
                                                                                   progress=300,
                                                                                   surface=self.screen,
                                                                                   text='Initializing...',
                                                                                   size=15, coordinates=(
                                    WIDTH / 2 - 150, HEIGHT / 2 - 10))

                        if self.progress >= 400:
                            pygame.mixer.Sound('assets\\sounds\\loading_success.mp3').play()
                            self.endscreen.fill((237, 235, 235, self.endalpha))
                            self.endalpha += self.endalpha_up
                            if self.endalpha_up < 0:
                                MENU_SCREEN.display(50 - self.endalpha)
                            # print(self.endalpha, self.endalpha_up, self.endscreen.get_alpha())
                            if self.endalpha > 100:
                                self.endalpha_up = -5
                            if self.endalpha <= 0:
                                Utilities.Storage.Game.Variable.loading = False
                                Utilities.Storage.Mechanics.play_music(loop=-1, fade=5)
                            screen.blit(self.endscreen, (0, 0))


pygame.mouse.set_visible(Utilities.Storage.Mouse.is_cursor)


class Player:
    def __init__(self, x=WIDTH / 2, y=HEIGHT / 2, color: str | tuple = 'black', border_color: str | tuple = 'black',
                 width=27, height=27, velocity: tuple = (0.5, 0.5),
                 border_radius: int = 3, border_size: int = 3):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_length = border_size

        self.velocity_x, self.velocity_y = velocity
        pygame.draw.rect(screen, color=self.border_color,
                         rect=pygame.rect.Rect(self.x - self.border_length, self.y - self.border_length,
                                               self.width + self.border_length * 2,
                                               self.height + self.border_length * 2),
                         border_radius=self.border_radius)
        self.object = pygame.draw.rect(screen, color=self.color,
                                       rect=pygame.rect.Rect(self.x, self.y, self.width, self.height),
                                       border_radius=self.border_radius)

    def display(self, is_movable: bool = True):
        if is_movable:
            if self.is_bounced():
                self.velocity_x *= -1
            self.x += self.velocity_x
            self.y += self.velocity_y
            self.velocity_y += (5 - self.velocity_y) / 6
        pygame.draw.rect(screen, color=self.border_color,
                         rect=pygame.rect.Rect(self.x - self.border_length, self.y - self.border_length,
                                               self.width + self.border_length * 2,
                                               self.height + self.border_length * 2),
                         border_radius=self.border_radius)
        self.object = pygame.draw.rect(screen, color=self.color,
                                       rect=pygame.rect.Rect(self.x, self.y, self.width, self.height),
                                       border_radius=self.border_radius)

    def is_bounced(self):
        if self.y > GAME_HEIGHT:
            self.y = 0 - self.width
        elif self.y + self.width < 0:
            self.y = GAME_HEIGHT
        if 0 < self.x + self.width / 2 < GAME_WIDTH:
            return False
        return True


class Object:
    def __init__(self, x=WIDTH / 2, y=HEIGHT / 2, radius=5, color: str = 'black', border_color: str | tuple = 'black',
                 border_size: int = 2):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.border_color = border_color
        self.border_size = border_size

        pygame.draw.circle(screen, color=self.border_color, center=(self.x, self.y),
                           radius=self.radius + self.border_size)
        self.object = pygame.draw.circle(screen, color=self.color, center=(self.x, self.y), radius=self.radius)

    def display(self):
        pygame.draw.circle(screen, color=self.border_color, center=(self.x, self.y),
                           radius=self.radius + self.border_size)
        self.object = pygame.draw.circle(screen, color=self.color, center=(self.x, self.y), radius=self.radius)


class MenuScreen:
    def __init__(self):
        self.screen = pygame.Surface((WIDTH, HEIGHT))

        self.headerText = Utilities.Write(self.screen, f'{__project__}', (WIDTH / 2, HEIGHT / 7), anchor='center',
                                          size=50)
        self.versionText = Utilities.Write(self.screen, f'v{__version__}', (WIDTH / 2, HEIGHT / 7 + 30),
                                           anchor='center',
                                           size=15)

        self.playButton = Utilities.Widget.Button(self.screen, 'black', '#65a5d6', (WIDTH / 2 - 90, HEIGHT / 3 - 15),
                                                  180,
                                                  30, border_radius=7, texts=[
                Utilities.Write(self.screen, 'Play', (WIDTH / 2, HEIGHT / 3 + 3), anchor='center', size=15)])
        self.settingButton = Utilities.Widget.Button(self.screen, 'black', '#65a5d6', (WIDTH / 2 - 90, HEIGHT / 3 + 35),
                                                     180,
                                                     30, border_radius=7, texts=[
                Utilities.Write(self.screen, 'Settings', (WIDTH / 2, HEIGHT / 3 + 54), anchor='center', size=15)])
        self.creditButton = Utilities.Widget.Button(self.screen, 'black', '#65a5d6', (5, HEIGHT - 28), 75, 18,
                                                    border_radius=7, texts=[
                Utilities.Write(self.screen, 'Credits', (45, HEIGHT - 16), anchor='center', size=14)])
        self.continueButton = Utilities.Widget.Button(self.screen, 'black', '#65a5d6', (WIDTH / 2 - 90, HEIGHT / 2),
                                                      180,
                                                      30, border_radius=7, texts=[
                Utilities.Write(self.screen, 'Continue', (WIDTH / 2, HEIGHT / 2 + 18), anchor='center', size=15)])
        self.returnButton = Utilities.Widget.Button(self.screen, 'black', '#65a5d6', (WIDTH / 2 - 90, HEIGHT / 2 + 50),
                                                    180,
                                                    30, border_radius=7, texts=[
                Utilities.Write(self.screen, 'Return to menu', (WIDTH / 2, HEIGHT / 2 + 68), anchor='center', size=15)])

        self.frame = pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.rect.Rect(0, 0, WIDTH, HEIGHT))
        self.background_image = BACKGROUND_IMAGE

        self.isSetting = False
        self.isCredited = False

    def display(self, alpha=255, mouse=True):
        pygame.mixer.music.unpause()

        screen.blit(self.screen, (0, 0))
        self.screen.set_alpha(alpha)
        if pygame.key.get_pressed()[pygame.K_RETURN if Utilities.Storage.Game.Variable.paused else pygame.K_SPACE] or \
                pygame.mouse.get_pressed()[
                    0] and self.playButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
            Utilities.Storage.Game.Variable.playing = True
            Utilities.Storage.Game.Variable.paused = False
            pygame.mouse.set_visible(False)
            (lambda x: (x.set_volume(0.5), x.play()))(pygame.mixer.Sound('assets\\sounds\\button.mp3'))
            start_game()
        if self.creditButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
            self.isCredited = True
        else:
            self.isCredited = False
        if self.settingButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
            self.isSetting = True
        else:
            self.isSetting = False

        pygame.mouse.set_cursor(
            pygame.SYSTEM_CURSOR_ARROW) if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW else None
        pygame.mouse.set_visible(mouse)

        self.frame = pygame.draw.rect(self.screen, BACKGROUND_COLOR, pygame.rect.Rect(0, 0, WIDTH, HEIGHT))
        self.background_image.set_alpha(150 if Utilities.Storage.Game.Variable.paused else 255)
        self.screen.blit(self.background_image, (0, 0))

        self.headerText.write()
        self.versionText.write()

        for b in [self.playButton, self.settingButton, self.creditButton]:
            if b is self.playButton:
                b.text_list[0].text = 'New game' if Utilities.Storage.Game.Variable.paused else 'Play'
            b.display()
            if b.inner_object.collidepoint(*pygame.mouse.get_pos()):
                b.inner_color = '#4f8dbd'
            else:
                b.inner_color = '#65a5d6'

        if Utilities.Storage.Game.Variable.paused:
            self.continueButton.display()
            self.returnButton.display()
            if self.continueButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
                self.continueButton.inner_color = '#4f8dbd'
            else:
                self.continueButton.inner_color = '#65a5d6'
            if self.returnButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
                self.returnButton.inner_color = '#b83535'
            else:
                self.returnButton.inner_color = '#d94343'

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.mixer.music.pause()
                Utilities.Storage.Game.Variable.paused = False
                Utilities.Storage.Game.Variable.playing = True
            if self.continueButton.inner_object.collidepoint(*pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    pygame.mixer.music.pause()
                    Utilities.Storage.Game.Variable.paused = False
                    Utilities.Storage.Game.Variable.playing = True
                    (lambda x: (x.set_volume(0.5), x.play()))(pygame.mixer.Sound('assets\\sounds\\button.mp3'))
            if self.returnButton.inner_object.collidepoint(*pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] or \
                    pygame.key.get_pressed()[pygame.K_q]:
                Utilities.Storage.Game.Variable.paused = False
                Utilities.Storage.Game.Variable.playing = False
                (lambda x: (x.set_volume(0.5), x.play()))(pygame.mixer.Sound('assets\\sounds\\button.mp3'))

        Utilities.Write(self.screen, '' if self.isCredited else 'Made by Hung', (WIDTH / 2, HEIGHT - 11),
                        color='#141414',
                        anchor='center', size=15).write()
        self.credits()
        self.settings()

    def credits(self):
        if not self.isCredited:
            return

        pygame.draw.rect(self.screen, 'gray', pygame.rect.Rect(self.creditButton.x,
                                                               self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 15,
                                                               WIDTH / 3 + 50, HEIGHT / 2), border_radius=7)

        Utilities.Write(self.screen, f'{__project__}',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 25),
                        size=20).write()
        Utilities.Write(self.screen, f'Version: {__version__}',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 50),
                        size=15).write()
        self.screen.blit(pygame.transform.scale(pygame.image.load(
            'assets\\icon\\icon2.png' if pygame.key.get_pressed()[pygame.K_LSHIFT] else 'assets\\icon\\icon.png'),
            (35, 35)), (self.creditButton.x + WIDTH / 3 + 3,
                        self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 25))

        Utilities.Write(self.screen, 'Lead developer: Hung',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 80),
                        size=15).write()
        Utilities.Write(self.screen, 'Programmer: Hung',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 100),
                        size=15).write()
        Utilities.Write(self.screen, 'UI Desinger: Hung',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 120),
                        size=15).write()
        # Utilities.Write(self.screen, 'Idea: Hung',
        #                 (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 140),
        #                 size=15).write()
        Utilities.Write(self.screen, 'Art: AI Generated',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 160),
                        size=15).write()
        Utilities.Write(self.screen, 'Icon: AI Generated',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 180),
                        size=15).write()
        Utilities.Write(self.screen, 'Music/Sound: Hung',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 200),
                        size=15).write()

        Utilities.Write(self.screen, 'GitHub: @ItsHungg',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - HEIGHT / 2 + 300),
                        size=15).write()

        Utilities.Write(self.screen, 'Thank you for playing!',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - 26),
                        size=15).write()

        Utilities.Write(self.screen, '- Made by Hung :)',
                        (self.creditButton.x + 10, self.creditButton.y - self.creditButton.height - 6), size=15,
                        color='#%02X%02X%02X' % (
                            random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))).write()

    def settings(self):
        if not self.isSetting:
            return

        pygame.draw.rect(self.screen, 'gray', pygame.rect.Rect(self.settingButton.x - 35,
                                                               self.settingButton.y + self.settingButton.height + 10,
                                                               self.settingButton.width + 70, 25), border_radius=7)

        Utilities.Write(self.screen, 'This feature is not available yet.',
                        (WIDTH / 2, self.settingButton.y + self.settingButton.height + 23), anchor='center',
                        size=15).write()


def start_game():
    global player, coin, obstacle_list, bomb_list, super_bomb_list, heart_list, HEALTH, SCORE, LEVEL, GAME_HEIGHT, energy_bar
    pygame.mixer.music.pause()
    GAME_HEIGHT = 600

    player = Player(velocity=(4.5, 5))
    coin = Object(color='green', y=GAME_HEIGHT / 2 - 50)

    energy_bar.progress = 200

    HEALTH = 100
    LEVEL = 0
    SCORE = 0

    obstacle_list = []
    bomb_list = []
    super_bomb_list = []
    heart_list = []

    button1.cost = 25
    button2.cost = 20
    button3.cost = 15
    button4.cost = 10
    button5.cost = 7
    button6.cost = 5


MENU_SCREEN = MenuScreen()
LOADING_SCREEN = Utilities.Storage.SpecialObject.Loading()

player = Player(velocity=(4.5, 5))
coin = Object(color='#87f02b', y=GAME_HEIGHT / 2 - 50)

cursor = Object(color='yellow', border_size=0)
energy_bar = Utilities.Widget.Progressbar(screen, 'black', 'green', (10, HEIGHT - 25), 200, 15, border_radius=3,
                                          progress=200, surface=screen, text='Energy', coordinates=(10, HEIGHT - 45),
                                          size=15)

menu = Utilities.Storage.SpecialObject.Menu()
button1 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 215, HEIGHT - 80), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '+Score',
                                                                        (GAME_WIDTH - 185, HEIGHT - 65), size=12,
                                                                        anchor='center')], cost=25)
button2 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 140, HEIGHT - 80), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '+Health',
                                                                        (GAME_WIDTH - 110, HEIGHT - 65), size=12,
                                                                        anchor='center')], cost=20)
button3 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 65, HEIGHT - 80), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '+Energy',
                                                                        (GAME_WIDTH - 35, HEIGHT - 65), size=12,
                                                                        anchor='center')], cost=15)
button4 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 215, HEIGHT - 40), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '%Health',
                                                                        (GAME_WIDTH - 185, HEIGHT - 24), size=12,
                                                                        anchor='center')], cost=10)
button5 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 140, HEIGHT - 40), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '%Energy',
                                                                        (GAME_WIDTH - 110, HEIGHT - 24), size=12,
                                                                        anchor='center')], cost=7)
button6 = Utilities.Storage.SpecialObject.Button(screen, 'black', 'pink', (GAME_WIDTH - 65, HEIGHT - 40), 55, 25,
                                                 border_radius=3,
                                                 texts=[Utilities.Write(screen, '+Jump',
                                                                        (GAME_WIDTH - 35, HEIGHT - 24), size=12,
                                                                        anchor='center')], cost=5)
display_cost = Utilities.Write(screen, 'Cost: N/A', (5, GAME_HEIGHT + 13), size=17)
display_info = Utilities.Write(screen, '', (5, GAME_HEIGHT + 32), size=13)

obstacle_list = []
bomb_list = []
super_bomb_list = []
heart_list = []
energy_list = []


@Utilities.run_once
def play_death_sound():
    pygame.mixer.Sound('assets\\sounds\\die.mp3').play()


while running:
    for event in pygame.event.get():
        event_type = event.type
        if event_type == pygame.QUIT:
            running = False
        if not Utilities.Storage.Game.Variable.playing or Utilities.Storage.Game.Variable.loading:
            continue

        if event_type == pygame.KEYDOWN:
            key = event.key
            if key in [pygame.K_SPACE, pygame.K_UP]:
                Utilities.Storage.Mechanics.jump()

            if HEALTH <= 0:
                if key == pygame.K_r:
                    start_game()
                    (lambda x: (x.set_volume(0.5), x.play()))(pygame.mixer.Sound('assets\\sounds\\button.mp3'))
                    play_death_sound.has_run = False
                elif key == pygame.K_RETURN:
                    Utilities.Storage.Game.Variable.playing = False
                    pygame.mixer.music.unpause()
                    play_death_sound.has_run = False

            if key == pygame.K_ESCAPE:
                pygame.mixer.music.unpause()
                Utilities.Storage.Game.Variable.playing = False
                Utilities.Storage.Game.Variable.paused = True

            if HEALTH <= 0:
                continue

            if key == pygame.K_1:
                if SCORE < button1.cost:
                    continue
                SCORE -= button1.cost
                Utilities.Storage.Game.Increasement.SCORE += 1
                button1.cost = int(button1.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()
            elif key == pygame.K_2:
                if SCORE < button2.cost:
                    continue
                SCORE -= button2.cost
                Utilities.Storage.Game.Increasement.HEALTH += 0.005
                button2.cost = int(button2.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()
            elif key == pygame.K_3:
                if SCORE < button3.cost:
                    continue
                SCORE -= button3.cost
                Utilities.Storage.Game.Increasement.ENERGY += 0.05
                button3.cost = int(button3.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()
            elif key == pygame.K_4:
                if SCORE < button4.cost:
                    continue
                SCORE -= button4.cost
                Utilities.Storage.Game.Chance.HEART += 1
                button4.cost = int(button4.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()
            elif key == pygame.K_5:
                if SCORE < button5.cost:
                    continue
                SCORE -= button5.cost
                Utilities.Storage.Game.Chance.ENERGY += 1
                button5.cost = int(button5.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()
            elif key == pygame.K_6:
                if SCORE < button6.cost:
                    continue
                SCORE -= button6.cost
                Utilities.Storage.Game.Increasement.JUMP_VELOCITY += 0.75
                button6.cost = int(button6.cost * 1.25)
                Utilities.Storage.Mechanics.upgrade_sound()

        if event_type == pygame.MOUSEBUTTONDOWN:
            for button in [button1, button2, button3, button4, button5, button6]:
                if button.inner_object.collidepoint(*pygame.mouse.get_pos()):
                    if SCORE < button.cost:
                        break

                    if button.text_list[0].text == '+Score':
                        SCORE -= button1.cost
                        Utilities.Storage.Game.Increasement.SCORE += 1
                        button1.cost = int(button1.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()
                    elif button.text_list[0].text == '+Health':
                        SCORE -= button2.cost
                        Utilities.Storage.Game.Increasement.HEALTH += 0.005
                        button2.cost = int(button2.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()
                    elif button.text_list[0].text == '+Energy':
                        SCORE -= button3.cost
                        Utilities.Storage.Game.Increasement.ENERGY += 0.05
                        button3.cost = int(button3.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()
                    elif button.text_list[0].text == '%Health':
                        SCORE -= button4.cost
                        Utilities.Storage.Game.Chance.HEART += 1
                        button4.cost = int(button4.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()
                    elif button.text_list[0].text == '%Energy':
                        SCORE -= button5.cost
                        Utilities.Storage.Game.Chance.ENERGY += 1
                        button5.cost = int(button5.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()
                    elif button.text_list[0].text == '+Jump':
                        SCORE -= button6.cost
                        Utilities.Storage.Game.Increasement.JUMP_VELOCITY += 0.75
                        button6.cost = int(button6.cost * 1.25)
                        Utilities.Storage.Mechanics.upgrade_sound()

            if pygame.mouse.get_pos()[1] > GAME_HEIGHT:
                continue
            mouse_key = event.button
            if mouse_key == 1:
                Utilities.Storage.Mechanics.jump()
            elif mouse_key == 2:
                cursor.color = '#%02X%02X%02X' % (
                    random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            elif mouse_key == 3:
                pygame.mouse.set_visible(False if pygame.mouse.get_visible() else True)
                Utilities.Storage.Mouse.is_cursor = pygame.mouse.get_visible()
            elif mouse_key == 4:
                if cursor.radius > 10:
                    continue
                cursor.border_size += 1
                cursor.radius += 1
            elif mouse_key == 5:
                if cursor.radius <= 5:
                    continue
                cursor.radius -= 1
                cursor.border_size -= 1

        if event_type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pos()[1] > GAME_HEIGHT:
                if not pygame.mouse.get_visible():
                    pygame.mouse.set_visible(True)
            else:
                if Utilities.Storage.Mouse.is_cursor != pygame.mouse.get_visible():
                    pygame.mouse.set_visible(Utilities.Storage.Mouse.is_cursor)

    if Utilities.Storage.Game.Variable.loading:
        LOADING_SCREEN.display()

        pygame.display.flip()
        clock.tick(60)
        continue

    if not Utilities.Storage.Game.Variable.playing:
        MENU_SCREEN.display()

        pygame.display.flip()
        clock.tick(60)
        continue

    screen.fill(BACKGROUND_COLOR)
    BACKGROUND_IMAGE.set_alpha(200)
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    if coin.object.colliderect(player.object):
        coin.x = random.randint(coin.radius + 1, GAME_WIDTH - coin.radius - 1)
        coin.y = random.randint(coin.radius + 1, GAME_HEIGHT - coin.radius - 1)

        if coin.color != 'purple':
            SCORE += Utilities.Storage.Game.Increasement.SCORE
        else:
            SCORE += random.randint(3, 5)
            HEALTH += (100 - HEALTH) // 5
            energy_bar.progress += (200 - energy_bar.progress) // 5

        if SCORE > 0 and SCORE % 25 == 0:
            coin.color = 'purple'
        else:
            coin.color = '#87f02b'

        player.velocity_x *= 1.0075
        LEVEL += 1

        bomb_list.append(
            Object(color='red', x=random.randint(50, GAME_WIDTH - 50), y=random.randint(50, GAME_HEIGHT - 50)))
        if LEVEL % 15 == 0:
            bomb_list.clear()
            obstacle_list.clear()
            super_bomb_list.clear()
        if random.randint(1, 15) == random.randint(1, 15) and LEVEL > 5:
            obstacle_list.append(
                Player(x=random.randint(50, GAME_WIDTH - 50), y=random.randint(50, GAME_HEIGHT - 50),
                       width=random.randint(4, 12),
                       height=random.randint(25, 50), border_radius=1, color='black', border_color='#ed3939',
                       border_size=2))
        if random.choices([0, 1], weights=[Utilities.Storage.Game.Chance.HEART, HEALTH]) == [0] and HEALTH < 100:
            heart_list.append(
                Object(color='#f9affa', x=random.randint(50, GAME_WIDTH - 50), y=random.randint(50, GAME_HEIGHT - 50)))
        if random.choices([0, 1], weights=[Utilities.Storage.Game.Chance.ENERGY, 100]) == [
            0] and energy_bar.progress <= 150:
            energy_list.append(
                Object(color='#2bb7cc', x=random.randint(50, GAME_WIDTH - 50), y=random.randint(50, GAME_HEIGHT - 50)))
        if random.randint(1, 100) == random.randint(1, 100) and LEVEL > 20:
            super_bomb_list.append(
                Object(color='black', x=random.randint(50, GAME_WIDTH - 50), y=random.randint(50, GAME_HEIGHT - 50),
                       border_color='red'))

    if HEALTH <= 0:
        play_death_sound()
        died_text_object = Utilities.Write(screen, 'You died', (WIDTH / 2, HEIGHT / 2 - 10), anchor='center')
        died_text_score_object = Utilities.Write(screen, f'Your score: {SCORE}', (WIDTH / 2, HEIGHT / 2 + 20),
                                                 anchor='center')
        Utilities.Write(screen, f'Press [ENTER] to continue', (WIDTH / 2, HEIGHT / 2 + 45), anchor='center', size=10,
                        color='#3b3d3c').write()
        Utilities.Write(screen, f'Press [R] to restart', (WIDTH / 2, HEIGHT / 2 + 57), anchor='center', size=10,
                        color='#3b3d3c').write()
        author_text_object = Utilities.Write(screen, 'Made by Hung', (WIDTH / 2, HEIGHT - 10), anchor='center',
                                             color='gray', size=15)

        if player.object.colliderect(died_text_object.write()[1]):
            died_text_object.color = '#%02X%02X%02X' % (
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if player.object.colliderect(died_text_score_object.write()[1]):
            died_text_score_object.color = '#%02X%02X%02X' % (
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if player.object.colliderect(author_text_object.write()[1]):
            author_text_object.color = 'black'
        else:
            author_text_object.color = 'gray'

        died_text_object.write()
        died_text_score_object.write()
        author_text_object.write()
        Utilities.Storage.Game().reset()

        display_cost.text = 'Item: N/A'
        display_info.text = ''

        HEALTH = 0
        GAME_HEIGHT = HEIGHT
        energy_bar.progress = 100
        obstacle_list.clear()
        bomb_list.clear()
        super_bomb_list.clear()
        heart_list.clear()
        energy_list.clear()
        coin.x, coin.y, coin.color = -WIDTH, -HEIGHT, BACKGROUND_COLOR
    else:
        Utilities.Write(screen, 'Score', (5, 5), size=15).write()
        Utilities.Write(screen, str(SCORE).zfill(2), (5, 20)).write()
        Utilities.Write(screen, 'Health', (WIDTH - 52.5, 5), size=15).write()
        Utilities.Write(screen, f'{str(round(HEALTH)).center(3)}', (WIDTH - 55, 20),
                        color='#549c5b' if HEALTH > 75 else '#b1bd31' if 45 < HEALTH <= 75 else '#de7d28' if 20 < HEALTH <= 45 else '#ba4536').write()

        energy_bar.progress += Utilities.Storage.Game.Increasement.ENERGY
        energy_bar.inner_color = 'green' if energy_bar.progress > 150 else '#aef261' if 100 < energy_bar.progress <= 150 else '#b1bd31' if 75 < energy_bar.progress <= 100 else '#de7d28' if 35 < energy_bar.progress <= 75 else '#ba4536'
        HEALTH += Utilities.Storage.Game.Increasement.HEALTH
        if HEALTH >= 100:
            HEALTH = 100

        # while any(coin.object.colliderect(i) for i in energy_bar.get()):
        #     coin.x = random.randint(coin.radius + 1, GAME_WIDTH - coin.radius - 1)
        #     coin.y = random.randint(coin.radius + 1, GAME_HEIGHT
        #                             - coin.radius - 1)
        #     coin.display()

        for obstacle in obstacle_list:
            obstacle.display(False)
            if obstacle.object.colliderect(player.object):
                HEALTH -= 1
        for bomb in bomb_list:
            if bomb.object.colliderect(coin.object):
                bomb.x, bomb.y = random.randint(50, GAME_WIDTH - 50), random.randint(50, GAME_HEIGHT
                                                                                     - 50)
            bomb.display()
            if bomb.object.colliderect(player.object):
                HEALTH -= 15
                bomb_list.remove(bomb)
        for heart in heart_list:
            heart.display()
            if heart.object.colliderect(player.object):
                HEALTH += 20
                if HEALTH > 100:
                    HEALTH = 100
                heart_list.remove(heart)
        for energy in energy_list:
            energy.display()
            if energy.object.colliderect(player.object):
                energy_bar.progress += 30
                energy_list.remove(energy)
        for bomb in super_bomb_list:
            if bomb.object.colliderect(coin.object):
                bomb.x, bomb.y = random.randint(50, GAME_WIDTH - 50), random.randint(50, GAME_HEIGHT
                                                                                     - 50)
            bomb.display()
            if bomb.object.colliderect(player.object):
                HEALTH -= 50
                super_bomb_list.remove(bomb)

    cursor.x, cursor.y = pygame.mouse.get_pos()
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR if cursor.y < GAME_HEIGHT else pygame.cursors.arrow)

    coin.display()
    player.display()

    if HEALTH > 0:
        menu.display()
        energy_bar.display()
        display_cost.write()
        display_info.write()

        # Utilities.Write(screen, f'Distance: {round(pygame.math.Vector2(player.x, player.y).distance_to((coin.x, coin.y)))}', (5, GAME_HEIGHT+12), size=15).write()
        # pygame.draw.line(screen, coin.color, (player.x+player.width/2, player.y+player.height/2), (coin.x, coin.y), 3)
        # for i in bomb_list+super_bomb_list+heart_list+energy_list+obstacle_list:
        #     pygame.draw.line(screen, i.color, (player.x + player.width / 2, player.y + player.height / 2),
        #                      (i.x, i.y), 3)

        for button in [button1, button2, button3, button4, button5, button6]:
            if SCORE < button.cost:
                button.inner_color = 'gray'
            button.display()

            # print(button.inner_object.collidepoint(*pygame.mouse.get_pos()))
            if button.inner_object.collidepoint(*pygame.mouse.get_pos()):
                display_cost.text = f'Cost: {button.cost}'
                if button.text_list[0].text == '+Score':
                    display_info.text = 'Increase the number of score you get'
                elif button.text_list[0].text == '+Health':
                    display_info.text = 'Increase the healing speed'
                elif button.text_list[0].text == '+Energy':
                    display_info.text = 'Increase the energy bar speed'
                elif button.text_list[0].text == '%Health':
                    display_info.text = 'Increase the chance of spawning Health'
                elif button.text_list[0].text == '%Energy':
                    display_info.text = 'Increase the chance of spawning Energy'
                elif button.text_list[0].text == '+Jump':
                    display_info.text = 'Increase the jump power (height)'
                else:
                    display_info.text = ''
                button.inner_color = '#f0a5b2'
            else:
                button.inner_color = 'pink'

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
