import random
import time

import pygameextra as pe
pe.init((0, 0))
board = pe.Surface(pe.display.get_size())

drawing_mode = 'chalk'
chalk_amount = 10
chalk_butter_amount = 1
spread = 5
two_finger_as_eraser = True

def draw_mode(mode: str) -> None:
    global drawing_mode
    drawing_mode = mode

def disperse(place: tuple) -> None:
    rx, ry = spread, spread
    while rx+ry > spread:
        rx, ry = random.randint(-spread, spread), random.randint(-spread, spread)
    return place[0] + rx, place[1] + ry

def chalk_draw(place: tuple) -> None:
    if sum(board.get_at(place)) > 512: return
    for _ in range(chalk_amount):
        pe.draw.circle(pe.colors.white, disperse(place), 1, 0, board)
    for _ in range(chalk_butter_amount):
        pe.draw.circle(pe.colors.darkgray, disperse(place), 1, 0, board)

def eraser_draw(place1: tuple, place2: tuple):
    pe.draw.line(pe.colors.verydarkgray, place1, place2, int(pe.display.get_width()*.025), board)

def handle_events() -> None:
    pe.event.quitCheckAuto()
    pe.mouse.fingersupport.handle_finger_events()

pe.display.make((0, 0), "Chalk board", pe.display.DISPLAY_MODE_FULLSCREEN)
pen_down_time = time.time()
board_mud = True

while True:
    [handle_events() for pe.event.c in pe.event.get()]

    pe.fill.full(pe.colors.verydarkgray)
    pe.display.blit(board)

    pe.button.rect((0, 0, 50, 50), pe.colors.darkgray, pe.colors.gray, action=draw_mode, data='chalk')

    if two_finger_as_eraser and 3 > len(pe.mouse.fingersupport.fingers) > 1:
        eraser_draw(*[[int(v) for v in finger['pos']] for finger in pe.mouse.fingersupport.fingers])
    else:
        for finger in pe.mouse.fingersupport.fingers:
            if finger['pos'][0] <= 100 and finger['pos'][1] <= 50: continue
            if drawing_mode == 'chalk':
                chalk_draw([int(v) for v in finger['pos']])
                board_mud = False
                pen_down_time = time.time()

    # if (not board_mud) and time.time() - pen_down_time > 1:
    #     # board_mud = True
    #     for x in range(0, board.size[0], 1):
    #         for y in range(0, board.size[1], 1):
    #             if sum(c := board.get_at((x,y))) < 512: continue
    #             board.set_at(disperse((x, y)), c)
    #             board.set_at((x, y), (0,0,0,0))

    pe.display.update()