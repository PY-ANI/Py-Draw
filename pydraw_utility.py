import pygame as pg
from tkinter.filedialog import askopenfile, asksaveasfilename
from time import time, sleep
import os


attribute_value_dict = {
    "width": 2,
    "primary-color": (0,0,0),
    "secondary-color": (250,250,250),
}

class button():
    def __init__(self,x,y,btn_name):
        self.text_surf = pg.font.SysFont("comicsans", 20, True).render(btn_name,True,(240,240,240))
        self.surface = pg.Surface((198,self.text_surf.get_height()),pg.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=(x,y))

        self.surface.fill((150,150,150))
        self.surface.set_alpha(80)
        self.surface.blit(self.text_surf,(4,0))
        self.surface.convert_alpha()
    
    def draw(self,win):
        win.blit(self.surface, self.rect)

class width_widget():
    def __init__(self, x, y) -> None:
        self.font_surf = pg.font.SysFont("comicsans", 30, True)
        self.left_button = self.font_surf.render("-", True, (255,255,255), (100,100,100))
        self.right_button = self.font_surf.render("+", True, (255,255,255), (100,100,100))
        self.left_button_rect = self.left_button.get_rect(topleft=(x,y))
        self.right_button_rect = self.right_button.get_rect(topright=(196,y))
        self.text_display_rect = pg.Rect(self.left_button_rect.right,y,self.right_button_rect.x-self.right_button_rect.w, self.left_button_rect.h)
    
    def draw(self, win):
        win.blit(self.left_button, self.left_button_rect)
        pg.draw.rect(win, (240,240,240), self.text_display_rect)
        win.blit(self.font_surf.render(str(attribute_value_dict["width"]),False,(50,50,50)), (self.text_display_rect.centerx, self.text_display_rect.y))
        win.blit(self.right_button, self.right_button_rect)
    
    def detect_click(self,pos):
        if self.left_button_rect.collidepoint(pos) and attribute_value_dict["width"] > 1: attribute_value_dict["width"] -= 1
        elif self.right_button_rect.collidepoint(pos) and attribute_value_dict["width"] < 10: attribute_value_dict["width"] += 1
        else: return True

class color_picker_widget():
    def __init__(self,x,y):
        self.rect = pg.Rect(x,y,196,200)

        self.colors = {
            0:{0:attribute_value_dict["primary-color"], 1:attribute_value_dict["secondary-color"]},
            1:{0:(255,0,0), 1:(0,255,0)},
            2:{0:(0,0,255), 1:(255,255,0)},
            3:{0:(0,255,255), 1:(255,0,255)},
            4:{0:(128,128,128), 1:(128,0,0)},
            5:{0:(173,255,47), 1:(127,255,212)},
        }
    
    def draw(self,win):
        for y, row in self.colors.items():
            for x, color in row.items():
                pg.draw.rect(win,color,(self.rect.x+42*x,self.rect.y+42*y,40,40))

    def detect_click(self,pos):
        x, y = pos[0]//41, (pos[1]-self.rect.y)//41
        try:
            attribute_value_dict['primary-color'] = self.colors[y][x]
        except:
            ...

class tool():
    def __init__(self, size:tuple[int, int], pos:tuple[int, int], icon:pg.Surface) -> None:
        self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
        self.tab_surface = pg.Surface((196, 300))
        self.tab_surface.fill((50,50,50))
        self.tab_surface.convert()
        self.tab_rect = self.tab_surface.get_rect(topleft=(2,self.rect.bottom+4))
        self.icon = icon
        self.widgets = []

    
    def draw(self, win):
        win.blit(self.icon, (self.rect.x+2, self.rect.y+2))

    def setup_surface(self):
        list(map(lambda x: x.draw(self.tab_surface), self.widgets))

class pencil_tool(tool):
    def __init__(self, id, size: tuple[int, int], pos: tuple[int, int], icon: pg.Surface) -> None:
        super().__init__(size, pos, icon)
        self.id = id

        self.widgets.append(width_widget(0,2))
        self.widgets.append(color_picker_widget(0,46))

        self.setup_surface()

    def tool_ability(self, win, buffer):
        if buffer.__len__() > 2:
            pg.draw.lines(win, attribute_value_dict["primary-color"], False, buffer, attribute_value_dict["width"])
    
    def draw_tab(self, win):
        win.blit(self.tab_surface, self.tab_rect, special_flags = pg.BLEND_RGB_ADD)

class erase_tool(tool):
    def __init__(self, id, size: tuple[int, int], pos: tuple[int, int], icon: pg.Surface) -> None:
        super().__init__(size, pos, icon)
        self.id = id

    def tool_ability(self, win, buffer):
        if buffer.__len__() > 2:
            pg.draw.polygon(win, attribute_value_dict["secondary-color"], buffer, 0)
    
    def draw_tab(self, win):
        win.blit(self.tab_surface, self.tab_rect, special_flags = pg.BLEND_RGB_ADD)


def load_icons(icon_dict):
    for icon in os.listdir("icons/"):
        if ".png" in icon:
            icon_dict[icon[:-4]] = pg.transform.smoothscale(pg.image.load("icons/"+icon).convert_alpha(), (40,40))

def export_data(surf):
    file = asksaveasfilename()
    try:
        if file: pg.image.save(surf,file)
    except:
        ...

def import_data():
    with askopenfile('r',filetypes=[(".png","PNG"),(".jpg","JPEG")], defaultextension=".png") as file:
        try:
            if file: return pg.image.load(file).convert()
        except:
            ...