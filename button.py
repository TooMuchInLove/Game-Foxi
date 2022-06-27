# -*- coding: utf-8 -*-

import pygame as pg
from os import listdir


class ButtonApp:
    def __init__(self, _screen, _w, _h, _namedir, _imagesize):
        self.screen = _screen
        self.w      = _w
        self.h      = _h
        __NAME_DIR  = _namedir
        __SIZE_IMG  = _imagesize

        ### ----- ПОДГРУЖАЕМ АНИМАЦИИ КНОПОК (формируем словарь со всеми анимациями) ------------------------------- ###
        self.__BTN_1 = {}
        self.__BTN_2 = {}
        img_dir, obj_dir = __NAME_DIR['BTN'][0], __NAME_DIR['BTN'][1]
        for item in __NAME_DIR['BTN'][2]: # СПИСОК ДИРЕКТОРИЙ В ДИРЕКТОРИИ - btn/[bg, help];
            self.__BTN_1[item] = [
                pg.transform.scale(
                    pg.image.load('%s/%s/%s/%s.png' % (img_dir, obj_dir, item, img)), (__SIZE_IMG[0])
                ) for img in range(1, len(listdir(path='%s/%s/%s/' % (img_dir, obj_dir, item))) + 1)
            ]
        for item in __NAME_DIR['BTN'][3]: # СПИСОК ДИРЕКТОРИЙ В ДИРЕКТОРИИ - btn/[close, left, ok, right];
            self.__BTN_2[item] = [
                pg.transform.scale(
                    pg.image.load('%s/%s/%s/%s.png' % (img_dir, obj_dir, item, img)), (__SIZE_IMG[0])
                ) for img in range(1, len(listdir(path='%s/%s/%s/' % (img_dir, obj_dir, item))) + 1)
            ]
        ### -------------------------------------------------------------------------------------------------------- ###
        ### ----- ПОДГРУЖАЕМ ФОН (формируем список со всеми background) -------------------------------------------- ###
        self.__bg = []
        img_dir, obj_dir = __NAME_DIR['BG'][0], __NAME_DIR['BG'][1]
        for i in range(1, len(listdir(path='%s/%s/' % (img_dir, obj_dir))) + 1):
            self.__bg.append(
                pg.transform.scale(pg.image.load('%s/%s/bg%s.png' % (img_dir, obj_dir, i)), (self.w / 3, self.h / 3))
            )
        ### -------------------------------------------------------------------------------------------------------- ###
        self.__CUT        = len(self.__BTN_1)             # СРЕЗ для списка координат кнопок;
        self.__EVENT_BTN  = (__NAME_DIR['BTN'][2][0], 0)  # ОПРЕДЕЛЯЕМ КАКАЯ КНОПКА НАЖАТА;
        self.__BTN_CLICK  = [False for i in self.__BTN_1] # ОПРЕДЕЛЯЕМ, НАЖАТА ЛИ КНОПКА;
        self.__BTN_CLICK += [False for i in self.__BTN_2] # ОПРЕДЕЛЯЕМ, НАЖАТА ЛИ КНОПКА;
        self.__list_pos_btn   = []                        # СПИСОК КОРТЕЖЕЙ (x, y) == КООРДИНАТЫ КНОПОК;
        self.__BLOCK_POS_PACK = False                     # ФЛАГ ПОЗВОЛЯЕТ ФОРМИРОВАТЬ СПИСОК КООРДИНАТ ОДИН РАЗ;

    def get_position_mouse_for_btn(self, _event):
        ### ----- Получаем координаты МЫШИ ------------------------------------------------------------------------- ###
        x, y = pg.mouse.get_pos()
        ### ----- Определяем, находится ли курсор в зоне КНОПКИ ---------------------------------------------------- ###
        iter = 0
        for item in self.__list_pos_btn[:self.__CUT]:
            size_w = self.__BTN_1[item[2]][0].get_size()[0] # Ширина изображения;
            size_h = self.__BTN_1[item[2]][0].get_size()[1] # Высота изображения;
            if item[0] <= x <= item[0] + size_w and item[1] <= y <= item[1] + size_h:
                #if   _event == 'mouse_hover': self.EVENT_BTN = (item[2], 1)
                #elif _event == 'mouse__down': self.EVENT_BTN = (item[2], 2)
                #elif _event == 'mouse____up': self.EVENT_BTN = (item[2], 0)
                #else: self.EVENT_BTN = (item[2], 0)
                self.__BTN_CLICK[iter]   = True
                self.__EVENT_BTN         = (item[2], 2)
            else: self.__BTN_CLICK[iter] = False
            iter += 1
        iter = 0
        for item in self.__list_pos_btn[self.__CUT:]:
            size_w = self.__BTN_2[item[2]][0].get_size()[0] # Ширина изображения;
            size_h = self.__BTN_2[item[2]][0].get_size()[1] # Высота изображения;
            if item[0] <= x <= item[0] + size_w and item[1] <= y <= item[1] + size_h:
                self.__BTN_CLICK[iter + self.__CUT]   = True
                self.__EVENT_BTN                      = (item[2], 1)
            else: self.__BTN_CLICK[iter + self.__CUT] = False
            iter += 1
        print(self.__BTN_CLICK, ' --- ', self.__EVENT_BTN)

    def draw_btns(self): # РИСУЕМ КНОПКИ ИНТЕРФЕЙСА;
        i = 0
        border = 5
        name_btn, name_anm = self.__EVENT_BTN
        for key in self.__BTN_1.keys():
            x, y = border + (i * (self.__BTN_1[key][0].get_size()[0] + border)), border
            ### ----- Формируем список координат кнопок self.__list_pos_btn ---------------------------------------- ###
            if not self.__BLOCK_POS_PACK:
                self.__list_pos_btn.append((x, y, key))
            ### ----- Определяем, какая конкретно нажата кнопка и изменяем её событие. Рисуем кнопки --------------- ###
            if self.__BTN_CLICK[i]:
                self.screen.blit(self.__BTN_1[name_btn][name_anm], (x, y))
            else: self.screen.blit(self.__BTN_1[key][0], (x, y))
            ### ----- Выводим объекты background, для выбора фона -------------------------------------------------- ###
            if name_btn == 'bg' and self.__BTN_CLICK[i] == True:
                ### ----- PanelApp(self.screen, self.w, self.h, self.__bg, self.__BTN_2).draw_panel()
                x_fon = x
                y_fon = (border * 2) + self.__BTN_1[key][0].get_size()[1]
                w_fon = (border * 2) + self.__bg[0].get_size()[0]
                h_fon = (border * 2) + self.__bg[0].get_size()[1]
                pg.draw.rect(self.screen, 'black', (x_fon, y_fon, w_fon, h_fon))
                self.screen.blit(self.__bg[0], (x_fon + border, y_fon + border))

                count = name_anm if self.__BTN_CLICK[i + self.__CUT] else 0
                self.screen.blit(self.__BTN_2['close'][count], (x_fon + w_fon, y_fon))

                # if self.__BTN_CLICK[i + self.__CUT]:
                #     self.screen.blit(self.__BTN_2['close'][name_anm], (x_fon + w_fon, y_fon))
                # else: self.screen.blit(self.__BTN_2['close'][0], (x_fon + w_fon, y_fon))

                j = 0
                for key in self.__BTN_2.keys():
                    _x = x_fon + (border + (j * (self.__BTN_2[key][0].get_size()[0] + border)))
                    _y = y_fon + h_fon + border
                    ### ----- Формируем список координат кнопок self.__list_pos_btn -------------------------------- ###
                    if not self.__BLOCK_POS_PACK:
                        self.__list_pos_btn.append((_x, _y, key))
                    #self.__list_pos_btn.append((_x, _y, key))
                    if self.__BTN_CLICK[j + self.__CUT]:
                        self.screen.blit(self.__BTN_2[name_btn][name_anm], (_x, _y))
                    else: self.screen.blit(self.__BTN_2[key][0], (_x, _y))
                    #if name_btn == 'right' and self.__BTN_CLICK[i] == True:
                    #    self.__BTN_CLICK[i] = True
                    #    self.__BTN_CLICK[j] = True
                    j += 1
                #
                #
                #
            i += 1
        self.__BLOCK_POS_PACK = True


class PanelApp:
    def __init__(self, _screen, _w, _h, _fon, _btns):
        self.screen = _screen
        self.w      = _w
        self.h      = _h
        self.__bg   = _fon
        self.__BTNS = _btns
        self.__BORDER = 5
        self.__SIZE_W = self.__bg[0].get_size()[0]
        self.__SIZE_H = self.__bg[0].get_size()[1]
        self.__X      = self.__BORDER
        self.__Y      = self.__SIZE_H / 2
        self.__W      = (self.__BORDER * 2) + self.__SIZE_W
        self.__H      = (self.__BORDER * 2) + self.__SIZE_H

    def draw_panel(self): # РИСУЕМ ПАНЕЛЬ С ВЫБОРОМ ФОНА;
        pg.draw.rect(self.screen, 'black', (self.__X, self.__Y, self.__W, self.__H))
        self.screen.blit(self.__bg[0], (self.__X + self.__BORDER, self.__Y + self.__BORDER))

    def get_position_btn(self) -> list:
        iter = 0
        list_pos_btn = []
        for key in self.__BTNS.keys():
            x = self.__BORDER + (iter * (self.__BTNS[key][0].get_size()[0] + self.__BORDER))
            x = x + (self.__SIZE_W / 2 - self.__BTNS[key][0].get_size()[0] / 2)
            y = self.__Y + self.__H + self.__BORDER
            list_pos_btn += [(x, y, key)]
            iter += 1
        return list_pos_btn