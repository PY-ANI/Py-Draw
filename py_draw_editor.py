# from threading import Thread

from pydraw_utility import *


class Tool_bar():
    def __init__(self, window:pg.Surface, window_size:tuple[int,int], window_pos:tuple[int,int]) -> None:
        self.window = window
        self.toolbar_screen = pg.Surface(window_size)
        self.overlay_surface = pg.Surface((46,46), pg.SRCALPHA)
        self.overlay_surface.fill((200,200,200))
        self.overlay_surface.convert()

        self.toolbar_rect = self.toolbar_screen.get_rect(topleft=window_pos)
        self.screen_size = pg.math.Vector2(window_size)

        self.icon_dict = {}
        self.tool_dict = {}
        self.button_dict = {}
        self.selected_tool = None
        
    def create_tools(self):
        self.tool_dict[0] = pencil_tool(0, (46,46), (2+48*0,100), self.icon_dict["pen"])
        self.tool_dict[1] = erase_tool(1, (46,46), (2+48*1,100), self.icon_dict["erase"])
        # self.tool_dict[2] = tool((46,46), (2+48*2,100), self.icon_dict["shapes"])

    def create_buttons(self):
        self.button_dict[0] = button(1,2,"EXPORT")
        self.button_dict[1] = button(1,32,"IMPORT")
        self.button_dict[2] = button(1,62,"NEW")

    def draw_toolbar(self):
        self.window.blit(self.toolbar_screen, self.toolbar_rect)
        self.toolbar_screen.fill((60,60,60))

        if self.selected_tool:
            pg.draw.rect(self.toolbar_screen, (220,220,220), self.selected_tool.rect, 2)
            self.selected_tool.draw_tab(self.toolbar_screen)


class Editor_screen():
    def __init__(self, window:pg.Surface, window_size:tuple[int,int], window_pos:tuple[int,int]) -> None:
        self.window = window
        self.editor_screen = pg.Surface(window_size)
        self.editor_rect = self.editor_screen.get_rect(topleft=window_pos)
        self.screen_size = pg.math.Vector2(window_size)
        self.editor_screen.fill(attribute_value_dict['secondary-color'])


    def draw_editor(self):
        self.window.blit(self.editor_screen, self.editor_rect)


class Editor(Editor_screen, Tool_bar):
    def __init__(self, window: pg.Surface, window_size: tuple[int, int]) -> None:
        self.toolbar_size = (200, window_size[1])
        self.editor_size = (window_size[0]-200, window_size[1])
        
        Editor_screen.__init__(self, window, self.editor_size, (0,0))
        Tool_bar.__init__(self, window, self.toolbar_size, self.editor_rect.topright)
        
        load_icons(self.icon_dict)
        self.create_tools()
        self.create_buttons()


        self.selected_tool = self.tool_dict[0]

        self.mouse_pos = (0,0)
        self.rel_mouse_pos = (0,0)
        self.mouse_pressed = None
        self.mouse_click = None
        self.buffer = []

        self.startup = 4

        self.fps_count = 0
        self.initial_time = time()

        self.font_surf = pg.font.SysFont("monospace", 20)


    def update_cursor(self):
        if self.toolbar_rect.collidepoint(self.mouse_pos):
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
        else:
            pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_CROSSHAIR)

    def draw_trail(self):
        if self.buffer.__len__() > 2:
            pg.draw.lines(self.window, (0,0,0), False, self.buffer, 2)
            pg.draw.lines(self.window, (255,255,255), False, self.buffer, 1)

    def update_utildata(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_pressed = pg.mouse.get_pressed(3)
        self.mouse_click = pg.event.get(pg.MOUSEBUTTONDOWN)
        self.rel_mouse_pos = (self.mouse_pos[0] - self.toolbar_rect.x, self.mouse_pos[1])
    
    def draw_buttons(self):
        for i, btn in self.button_dict.items():
            if btn.rect.collidepoint(self.rel_mouse_pos):
                btn.surface.set_alpha(100)

                if self.mouse_click and self.mouse_click[0].button == 1:
                    if i == 1: self.editor_screen = import_data() or self.editor_screen
                    elif i == 2: self.editor_screen.fill(attribute_value_dict["secondary-color"])
                    else: export_data(self.editor_screen)
                    self.startup=2
            else:
                btn.surface.set_alpha(80)

            btn.draw(self.toolbar_screen)

    def draw_tools(self):
        for Tool in self.tool_dict.values():
            if Tool.rect.collidepoint(self.rel_mouse_pos):
                self.toolbar_screen.blit(self.overlay_surface, Tool.rect, special_flags = pg.BLEND_RGB_MULT)

                if self.mouse_click and self.mouse_click[0].button == 1:
                    self.selected_tool = Tool
                    list(map(lambda x: x.draw(Tool.tab_surface), Tool.widgets))

            Tool.draw(self.toolbar_screen)


    def run(self):

        self.update_cursor()
        self.update_utildata()

        if self.editor_rect.collidepoint(self.mouse_pos) or self.startup:
            self.draw_editor()

            if self.selected_tool:
                if self.mouse_pressed[0]:
                    if self.selected_tool.id == 0:
                        self.selected_tool.tool_ability(self.editor_screen, self.buffer)
                    elif self.selected_tool.id == 1:
                        self.draw_trail()
                else:
                    if self.selected_tool.id == 1:
                        self.selected_tool.tool_ability(self.editor_screen, self.buffer)
            
            if self.mouse_pressed[2]: self.editor_screen.fill(attribute_value_dict['secondary-color'])
            
            if self.mouse_pressed[0]:
                self.buffer.append(self.mouse_pos)
            else:
                self.buffer.clear()
        
        if self.toolbar_rect.collidepoint(self.mouse_pos) or self.startup:
            self.draw_toolbar()
            self.draw_buttons()
            self.draw_tools()
            
            if (self.mouse_click and self.mouse_click[0].button == 1) or self.startup:
                if self.selected_tool.tab_rect.collidepoint(self.rel_mouse_pos) or self.startup:
                    shifted_mouse_pos = self.rel_mouse_pos[0]-self.selected_tool.tab_rect.x , self.rel_mouse_pos[1]-self.selected_tool.tab_rect.y
                    for widget in self.selected_tool.widgets:
                        if widget.detect_click(shifted_mouse_pos): continue
                        widget.draw(self.selected_tool.tab_surface)



        if self.startup: 
            self.startup -= 1
        





        #fps
        # self.fps_count = 1//(time()-self.initial_time)
        # self.initial_time = time()

        # self.window.blit(self.font_surf.render(str(self.fps_count), False, (0,250,0), (250,250,250)), (1100, 10))