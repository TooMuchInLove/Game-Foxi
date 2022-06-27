# -*- coding: utf-8 -*-

import sys
import pygame as pg
from foxi   import FoxApp
from menu   import MenuApp
from button import ButtonApp


FPS          = 100      # Отрисовка каждые 0.1 сек;
PAUSE        = False    # Ставим игру на паузу;
RUNNING_GAME = True     # Запуск игры;
MENU         = True     # Вызов меню игры;
INCREASE     = 4        # Увеличиваем объекты в X раз(а);
WIDTH  = 290 * INCREASE # Ширина рабочего окна;
HEIGHT = 130 * INCREASE # Высота рабочего окна;
ANIMATION_FOX = 0       # Смена анимации foxi;
NAME_DIR_IMG  = 'imgs'  # РАСПОЛОЖЕНИЕ КАРТИНОК (директория);

NAME_DIR_BTN = { # СЛОВАРЬ НАЗВАНИЙ ДИРЕКТОРИЙ (buttons);
    'BG'  : (NAME_DIR_IMG, 'background'), # 1 dir
    'BTN' : (NAME_DIR_IMG, 'btn',
                ['bg', 'help', 'help1', 'help2', 'left', 'ok', 'right', 'close'], # PACK 1
                ['left', 'ok', 'right', 'close']), # PACK 2
}

NAME_DIR_FOX = { # СЛОВАРЬ НАЗВАНИЙ ДИРЕКТОРИЙ (foxi);
    'F'   : (NAME_DIR_IMG, 'foxi', ['move', 'sleep', 'stop', 'flip_left_or_right', 'stop_to_sleep']), # 5 dir
    'TP'  : (NAME_DIR_IMG, 'top_panel', ['health', 'energy']), # 2 dir
    'BSH' : (NAME_DIR_IMG, 'bush', ['bush']), # 1 dir
}

IMG_SIZE_BTN = ( # КОРТЕЖ РАЗМЕРОВ ИЗОБРАЖЕНИЙ (buttons);
    ( 8 * INCREASE,  8 * INCREASE), # 00. btn  bg, help [ 17x20 ]
    (12 * INCREASE,  9 * INCREASE), # 01. btn  close, left, ok, right
    #( 8 * INCREASE,  8 * INCREASE), # 00. btn  close [ 8x7 ]
)

IMG_SIZE_FOX = ( # КОРТЕЖ РАЗМЕРОВ ИЗОБРАЖЕНИЙ (foxi, bush);
    (39 * INCREASE, 33 * INCREASE), # 00. foxi move
    (48 * INCREASE, 19 * INCREASE), # 01. foxi sleep              [ 39x19 ], [ 48x19 ]
    (39 * INCREASE, 33 * INCREASE), # 02. foxi stop               [ 35x29 ]
    (39 * INCREASE, 33 * INCREASE), # 03. foxi flip_left_or_right [ 32x33 ]
    (39 * INCREASE, 33 * INCREASE), # 04. foxi stop_to_sleep      [ 39x33 ]
    ( 7 * INCREASE,  6 * INCREASE), # 05. health & energy
    (75 * INCREASE, 77 * INCREASE), # 06. bush
)

PALETTE = ( # ПАЛИТРА ЦВЕТОВ;
    (  0, 200,   0), # 0. Ярко-зелёный
    (153, 154, 153), # 1. Хмуро-серый
    (255, 255, 255), # 2. Белый
    (153, 102,  52), # 3. Светло-коричневый
    (101,  51,   0), # 4. Тёмно-коричневый
    ( 26,  26,  26), # 5. Чёрно-сероватый
    (  0,   0,   0), # 6. Чёрный
    (250, 239,   4), # 7. Жёлтый
)

LIST_MENU = ( # ПУНКТЫ МЕНЮ;
    (0, 'Foxi'),
    (1, 'Start game'),
    (2, 'Exit game'),
    (3, 'Test'),
    (4, 'Test'),
)

if __name__ == '__main__':
    pg.init() # Инициализация
    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE) # Создаём окно
    pg.display.set_caption('Foxi') # Название окна
    pg.display.set_icon(pg.image.load(NAME_DIR_IMG+'/foxi.ico'))

    menu       = MenuApp(screen, WIDTH, HEIGHT, PALETTE, LIST_MENU)
    foxi       = FoxApp(screen, WIDTH, HEIGHT, NAME_DIR_FOX, IMG_SIZE_FOX)
    btns       = ButtonApp(screen, WIDTH, HEIGHT, NAME_DIR_BTN, IMG_SIZE_BTN)
    BACKGROUND = pg.transform.scale(pg.image.load(NAME_DIR_IMG+'/background/bg1.png'), (WIDTH, HEIGHT))

    while RUNNING_GAME: # Запуск игры
        #print(pg.display.get_window_size())
        #w, h = pg.display.get_window_size()
        #print(w % WIDTH)
        #print(HEIGHT * (WIDTH / HEIGHT))
        #BACKGROUND = pg.transform.scale(pg.image.load('foxi/bg.png'), (w, h - (WIDTH / HEIGHT)))

        pg.time.delay(FPS)
        screen.fill(PALETTE[6])
        screen.blit(BACKGROUND, (0, 0))

        if ANIMATION_FOX >=  1: foxi.ANIMATION = 2 #  1 iter == 0.1 сек
        if ANIMATION_FOX >= 48: foxi.ANIMATION = 4 # 48 iter == 4.8 сек
        if ANIMATION_FOX >= 50: foxi.ANIMATION = 1 # 50 iter == 5.0 сек
        ANIMATION_FOX += 1

        for event in pg.event.get(): # События
            if event.type == pg.QUIT: # Закрытие окна
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEMOTION: # Движение курсора мыши;
                # btns.get_position_mouse_for_btn('mouse_hover')
                pass
            elif event.type == pg.MOUSEBUTTONUP: # Отпускание кнопки мыши;
                if event.button == 1: # ЛКМ
                    # btns.get_position_mouse_for_btn('mouse____up')
                    pass
            elif event.type == pg.MOUSEBUTTONDOWN: # Нажатие кнопки мыши;
                if event.button == 1: # ЛКМ
                    # if MENU: MENU = menu.get_position_mouse_for_menu()
                    # else: btns.get_position_mouse_for_btn('mouse__down')
                    btns.get_position_mouse_for_btn('mouse__down')
            elif event.type == pg.KEYDOWN: # | K_LEFT | K_RIGHT | K_UP | K_DOWN | K_SPACE |
                if event.key == pg.K_UP:
                    foxi.fox_move____up()
                    ANIMATION_FOX = 0
                else: pass
            else: pass

        KEY_PRESSED = pg.key.get_pressed() # ЗАЖАТИЕ КЛАВИШИ;
        if   KEY_PRESSED[pg.K_LEFT]:
            if foxi.ANIMATION != 1:
                foxi.fox_move__left()
                ANIMATION_FOX = 0
            else: pass
        elif KEY_PRESSED[pg.K_RIGHT]:
            if foxi.ANIMATION != 1:
                foxi.fox_move_right()
                ANIMATION_FOX = 0
            else: pass
        else: pass

        # if MENU:
        #     menu.draw_menu() # Рисуем меню
        # else:
        foxi.draw_foxi()
        # foxi.draw_bush()
        btns.draw_btns()
        pg.display.update() # Обновляем рабочий экран
    pg.quit()
