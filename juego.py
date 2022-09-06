#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sugar3.activity.activity import get_activity_root
import time
import locale
import logging
from pygame.locals import Rect
from pygame.locals import QUIT
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEMOTION
from pygame.locals import K_ESCAPE
from pygame.locals import KEYDOWN
import pygame
import random
from gi.repository import Gtk
import os
import gi
gi.require_version('Gtk', '3.0')


class number(pygame.sprite.Sprite):

    def __init__(self, x, y, image, answer=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(
            (x, y), (self.image.get_width(), self.image.get_height()))
        self.answer = answer

    def update(self, time_to_iterate, vel, level):
        incremento_nivel = {"facil": 1, "medio": 2, "dificil": 3}
        self.rect.move_ip(0, time_to_iterate * vel * incremento_nivel[level])


class expresion:

    def __init__(self, level, fuente):

        incremento_nivel = {"facil": 9, "medio": 20, "dificil": 50}
        operacion = {1: "+", 2: "-", 3: "*", 4: "/"}
        self.fuente = fuente
        self.simbolo = {1: "+", 2: "-", 3: "X", 4: ":"}
        self.operador = random.randint(2, 3)
        self.primero = str(random.randint(0, incremento_nivel[level]))
        self.segundo = str(random.randint(0, incremento_nivel[level]))
        self.expresion = fuente.render(
            self.primero +
            self.simbolo[self.operador] +
            self.segundo +
            " = ? ",
            True,
            (255, 120, 120))
        self.resultado = str(
            eval(
                self.primero +
                operacion[self.operador] +
                self.segundo))
        self.vida = 0

        list_y = [int(sx(-120)), int(sx(-105)), int(sx(-90)),
                  int(sx(-75)), int(sx(-60)), int(sx(-45)),
                  int(sx(-30)), int(sx(-15)), int(sx(-0))]
        list_x = [int(sx(80)), int(sx(200)), int(sx(320)),
                  int(sx(440)), int(sx(560)), int(sx(680)),
                  int(sx(800)), int(sx(920)), int(sx(1040)),
                  int(sx(1160))]

        def rand_generator_x():
            rand_coord_x = random.choice(list_x)
            list_x.remove(rand_coord_x)
            return rand_coord_x

        def rand_generator_y():
            rand_coord_y = random.choice(list_y)
            list_y.remove(rand_coord_y)
            return rand_coord_y

        self.preguntas = pygame.sprite.Group()
        self.correct_number = number(
            rand_generator_x(), rand_generator_y(),
            fuente.render(
                self.resultado, True, (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                )
            ),
            True
        )
        self.preguntas.add(self.correct_number)
        self.wrong_numbers = []
        for i in range(0, 5):
            if random.randint(0, 1) == 0:
                wrong = str(int(self.resultado) - random.randint(1, 10))
            else:
                wrong = str(int(self.resultado) + random.randint(1, 10))
            wrong_x_coord = rand_generator_x()
            wrong_y_coord = rand_generator_y()
            image_wrong = fuente.render(
                wrong, True, (random.randint(
                    100, 255), random.randint(
                    100, 255), random.randint(
                    100, 255)))
            self.wrong_numbers.append(number(
                wrong_x_coord,
                wrong_y_coord,
                image_wrong,
                False))
        self.preguntas.add(*self.wrong_numbers)

    def update_expression(self, user):
        self.expresion = self.fuente.render(
            self.primero +
            self.simbolo[self.operador] +
            self.segundo +
            " = " +
            user,
            True,
            (255, 120, 120)
        )


def cargar_imagen(nombre, trasnparent=False):
    try:
        imagen = pygame.image.load(nombre)
        sizex, sizey = imagen.get_rect().size
        imagen = \
            pygame.transform.scale(imagen,
                                   (int(sizex * scale_x),
                                    int(sizey * scale_y)))
    except pygame.error as message:
        raise SystemExit(message)
    imagen = imagen.convert()
    return imagen


def get_translated_text(text):
    if locale.getdefaultlocale()[0][:2] != "es":
        return text
    translations = {
        "PLAY" : "JUGAR",
        "LEVEL" : "NIVEL",
        "QUIT" : "SALIR",
        "easy" : "facil",
        "medium" : "medio",
        "hard" : "dificil",
        "Score : " : "Punjate : ",
        "Highest Score : " : "Puntaje Mas Alto : ",
        "Timer : " : "Temporizador : ",
        "PLAY AGAIN" : "jUEGA DE NUEVO",
        "GAME OVER!!" : "JUEGO TERMINADO!!",
        "Hurray! you won :)" : "Hurra! ganaste :)",
        "Ay! you lost :(" : "Ay! perdiste :(",
        "Select correct ball to answer or type it using keyboard" : "Selecciona la bola correcta para responder o escribe la respuesta usando el teclado",
    }
    return translations[text]


class Game():

    def __init__(self, activity):
        self.activity = activity
        self.user = ""
        self.keys = (
            pygame.K_0,
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
            pygame.K_MINUS,
            pygame.K_BACKSPACE,
            pygame.K_RETURN,
        )

    global sx, sy

    def sx(coord_x):
        return coord_x * scale_x

    def sy(coord_y):
        return coord_y * scale_y

    def main(self):
        sonido_menu = load_sound("menu.ogg")
        jugar = self.fuente_130.render(
            get_translated_text("PLAY"), True, (0, 0, 255), (0, 0, 0))
        level = self.fuente_130.render(
            get_translated_text("LEVEL"), True, (0, 0, 255), (0, 0, 0))
        quit = self.fuente_130.render(
            get_translated_text("QUIT"), True, (0, 0, 255), (0, 0, 0))
        help = self.fuente_32.render(
            get_translated_text(
                "Select correct ball to answer or type it using keyboard"),
            True,
            (0,
             255,
             0),
            (0,
             0,
             0))
        fondo = cargar_imagen('data/1.jpg')
        chosen_level = "facil"

        while self.running:
            self.screen.fill((0, 0, 0))
            jugar_rect = jugar.get_rect()
            jugar_rect.x = sx(475)
            jugar_rect.y = sy(180)
            level_rect = level.get_rect()
            level_rect.x = sx(475)
            level_rect.y = sy(360)
            quit_rect = jugar.get_rect()
            quit_rect.x = sx(475)
            quit_rect.y = sy(540)
            help_rect = jugar.get_rect()
            help_rect.x = sx(600) - help.get_rect().width / 2
            help_rect.y = sy(840)
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(jugar, jugar_rect)
            self.screen.blit(level, level_rect)
            self.screen.blit(quit, quit_rect)
            self.screen.blit(help, help_rect)
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    not_hover = True
                    if not_hover:
                        jugar = self.fuente_130.render(
                            get_translated_text("PLAY"), True, (0, 0, 255), (0, 0, 0))
                        level = self.fuente_130.render(
                            get_translated_text("LEVEL"), True, (0, 0, 255), (0, 0, 0))
                        quit = self.fuente_130.render(
                            get_translated_text("QUIT"), True, (0, 0, 255), (0, 0, 0))

                    if event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + jugar.get_width() and \
                            event.pos[1] > sy(180) and \
                            event.pos[1] < sy(180) + jugar.get_height():
                        jugar = self.fuente_130.render(
                            get_translated_text("PLAY"),
                            True, (122, 245, 61),
                            (102, 110, 98))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + level.get_width() and \
                            event.pos[1] > sy(360) and \
                            event.pos[1] < sy(360) + level.get_height():
                        level = self.fuente_130.render(
                            get_translated_text("LEVEL"),
                            True, (122, 245, 61),
                            (102, 110, 98))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + quit.get_width() and \
                            event.pos[1] > sy(540) and \
                            event.pos[1] < sy(540) + quit.get_height():
                        quit = self.fuente_130.render(
                            get_translated_text("QUIT"),
                            True, (122, 245, 61),
                            (102, 110, 98))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    else:
                        not_hover = True
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + jugar.get_width() \
                                and event.pos[1] > sy(180) and \
                                event.pos[1] < sy(180) + jugar.get_height():
                            return chosen_level
                        elif event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + level.get_width() \
                                and event.pos[1] > sy(360) and \
                                event.pos[1] < sy(360) + level.get_height():
                            chosen_level = self.choose_level()
                        elif event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + quit.get_width() \
                                and event.pos[1] > sy(540) and \
                                event.pos[1] < sy(540) + quit.get_height():
                            self.running = False
                            self.activity.close()
            pygame.display.update()

    def choose_level(self):

        sonido_menu = load_sound("menu.ogg")
        facil = self.fuente_130.render(
            get_translated_text("easy"), True, (0, 0, 255), (0, 0, 0))
        medio = self.fuente_130.render(
            get_translated_text("medium"), True, (0, 0, 255), (0, 0, 0))
        dificil = self.fuente_130.render(
            get_translated_text("hard"), True, (0, 0, 255), (0, 0, 0))
        fondo = cargar_imagen('data/1.jpg')
        level = "facil"
        while self.running:
            self.screen.fill((0, 0, 0))
            facil_rect = facil.get_rect()
            facil_rect.x = sx(470)
            facil_rect.y = sy(180)
            medio_rect = medio.get_rect()
            medio_rect.x = sx(417)
            medio_rect.y = sy(360)
            dificil_rect = dificil.get_rect()
            dificil_rect.x = sx(465)
            dificil_rect.y = sy(540)
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(facil, facil_rect)
            self.screen.blit(medio, medio_rect)
            self.screen.blit(dificil, dificil_rect)
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    not_hover = True
                    if not_hover:
                        facil = self.fuente_130.render(
                            get_translated_text("easy"), True, (0, 0, 255), (0, 0, 0))
                        medio = self.fuente_130.render(
                            get_translated_text("medium"), True, (0, 0, 255), (0, 0, 0))
                        dificil = self.fuente_130.render(
                            get_translated_text("hard"), True, (0, 0, 255), (0, 0, 0))

                    if event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + facil.get_width() and \
                            event.pos[1] > sy(180) and \
                            event.pos[1] < sy(180) + facil.get_height():
                        facil = self.fuente_130.render(
                            get_translated_text("easy"), True, (0, 255, 0), (0, 0, 0))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + medio.get_width() and \
                            event.pos[1] > sy(360) and \
                            event.pos[1] < sy(360) + medio.get_height():
                        medio = self.fuente_130.render(
                            get_translated_text("medium"), True, (0, 255, 0), (0, 0, 0))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and \
                            event.pos[0] < sx(450) + dificil.get_width() and \
                            event.pos[1] > sy(540) and \
                            event.pos[1] < sy(540) + dificil.get_height():
                        dificil = self.fuente_130.render(
                            get_translated_text("hard"), True, (0, 255, 0), (0, 0, 0))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    else:
                        not_hover = True
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + facil.get_width() \
                                and event.pos[1] > sy(180) and \
                                event.pos[1] < sy(180) + facil.get_height():
                            pass
                            return level
                        elif event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + medio.get_width() \
                                and event.pos[1] > sy(360) and \
                                event.pos[1] < sy(360) + medio.get_height():
                            level = "medio"
                            return level
                        elif event.pos[0] > sx(450) and \
                                event.pos[0] < sx(450) + dificil.get_width() \
                                and event.pos[1] > sy(540) and \
                                event.pos[1] < sy(540) + dificil.get_height():
                            level = "dificil"
                            return level
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        level = "facil"
                        return level
            pygame.display.update()

    def play(self, level):
        die_point = {"facil": 200, "medio": 100, "dificil": 60}

        another_quest = True

        right_sound = load_sound("right.ogg")
        wrong_sound = load_sound("wrong.ogg")
        fondo = cargar_imagen("data/" + str(1) + ".jpg")
        score = 0
        puntuacionalta = load_puntuacionalta()
        response = 0
        sonido_menu = load_sound("menu.ogg")
        play_again = self.fuente_60.render(
            get_translated_text("PLAY AGAIN"), True, (0, 0, 0), (255, 0, 0))
        quit_game = self.fuente_60.render(
            get_translated_text("QUIT"), True, (0, 0, 0), (255, 0, 0))
        max_time_limit = 60.00
        start_time = time.time()
        current_time = max_time_limit
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo, (0, 0))
            if response == 0:
                time_to_iterate = self.clock.tick(30) / 1000.
                if another_quest:
                    nueva_expresion = expresion(level, self.fuente_60)
                    another_quest = False

                nueva_expresion.vida += 1
                if nueva_expresion.vida > die_point[level]:
                    if wrong_sound is not None:
                        wrong_sound.play()
                    another_quest = True
                # esto va?
                # score -= 7

                nueva_expresion.preguntas.update(
                    time_to_iterate, random.randint(80, 155), level)
                self.screen.blit(
                    self.fuente_32.render(
                        get_translated_text("Score : ") + str(score),
                        True,
                        (120, 255, 120)),
                    (sx(260), 0))
                self.screen.blit(
                    self.fuente_32.render(
                        get_translated_text(
                            "Highest Score : ") + str(puntuacionalta),
                        True,
                        (120, 255, 120)),
                    (sx(450), 0))
                self.screen.blit(nueva_expresion.expresion, (sx(200), sy(750)))
                for number in (nueva_expresion.correct_number,
                               *nueva_expresion.wrong_numbers):
                    pygame.draw.circle(
                        self.screen, (40, 40, 40), number.rect.center, 50)
                nueva_expresion.preguntas.draw(self.screen)
                current_time = max_time_limit - (time.time() - start_time)
                countdown_time = "{:.2f}".format(current_time)
                self.screen.blit(
                    self.fuente_32.render(
                        get_translated_text("Timer : ") + str(countdown_time),
                        True,
                        (120, 255, 120)),
                    (sx(780), 0))

            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            if float(current_time) <= 00.10:
                game_over()
                response = 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    not_hover = True
                    if not_hover:
                        play_again = self.fuente_60.render(
                            get_translated_text("PLAY AGAIN"), True, (0, 0, 255), (0, 0, 0))
                        quit_game = self.fuente_60.render(
                            get_translated_text("QUIT"), True, (0, 0, 255), (0, 0, 0))

                    if event.pos[0] > sx(60) and \
                            event.pos[0] < sx(60) + play_again.get_width() and \
                            event.pos[1] > sy(700) and \
                            event.pos[1] < sy(700) + play_again.get_height():
                        play_again = self.fuente_60.render(
                            get_translated_text("PLAY AGAIN"),
                            True, (122, 245, 61),
                            (102, 110, 98))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    if event.pos[0] > sx(840) and \
                            event.pos[0] < sx(840) + quit_game.get_width() and \
                            event.pos[1] > sy(700) and \
                            event.pos[1] < sy(700) + quit_game.get_height():
                        quit_game = self.fuente_60.render(
                            get_translated_text("QUIT"), True, (122, 245, 61), (102, 110, 98))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    else:
                        not_hover = True
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in nueva_expresion.preguntas.sprites():
                            if event.pos[0] > i.rect.x and \
                                    event.pos[0] < i.rect.x \
                                    + i.image.get_width() \
                                    and event.pos[1] > i.rect.y and \
                                    event.pos[1] < i.rect.y \
                                    + i.image.get_height():
                                if i.answer:
                                    if right_sound is not None:
                                        right_sound.play()
                                    another_quest = True
                                    score += 7

                                else:
                                    if right_sound is not None:
                                        wrong_sound.play()
                                    another_quest = True
                                    score -= 3
                        if response == 1:
                            if event.pos[0] > sx(60) and \
                                    event.pos[0] < sx(60) + play_again.get_width() and \
                                    event.pos[1] > sy(700) and \
                                    event.pos[1] < sy(700) + play_again.get_height():
                                return
                            if event.pos[0] > sx(840) and \
                                    event.pos[0] < sx(840) + quit_game.get_width() and \
                                    event.pos[1] > sy(700) and \
                                    event.pos[1] < sy(700) + quit_game.get_height():
                                self.running = False
                                self.activity.close()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
                    if event.key in self.keys:
                        if event.key == pygame.K_RETURN:
                            if self.user == nueva_expresion.resultado:
                                if right_sound is not None:
                                    right_sound.play()
                                score += 7
                            else:
                                if right_sound is not None:
                                    wrong_sound.play()
                                score -= 3
                            another_quest = True
                            self.user = ""
                        elif event.key == pygame.K_BACKSPACE:
                            self.user = self.user[:-1]
                        elif event.key == pygame.K_MINUS:
                            if len(self.user) > 0 and self.user[0] == "-":
                                self.user = self.user[1:]
                            else:
                                self.user = "-" + self.user
                        else:
                            self.user += pygame.key.name(event.key)
                        nueva_expresion.update_expression(self.user)
                save_puntuacionalta(score)

            def game_over():

                high_score = puntuacionalta
                while Gtk.events_pending():
                    Gtk.main_iteration()
                gameover = self.fuente_60.render(
                    get_translated_text(
                        "GAME OVER!!"),
                    True, (255, 255, 255),
                    (0, 0, 0))
                if score >= high_score:
                    high_score = score
                    win = self.fuente_130.render(
                        get_translated_text("Hurray! you won :)"),
                        True,
                        (237, 88, 235),
                        (0, 0, 0))
                    win_rect = win.get_rect()
                    win_rect.center = (sx(600), sy(350))
                else:
                    lose = self.fuente_130.render(
                        get_translated_text("Ay! you lost :("),
                        True,
                        (245, 17, 25),
                        (0, 0, 0))
                    lose_rect = lose.get_rect()
                    lose_rect.center = (sx(600), sy(350))
                score_display = self.fuente_60.render(
                    get_translated_text("Score : ") + str(score),
                    True,
                    (0, 255, 255),
                    (0, 0, 0))
                high_score_display = self.fuente_60.render(
                    get_translated_text("Highest Score : ") + str(high_score),
                    True,
                    (0, 255, 255),
                    (0, 0, 0))
                gameover_rect = gameover.get_rect()
                gameover_rect.midtop = (sx(590), sy(100))
                score_display_rect = score_display.get_rect()
                score_display_rect.center = (sx(590), sy(500))
                high_score_display_rect = high_score_display.get_rect()
                high_score_display_rect.midbottom = (sx(590), sy(650))
                quit_rect = quit_game.get_rect()
                quit_rect.bottomleft = (sx(840), sy(780))
                play_again_rect = play_again.get_rect()
                play_again_rect.bottomright = (sx(420), sy(780))
                self.screen.blit(fondo, (0, 0))
                self.screen.blit(gameover, gameover_rect)
                self.screen.blit(score_display, score_display_rect)
                self.screen.blit(
                    high_score_display, high_score_display_rect)
                self.screen.blit(quit_game, quit_rect)
                self.screen.blit(play_again, play_again_rect)
                if score >= high_score:
                    self.screen.blit(win, win_rect)
                else:
                    self.screen.blit(lose, lose_rect)
                pygame.display.flip()
            pygame.display.update()

    def run(self):
        self.running = True
        self.screen = pygame.display.get_surface()

        info = pygame.display.Info()

        if not self.screen:
            self.screen = pygame.display.set_mode(
                (info.current_w, info.current_h))

        global scale_x, scale_y
        scale_x = self.screen.get_width() / 1200.0
        scale_y = self.screen.get_height() / 900.0

        self.clock = pygame.time.Clock()

        self.fuente_32 = pygame.font.Font("data/fuente.ttf", int(sx(32)))
        self.fuente_60 = pygame.font.Font("./data/fuente.ttf", int(sx(60)))
        self.fuente_130 = pygame.font.Font("./data/fuente.ttf", int(sx(130)))

        self.fondo = cargar_imagen('data/1.jpg')
        self.screen.blit(self.fondo, (0, 0))
        pygame.display.flip()
        while self.running:
            level = self.main()
            self.play(level)


# Funcion para cargar Sonidos
def load_sound(name):
    path = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except BaseException:
        logging.debug('Warning, unable to load: ', path)

# Funcion para guardar puntuaciones altas


def save_puntuacionalta(score):
    file_path = os.path.join(get_activity_root(), 'data', 'PuntajeAlto')
    logging.debug(file_path)
    puntuacionalta = []
    puntuacionalta.append(0)
    if os.path.exists(file_path):
        File = open(file_path, "r")
        puntuacionalta = File.readlines()
        File.close()
    p = int(puntuacionalta[0])
    if not(p > score):
        File = open(file_path, "w")
        File.write(str(score))
        File.close()


def load_puntuacionalta():
    file_path = os.path.join(get_activity_root(), 'data', 'PuntajeAlto')
    logging.debug(file_path)
    if os.path.exists(file_path):
        try:
            File = open(file_path, "r")
            puntuacionalta = int(File.readlines()[0])
            File.close()
            return puntuacionalta
        except BaseException:
            return 0
    else:
        return 0
