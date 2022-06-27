# -*- coding: utf-8 -*-

import pygame as pg
from os import listdir


class FoxApp:
    def __init__(self, _screen, _w, _h, _namedir, _imagesize):
        self.screen = _screen
        self.w      = _w
        self.h      = _h
        self.__NDIR = _namedir
        self.__SIZE = _imagesize

        self.__NUM_L_HEALTH  = 5     # НОМЕР ИЗ СПИСКА РАЗМЕРОВ ИЗОБРАЖЕНИЙ (ЗДОРОВЬЕ и ЭНЕРГИЯ);
        self.__NUM_L_BUSH    = 6     # НОМЕР ИЗ СПИСКА РАЗМЕРОВ ИЗОБРАЖЕНИЙ (РАСТЕНИЯ);
        self.__COUNT_FOX     = 0     # ПОКАДРОВОЕ АНИМАЦИЯ foxi;
        self.__COUNT_BUSH    = 0     # ПОКАДРОВАЯ АНИМАЦИЯ РАСТЕНИЙ;
        self.ANIMATION       = 0     # ВЫБОР АНИМАЦИИ (флаг); ### 2
        self.__FOX_FLIP      = False # НАПРАВЛЕНИЕ ИЗОБРАЖЕНИЯ ПО ХОДУ ДВИЖЕНИЯ (вправо, влево);
        self.__FOX_FLIP_L    = 1     # СЧЁТЧИК ДЛЯ ОПРЕДЕЛЕНИЯ ПОВОРОТА foxi;
        self.__FOX_FLIP_R    = 1     # СЧЁТЧИК ДЛЯ ОПРЕДЕЛЕНИЯ ПОВОРОТА foxi;

        ### ----- ПОДГРУЖАЕМ АНИМАЦИИ ЗДОРОВЬЯ и ЭНЕРГИИ (формируем словарь со всеми анимациями) ------------------- ###
        self.__heal = {}
        img_dir, obj_dir = self.__NDIR['TP'][0], self.__NDIR['TP'][1]
        for item in self.__NDIR['TP'][2]: # СПИСОК ДИРЕКТОРИЙ В ДИРЕКТОРИИ <<top_panel>>;
            self.__heal[item] = [
                pg.transform.scale(
                    pg.image.load('%s/%s/%s/%s.png' % (img_dir, obj_dir, item, img)), (self.__SIZE[self.__NUM_L_HEALTH])
                ) for img in range(1, len(listdir(path='%s/%s/%s/' % (img_dir, obj_dir, item))) + 1)
            ]
        ### -------------------------------------------------------------------------------------------------------- ###
        ### ----- ПОДГРУЖАЕМ АНИМАЦИИ foxi (формируем словарь со всеми анимациями) --------------------------------- ###
        self.__foxi = {}
        iter, img_dir, obj_dir = 0, self.__NDIR['F'][0], self.__NDIR['F'][1]
        for item in self.__NDIR['F'][2]: # СПИСОК ДИРЕКТОРИЙ В ДИРЕКТОРИИ <<foxi>>;
            self.__foxi[item] = [
                pg.transform.scale(
                    pg.image.load('%s/%s/%s/%s.png' % (img_dir, obj_dir, item, img)), (self.__SIZE[iter])
                ) for img in range(1, len(listdir(path='%s/%s/%s/' % (img_dir, obj_dir, item))) + 1)
            ]
            iter += 1
        ### -------------------------------------------------------------------------------------------------------- ###
        ### ----- ПОДГРУЖАЕМ АНИМАЦИИ bush (формируем словарь со всеми анимациями) --------------------------------- ###
        self.__bush = {}
        img_dir, obj_dir = self.__NDIR['BSH'][0], self.__NDIR['BSH'][1]
        for item in self.__NDIR['BSH'][2]:  # СПИСОК ДИРЕКТОРИЙ В ДИРЕКТОРИИ <<bush>>;
            self.__bush[item] = [
                pg.transform.scale(
                    pg.image.load('%s/%s/%s/%s.png' % (img_dir, obj_dir, item, img)), (self.__SIZE[self.__NUM_L_BUSH])
                ) for img in range(1, len(listdir(path='%s/%s/%s/' % (img_dir, obj_dir, item))) + 1)
            ]
        ### -------------------------------------------------------------------------------------------------------- ###
        self.get_position_mouse_for_fox() # ОПРЕДЕЛЯЕМ НАЧАЛЬНЫЕ КООРДИНАТЫ foxi;

    def get_position_mouse_for_fox(self): # ПОЗИЦИЯ foxi;
        ### ----- self.__imgs необходим для определения размера изображения ---------------------------------------- ###
        w, h = self.__SIZE[self.ANIMATION]
        ### ----- x и y нужны для опредления начальных координат foxi ---------------------------------------------- ###
        self.x, self.y = (self.w / 2 - w / 2, self.h - h)

    def draw_foxi(self): # РИСУЕМ НАШУ ЛИСИЧКУ;
        ### ----- Блок для проверки поворота foxi в противоположную сторону ---------------------------------------- ###
        if self.__FOX_FLIP_L == 1 and self.__FOX_FLIP_R == 0:
            self.ANIMATION = 3
            self.__FOX_FLIP_L += 1
        if self.__FOX_FLIP_L == 0 and self.__FOX_FLIP_R == 1:
            self.ANIMATION = 3
            self.__FOX_FLIP_R += 1
        ### ----- Выбираем название директории, где "лежит" анимация foxi ------------------------------------------ ###
        NAME_ANIMATION = self.__NDIR['F'][2][self.ANIMATION]
        ### ----- __COUNT_FOX отвечает за смену изображения (анимация foxi) ---------------------------------------- ###
        if self.__COUNT_FOX >= len(self.__foxi[NAME_ANIMATION]):
            self.__COUNT_FOX = 0
        ### ----- self.__imgs необходим для определения размера изображения ---------------------------------------- ###
        w, h = self.__SIZE[self.ANIMATION]
        ### ----- Костыль: чтобы анимация foxi не искожалась (из сидячего в лежачее состояние) --------------------- ###
        SIZE_SLEEP_LEFT = (11 * 4) if (self.__FOX_FLIP and self.ANIMATION == 1) else 0
        ### ----- Координаты анимаций foxi [ x,y ] ----------------------------------------------------------------- ###
        x, y = self.x - SIZE_SLEEP_LEFT, self.h - h if (self.ANIMATION == 1) else self.h - (h + 10)
        ### ----- Отрисовка различных анимаций foxi ---------------------------------------------------------------- ###
        self.screen.blit(
            pg.transform.flip(
                self.__foxi[NAME_ANIMATION][self.__COUNT_FOX],
                True if self.__FOX_FLIP else False, False
            ), (x, y)
        )
        ### ----- Отрисовка ЗДОРОВЬЯ и ЭНЕРГИИ foxi ---------------------------------------------------------------- ###
        w_tp, h_tp = self.__SIZE[self.__NUM_L_HEALTH][0], self.__SIZE[self.__NUM_L_HEALTH][1]
        # for i in range(-1, 2):
        #     self.screen.blit(self.__heal['health'][0], (x + ((w / 2 - w_tp / 2) + (i * w_tp)), y - (h_tp * 3)))
        #     self.screen.blit(self.__heal['energy'][0], (x + ((w / 2 - w_tp / 2) + (i * w_tp)), y - (h_tp * 2)))
        self.screen.blit(self.__heal['health'][0], (x + (w / 2 - w_tp / 2), y - (h_tp * 2)))
        ### ----- Счётчик __COUNT_FOX для анимации ----------------------------------------------------------------- ###
        self.__COUNT_FOX += 1

    def draw_bush(self): # РИСУЕМ РАСТЕНИЯ;
        ### ----- __COUNT_BUSH отвечает за смену изображения (анимация bush) --------------------------------------- ###
        if self.__COUNT_BUSH >= len(self.__bush['bush']):
            self.__COUNT_BUSH = 0
        ### ----- self.__imgs необходим для определения размера изображения ---------------------------------------- ###
        w, h = self.__SIZE[self.__NUM_L_BUSH]
        ### ----- Отрисовка различных анимаций bush ---------------------------------------------------------------- ###
        self.screen.blit(self.__bush['bush'][self.__COUNT_BUSH], (0, self.h - h))
        ### ----- Счётчик __COUNT_BUSH для анимации ---------------------------------------------------------------- ###
        self.__COUNT_BUSH += 1

    def fox_move__left(self): # ДВИЖЕНИЕ foxi ВЛЕВО;
        ### ----- Определяем, в какую сторону повёрнута foxi [ВЛЕВО] ----------------------------------------------- ###
        self.__FOX_FLIP = True
        ### ----- Устанавливаем анимацию foxi [ 0 == идёт ] -------------------------------------------------------- ###
        self.ANIMATION = 0
        ### ----- Счётчики для определения, повернулась ли foxi [СЛЕВА - НАПРАВО] ---------------------------------- ###
        self.__FOX_FLIP_L += 1
        self.__FOX_FLIP_R  = 0
        ### ----- ДВИЖЕНИЕ foxi ВЛЕВО ------------------------------------------------------------------------------ ###
        self.x -= 25

    def fox_move_right(self): # ДВИЖЕНИЕ foxi ВПРАВО;
        ### ----- Определяем, в какую сторону повёрнута foxi [ВПРАВО] ---------------------------------------------- ###
        self.__FOX_FLIP = False
        ### ----- Устанавливаем анимацию foxi [ 0 == идёт ] -------------------------------------------------------- ###
        self.ANIMATION = 0
        ### ----- Счётчики для определения, повернулась ли foxi [СПРАВА - НАЛЕВО] ---------------------------------- ###
        self.__FOX_FLIP_L  = 0
        self.__FOX_FLIP_R += 1
        ### ----- ДВИЖЕНИЕ foxi ВПРАВО ----------------------------------------------------------------------------- ###
        self.x += 25

    def fox_move____up(self): # ДВИЖЕНИЕ foxi ВВЕРХ;
        ### ----- Если foxi уже сидит, то поднимаем её ------------------------------------------------------------- ###
        if self.ANIMATION == 2:
            self.ANIMATION = 0
            return True
        ### ----- Устанавливаем анимацию foxi [ 2 == сидит ] ------------------------------------------------------- ###
        self.ANIMATION = 2

    def fox_move__down(self): # ДВИЖЕНИЕ foxi ВВЕРХ;
        ### ----- ДВИЖЕНИЕ foxi ВВЕРХ [ПРЫЖОК] --------------------------------------------------------------------- ###
        self.y -= 30