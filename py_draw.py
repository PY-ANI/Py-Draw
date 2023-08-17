import pygame as pg

# from py_draw_viewer import viewer
from py_draw_editor import Editor

window_dimension = (1200,700)

if __name__ == "__main__":
    
    pg.init()

    win = pg.display.set_mode(window_dimension)

    editor = Editor(win,window_dimension)

    pg.display.set_caption("PY DRAW | Editor")
    pg.display.set_icon(pg.image.load("icon.png").convert_alpha())

    clock = pg.time.Clock()
    
    fps = 200
    
    while not pg.event.get(pg.QUIT):
        
        # clock.tick(fps)

        editor.run()

        pg.display.flip()

    pg.quit()