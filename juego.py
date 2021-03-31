#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pygame.locals import *
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

    def update(self, time, vel, level):
        incremento_nivel = {"facil": 1, "medio": 2, "dificil": 3}
        self.rect.move_ip(0, time * vel * incremento_nivel[level])


class expresion:

    def __init__(self, level, fuente):

        incremento_nivel = {"facil": 9, "medio": 20, "dificil": 50}
        operacion = {1: "+", 2: "-", 3: "*", 4: "/"}
        simbolo = {1: "+", 2: "-", 3: "X", 4: ":"}
        operador = random.randint(2, 3)
        self.primero = str(random.randint(0, incremento_nivel[level]))
        self.segundo = str(random.randint(0, incremento_nivel[level]))
        self.expresion = fuente.render(
            self.primero + simbolo[operador] + self.segundo + " = ? ", True, (255, 0, 0))
        self.resultado = str(
            eval(
                self.primero +
                operacion[operador] +
                self.segundo))
        self.vida = 0

        no_repeat_check_x = []
        no_repeat_check_y = []
        list_y = [int(sx(-90)), int(sx(-80)), int(sx(-60)), int(sx(-50)), int(sx(-40)), int(sx(-30)),
                  int(sx(-20)), int(sx(-10)), int(sx(-0))]
        list_x = [int(sx(100)), int(sx(200)), int(sx(300)), int(sx(400)), int(sx(500)), int(sx(600)),
                  int(sx(700)), int(sx(800)),
                  int(sx(900))]

        def rand_generator_x():
            count_x = 0
            while count_x < len(list_x):
                rand_coord_x = random.choice(list_x)
                count_x += 1
                if rand_coord_x not in no_repeat_check_x:
                    no_repeat_check_x.append(rand_coord_x)
                    return rand_coord_x
            return int(sx(1000))

        def rand_generator_y():
            count_y = 0
            while count_y < len(list_y):
                count_y += 1
                rand_coord_y = random.choice(list_y)
                if rand_coord_y not in no_repeat_check_y:
                    no_repeat_check_y.append(rand_coord_y)
                    return rand_coord_y
            return int(sx(-70))

        self.preguntas = pygame.sprite.Group()
        ans_x_coord = rand_generator_x()
        ans_y_coord = rand_generator_y()
        self.preguntas.add(number(ans_x_coord, ans_y_coord,
                             fuente.render(self.resultado, True, 
                                            (random.randint(0, 255),
                                             random.randint(0, 255), random.randint(0, 255))), True))
        for i in range(0, 5):
            if random.randint(0, 1) == 0:
                wrong = str(int(self.resultado) - random.randint(1, 10))
            else:
                wrong = str(int(self.resultado) + random.randint(1, 10))
            wrong_x_coord = rand_generator_x()
            wrong_y_coord = rand_generator_y()
            image_wrong = fuente.render(
                wrong, True, (random.randint(
                    0, 255), random.randint(
                    0, 255), random.randint(
                    0, 255)))
            self.preguntas.add(
                number(
                    wrong_x_coord,
                    wrong_y_coord,
                    image_wrong,
                    False))


def cargar_imagen(nombre, trasnparent=False):
    try:
        imagen = pygame.image.load(nombre)
        sizex, sizey = imagen.get_rect().size
        imagen = \
            pygame.transform.scale(imagen,
                                   (int(sizex * scale_x), int(sizey * scale_y)))
    except pygame.error as message:
        raise SystemExit(message)
    imagen = imagen.convert()
    return imagen


class Game():

    def __init__(self, get_activity_root):
        self.activity_root = get_activity_root
        pass

    global sx, sy

    def sx(coord_x):
        return coord_x * scale_x

    def sy(coord_y):
        return coord_y * scale_y

    def main(self):
        sonido_menu = load_sound("menu.ogg")
        jugar = self.fuente_130.render("JUGAR", True, (0, 0, 255))
        level = self.fuente_130.render("NIVEL", True, (0, 0, 255))
        quit = self.fuente_130.render("SALIR", True, (0, 0, 255))
        fondo = cargar_imagen('data/1.jpg')
        chosen_level = "facil"

        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(jugar, (sx(450), sy(100)))
            self.screen.blit(level, (sx(450), sy(200)))
            self.screen.blit(quit, (sx(450), sy(300)))
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    if event.pos[0] > sx(550) and event.pos[0] < sx(450) + jugar.get_width() and \
                            event.pos[1] > sy(100) and event.pos[1] < sy(100) + jugar.get_height():
                        jugar = self.fuente_130.render(
                            "JUGAR", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(550) and event.pos[0] < sx(450) + level.get_width() and \
                            event.pos[1] > sy(200) and event.pos[1] < sy(200) + level.get_height():
                        level = self.fuente_130.render(
                            "NIVEL", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(550) and event.pos[0] < sx(450) + quit.get_width() and \
                            event.pos[1] > sy(300) and event.pos[1] < sy(300) + quit.get_height():
                        quit = self.fuente_130.render(
                            "SALIR", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] > sx(450) and event.pos[0] < sx(450) + jugar.get_width() and \
                                event.pos[1] > sy(100) and event.pos[1] < sy(100) + jugar.get_height():
                            return chosen_level
                        elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + level.get_width() and \
                                event.pos[1] > sy(200) and event.pos[1] < sy(200) + level.get_height():
                            chosen_level = self.choose_level()
                        elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + quit.get_width() and \
                                event.pos[1] > sy(300) and event.pos[1] < sy(300) + quit.get_height():
                            self.running = False
                            exit()
            pygame.display.update()

    def choose_level(self):

        sonido_menu = load_sound("menu.ogg")
        facil = self.fuente_130.render("facil", True, (0, 0, 255))
        medio = self.fuente_130.render("medio", True, (0, 0, 255))
        dificil = self.fuente_130.render("dificil", True, (0, 0, 255))
        fondo = cargar_imagen('data/1.jpg')
        level = "facil"
        while self.running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(facil, (sx(450), sy(100)))
            self.screen.blit(medio, (sx(450), sy(200)))
            self.screen.blit(dificil, (sx(450), sy(300)))
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    return
                elif event.type == MOUSEMOTION:
                    if event.pos[0] > sx(450) and event.pos[0] < sx(450) + facil.get_width() and \
                            event.pos[1] > sy(100) and event.pos[1] < sy(100) + facil.get_height():
                        facil = self.fuente_130.render(
                            "facil", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + medio.get_width() and \
                            event.pos[1] > sy(200) and event.pos[1] < sy(200) + medio.get_height():
                        medio = self.fuente_130.render(
                            "medio", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + dificil.get_width() and \
                            event.pos[1] > sy(300) and event.pos[1] < sy(300) + dificil.get_height():
                        dificil = self.fuente_130.render(
                            "dificil", True, (0, 0, 255))
                        if sonido_menu is not None:
                            sonido_menu.play()
                    else:
                        facil = self.fuente_130.render(
                            "facil", True, (0, 0, 255))
                        medio = self.fuente_130.render(
                            "medio", True, (0, 0, 255))
                        dificil = self.fuente_130.render(
                            "dificil", True, (0, 0, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] > sx(450) and event.pos[0] < sx(450) + facil.get_width() and \
                                event.pos[1] > sy(100) and event.pos[1] < sy(100) + facil.get_height():
                            pass
                            return level
                        elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + medio.get_width() and \
                                event.pos[1] > sy(200) and event.pos[1] < sy(200) + medio.get_height():
                            level = "medio"
                            return level
                        elif event.pos[0] > sx(450) and event.pos[0] < sx(450) + dificil.get_width() and \
                                event.pos[1] > sy(300) and event.pos[1] < sy(300) + dificil.get_height():
                            level = "dificil"
                            return level
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        level = "facil"
                        return level
            pygame.display.update()

    def play(self, level):
        NUM_IMAGES = 1

        die_point = {"facil": 200, "medio": 100, "dificil": 60}

        another_quest = True

        right_sound = load_sound("right.ogg")
        wrong_sound = load_sound("wrong.ogg")
        fondo = cargar_imagen("data/" + str(1) + ".jpg")
        score = 0
        puntuacionalta = load_puntuacionalta(self.activity_root)

        while self.running:
            time = self.clock.tick(30) / 1000.
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
                time, random.randint(80, 155), level)

            self.screen.fill((0, 0, 0))
            self.screen.blit(fondo, (0, 0))
            self.screen.blit(
                self.fuente_32.render(
                    "Puntaje: " + str(score), True, (0, 0, 0)), (sx(410), 0))
            self.screen.blit(
                self.fuente_32.render(
                    "Puntaje Mas Alto: " + str(puntuacionalta), True, (0, 0, 0)), (sx(600), 0))
            self.screen.blit(nueva_expresion.expresion, (sx(600), sy(750)))
            nueva_expresion.preguntas.draw(self.screen)
            while Gtk.events_pending():
                Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    save_puntuacionalta(score, self.activity_root)
                    self.running = False
                    return
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in nueva_expresion.preguntas.sprites():
                            if event.pos[0] > i.rect.x and event.pos[0] < i.rect.x + i.image.get_width() and \
                                    event.pos[1] > i.rect.y and event.pos[1] < i.rect.y + i.image.get_height():
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
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return 0
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


def save_puntuacionalta(score, activity_root):
    file_path = os.path.join(activity_root, 'data', 'PuntajeAlto')
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


def load_puntuacionalta(activity_root):
    file_path = os.path.join(activity_root, 'data', 'PuntajeAlto')
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
