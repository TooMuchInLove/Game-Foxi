# -*- coding: utf-8 -*-

import sys
import pygame as pg


class MenuApp:
    def __init__(self, _screen, _w, _h, _colors, _menu):
        self.screen = _screen
        self.w      = _w
        self.h      = _h
        self.COLORS = _colors
        self.menu   = _menu
        self.style  = pg.font.SysFont('Consolas', 35)

    def draw_menu(self): # РИСУЕМ МЕНЮ;
        ### ----- Список позиций пунктов МЕНЮ [ x, y, width, height ] ---------------------------------------------- ###
        self.pos = []
        ### ----- Отрисовываем ФОН --------------------------------------------------------------------------------- ###
        pg.draw.rect(self.screen, self.COLORS[5], (0, 0, self.w, self.h))
        ### ----- Получаем координаты МЫШИ ------------------------------------------------------------------------- ###
        x, y = pg.mouse.get_pos()
        ### ----- Формируем компоненты МЕНЮ ------------------------------------------------------------------------ ###
        for i in range(len(self.menu)):
            text = self.style.render(self.menu[i][1], True, self.COLORS[2])
            if self.menu[i][0] == 0:
                text = self.style.render(self.menu[i][1], True, self.COLORS[0])
            self.pos += [[  # [ x, y, width, height ]
                (self.w - text.get_size()[0]) / 2,
                (self.h - text.get_size()[1] * len(self.menu)) / 2 + i * (text.get_size()[1] + 5),
                text.get_size()[0],
                text.get_size()[1]
            ]]
            ### ----- Определяем, находится ли курсор в зоне МЕНЮ -------------------------------------------------- ###
            if self.pos[i][0] <= x <= self.pos[i][0] + self.pos[i][2] and \
                    self.pos[i][1] <= y <= self.pos[i][1] + self.pos[i][3] and self.menu[i][0] != 0:
                text = self.style.render(self.menu[i][1], True, self.COLORS[1])
            self.screen.blit(text, (self.pos[i][0], self.pos[i][1]))

    def get_position_mouse_for_menu(self): # ОПРЕДЕЛЯЕМ ПОПАДАНИЕ ПО ПУНКТАМ МЕНЮ;
        ### ----- Получаем координаты МЫШИ ------------------------------------------------------------------------- ###
        x, y = pg.mouse.get_pos()
        ### ----- Определяем, находится ли курсор в зоне пунктов МЕНЮ ---------------------------------------------- ###
        for i in range(len(self.menu)):
            if self.pos[i][0] <= x <= self.pos[i][0] + self.pos[i][2] and \
                    self.pos[i][1] <= y <= self.pos[i][1] + self.pos[i][3]:
                ### ----- Убираем из меню всё ненужное ------------------------------------------------------------- ###
                if len(self.menu) > 3:
                    self.menu = self.menu[:3]
                    return False
                ### ----- Выходим из игры -------------------------------------------------------------------------- ###
                if self.menu[i][0] == 2:
                    pg.quit()
                    sys.exit()
        return True