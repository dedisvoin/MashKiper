from api.lib import *
import json

win = Window(size=[1920/2,1080/2], flag=Flags.WINDOW_RESIZE)
datas = DataLoader().Load_from_file('mapcreatordata\mapdatas.data')
LAYERS = []
LAYER_ID = 0
VABOR_LAYER_INDEX = None
GRID = None
END_GRID = None

VABOR_TILE = None
VABOR_TILE_NAME = None

VABOR_OBJ = None
VABOR_OBJ_NAME = None

COLOR_1B = (100,100,130)
COLOR_2B = (170,170,250)
COLOR_3B = (200,200,250)
COLOR_4B = (70,70,90)

COLOR_TRIG = (170,220,250)
COLOR_BARS_BG = (100,100,130)
COLOR_BG = (60,60,80)
COLOR_WHITE = (255,255,255)

COLOR_WINS_BG = (100-10,100-10,130-10)
COLOR_WINS_BORDER = (70,70,90)
COLOR_CLOSE_1 = (220,180,200)
COLOR_CLOSE_2 = (250,130,220)

COLOR_TEXT_INPUT = (100,100,130)
COLOR_TEXT = (80,80,110)
COLOR_GRID = (80,80,110)
LOAD_COLOR = (200,200,230)
LOAD_COLOR_NONE = (200-80,200-80,230-80)
GLOBAL_PRESS_WIN = False
COLOR_TEXT_WHITE = (150,150,180)

ON_THE_BOARD = False

VABOR_GRASSES = []


def get_win_size():
    return win.get_size()

def get_win_center():
    return win.center

class UserHelp:
    def __init__(self, name, text, key) -> None:
        self.name = name
        self.text = text
        self.key = key
        
        self.text_name = Text('arial', 20, self.name, COLOR_TEXT, True).render(self.name, COLOR_TEXT_WHITE)
        self.text_text = Text('arail', 17, self.text, COLOR_WHITE, False).render(self.text, COLOR_WHITE)
        self.text_key = Text('arail', 18, self.text, COLOR_WHITE, True).render(f'press [{self.key}]', COLOR_WHITE)
        
    def render(self, pos, surf):
        width = max(self.text_text.get_width(), self.text_name.get_width())+20
        height = 60
        
        pos = [pos[0]-width/2, pos[1] - height-20]
        Draw.draw_rect(surf, pos, [width, height], COLOR_1B, radius=5)
        Draw.draw_rect(surf, [pos[0]+2, pos[1]+20], [width-4, height-20-2],COLOR_BG, radius=5 )
        
        surf.blit(self.text_name, [pos[0]+3, pos[1]])
        surf.blit(self.text_text, [pos[0]+7, pos[1]+24])
        surf.blit(self.text_key, [pos[0]+7, pos[1]+height-self.text_key.get_height()-5])
        
class Button:
    def __init__(self, sprite: Sprite, scale, clicked = False) -> None:
        self.sprite = copy(sprite)
        self.sprite.scale = scale
        self.pos = [0, 0]
        self.vabor = False
        self.c = clicked
        self.clicked = False
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.click = False
        
    def update(self, pos):
        self.pos = pos
        self.vabor = False
        self.mouse_events.EventsUpdate()
        self.click = False
        if in_rect(self.pos, self.sprite.size, Mouse.pos):
            self.vabor = True
            self.click = self.mouse_events.GetEventById('click')
            
            if self.mouse_events.GetEventById('click'):
                self.clicked = not self.clicked
            
        
    def render(self, surf):
        if not self.vabor:
            Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_1B, radius=8)
        else:
            Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_2B, radius=8, outline=[(255,255,255),2])
        if self.c:
            if self.clicked:
                Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_3B, radius=8, outline=[(255,255,255),3])
        self.sprite.center = [self.pos[0]+self.sprite.size[0]/2,self.pos[1]+self.sprite.size[1]/2]
        self.sprite.render(surf)

class TextButton:
    def __init__(self, text, font_size, size=[200,30], left = False, right = False) -> None:
        self.l = left
        self.r = right
        self.pos = [-1000,1000]
        self.size = size
        
        self.string_text = text
        self.font_size = font_size
        self.text = Text('arial', font_size, self.string_text, (200,200,200), True)
        
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.click = False
        self.clicked = False
        self.vabor = False
        
    def update(self, pos=None):
        if pos is not None:
            self.pos = pos
        self.vabor = False
        self.mouse_events.EventsUpdate()
        self.click = False
        if in_rect(self.pos, self.size, Mouse.pos):
            self.vabor = True
            self.click = self.mouse_events.GetEventById('click')
            
            if self.mouse_events.GetEventById('click'):
                self.clicked = not self.clicked
            
        
    def render(self, surf):
        radius = [8,8,8,8]
        if self.l == True:
            radius[0] = 0
            radius[3] = 0
        if self.r == True:
            radius[1] = 0
            radius[2] = 0
        if not self.vabor:
            Draw.draw_rect(surf, self.pos, self.size, COLOR_1B, radius=radius)
        else:
            Draw.draw_rect(surf, self.pos, self.size, COLOR_2B, radius=radius, outline=[(255,255,255),1])
        
        
        self.text.draw(surf, [self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2], True, self.string_text, (200,200,200))

class TrigerButton:
    def __init__(self, sprite: Sprite, scale, clicked = False, left=False, right=False) -> None:
        self.sprite = copy(sprite)
        self.sprite.scale = scale
        self.pos = [0, 0]
        self.vabor = False
        self.c = clicked
        self.clicked = False
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.l = left
        self.r = right
        
        self.click = False
        
        self.triger = False
        
    def update(self, pos):
        self.pos = pos
        self.vabor = False
        self.mouse_events.EventsUpdate()
        self.click = False
        if in_rect(self.pos, self.sprite.size, Mouse.pos):
            self.vabor = True
            self.click = self.mouse_events.GetEventById('click')
            
            if self.mouse_events.GetEventById('click'):
                self.clicked = not self.clicked
                self.triger = not self.triger
            
        
    def render(self, surf):
        radius = [8,8,8,8]
        if self.l == True:
            radius[0] = 0
            radius[2] = 0
        if self.r == True:
            radius[1] = 0
            radius[3] = 0
        
        
        if not self.vabor:
            Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_1B, radius=radius)
        else:
            Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_2B, radius=radius, outline=[(255,255,255),2])
        
        self.sprite.center = [self.pos[0]+self.sprite.size[0]/2,self.pos[1]+self.sprite.size[1]/2]
        self.sprite.render(surf)
        if self.triger:
            Draw.draw_rect(surf, self.pos, self.sprite.size, COLOR_3B,2, radius=8,)

class Table:
    def __init__(self, size, start_pos, name, resizing=True) -> None:
        self.size = size
        self.start_pos = start_pos
        self.pos = start_pos
        self.bg_color = COLOR_WINS_BG
        self.start_size = copy(size)
        
        self.opened = False
        self.pressed = False
        
        self.string_text = name
        self.text = Text('arial', 20, name, [255,255,255], True)
        
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click1'))
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.press_event, 'press1'))
        
        self.closed_vabor = False
        self.close_rect = [self.pos[0]+self.size[0]-20,self.pos[1]]
        self.cl = False
        self.resizing = resizing
        
        self.sizing_pressed = False
        self.size_resizing = False
        
        self.left_mode = False
        self.right_mode = False
        
    
    def render(self, render_event: None = None, surf = None):
        if self.opened:
            Draw.draw_rect(surf, self.pos, self.size, self.bg_color, radius=5, outline=[COLOR_1B, 1])
            Draw.draw_rect(surf, self.pos, [self.size[0],20], COLOR_WINS_BORDER, radius=(5,5,0,0))
            
            if not self.closed_vabor:
                Draw.draw_rect(surf, [self.pos[0]+self.size[0]-20,self.pos[1]], [20,20], COLOR_CLOSE_1,radius=(0,5,0,0))
            else:
                Draw.draw_rect(surf, [self.pos[0]+self.size[0]-20,self.pos[1]], [20,20], COLOR_CLOSE_2,radius=(0,5,0,0))
            
            self.text.draw(surf, [self.pos[0]+self.size[0]/2, self.pos[1]+10], text=self.string_text,centering=True)
            
            
                
            if self.cl:
                Draw.draw_rect(surf, self.pos, self.size, COLOR_3B,2, radius=(5,5,5,5))
                
            if render_event is not None:
                render_event(self.pos, self.size, surf)
            
            if self.size_resizing:
                Draw.draw_rect(surf, self.pos, self.size, COLOR_3B,2, radius=(5,5,5,5))
            
    def update(self, ms):
        global GLOBAL_PRESS_WIN, ON_THE_BOARD
        
        self.mouse_events.EventsUpdate()
        click = self.mouse_events.GetEventById('click1')
        press = self.mouse_events.GetEventById('press1')
        if Keyboard.key_pressed('q'):
            self.left_mode = False
            self.right_mode = False
            
        
        
        self.close_rect = [self.pos[0]+self.size[0]-20,self.pos[1]]
        self.sizing_rect = [self.pos[0]+self.size[0]-20,self.pos[1]+self.size[1]-20]
        self.closed_vabor = False
        if in_rect(self.close_rect, [20,20], Mouse.pos):
            self.closed_vabor = True
            
            if click:
                self.opened = False
        
        self.cl = False
        if self.opened:
            if in_rect(self.pos, self.size, Mouse.pos):
                GLOBAL_PRESS_WIN = True
                ON_THE_BOARD = True
        if in_rect(self.pos, [self.size[0],20], Mouse.pos) and press:
            self.cl = True
        
        if in_rect(self.pos, [self.size[0],20], Mouse.pos) and click:
            self.pressed = True
        if not press:
            self.pressed = False
            
        
        self.size_resizing = False
        if self.opened:

            if self.pressed:

                self.pos[0]+=ms[0]
                self.pos[1]+=ms[1]
                if Keyboard.key_pressed('w'):
                    if self.pos[0]+self.size[0]/2>win_center[0]:
                        self.right_mode = True
                    else:
                        self.left_mode = True
                    
        
            if in_rect(self.sizing_rect, [20,20], Mouse.pos):
                
                if click:
                    self.sizing_pressed = True
            if not press:
                self.sizing_pressed = False
            
            if self.sizing_pressed and self.resizing:
                self.size_resizing = True
                self.size[0]+=ms[0]
                self.size[1]+=ms[1]
                
        if self.left_mode:
            self.pos[0] = 0
        if self.right_mode:
            self.pos[0] = win_size[0]-self.size[0]

        self.pos[0] = min(max(self.pos[0],0), win.get_size()[0]-self.size[0])
        self.pos[1] = min(max(self.pos[1],0), win.get_size()[1]-self.size[1])
        self.size[0] = max(self.size[0],self.start_size[0])
        self.size[1] = max(self.size[1],self.start_size[1])

class TextInput:
    def __init__(self, size, text) -> None:
        self.size = size
        self.text = ''

        self.bg_color = COLOR_TEXT_INPUT
        self.pos = [0,0]
        self.vabor = False
        self.mouse_events = MouseEventHandler()
        self.mouse_events.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'click'))
        
        self.view_text = Text('arial',20, '',COLOR_WHITE,True)
        self.end_press = None
        self.timer = 0
        
        self.text_val = text
        
        
    def update(self):
        if self.vabor:
            inp = win.press_key
            
            if inp is not None:
                if inp == 'backspace':
                    self.text = self.text[:-1]
                elif inp == 'left shift':
                    self.end_press = inp
                elif inp == 'left ctrl':
                    self.end_press = inp
                else:
                    if self.end_press == 'left shift' and inp=='=':
                        
                        inp = '+' 
                    elif self.end_press == 'left shift' and inp=='9':
                        
                        inp = '(' 
                    elif self.end_press == 'left shift' and inp=='0':
                        
                        inp = ')' 
                        
                    elif self.end_press == 'left shift':
                        inp = inp.upper()
                    if self.end_press == 'left ctrl' and inp == 'v':
                        self.text = paste()
                    else:
                    
                    
                        self.text+=inp
                    self.end_press = None
                
        self.timer+=0.1
        self.mouse_events.EventsUpdate()
        
        
        if self.mouse_events.GetEventById('click'):
            if in_rect(self.pos, self.size, Mouse.pos):
                self.vabor = not self.vabor
            else:
                self.vabor = False
        
        
    def render(self, surf):
        
        Draw.draw_rect(surf, self.pos, self.size, self.bg_color, radius = 5)
        if self.text == '':
            self.view_text.draw(surf, [self.pos[0]+5,self.pos[1]], False, self.text_val, COLOR_TEXT)
        if self.vabor:
            Draw.draw_rect(surf, self.pos, self.size, (200,250,250),1,radius=5 )
        text_surf = self.view_text.render(self.text, COLOR_WHITE, self.size[0]-5)
        surf.blit(text_surf, [self.pos[0]+5,self.pos[1]])
        if self.vabor:
            d = abs(12*sin(self.timer))
            Draw.draw_vline(surf, self.pos[0]+text_surf.get_width()+7, self.pos[1]+d, self.pos[1]+24-d,2, (200,250,250))

class DownTable:
    def __init__(self) -> None:
        self.pos = [0, 0]
        self.buttons_count = 6
        self.buttons_size = 60
        self.btns_scale = 2.5
        self.MOUSE_EH = MouseEventHandler()
        self.MOUSE_EH.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'vabor_tile'))
        
        self.btn_tiles = Button(datas['tiles_btn'],self.btns_scale)
        self.tbl_tiles = Table([230,300],[200,200],'Tiles')
        self.tbl_tiles_load_btn = TextButton('load', 20, [110,25], right = True)
        self.tbl_tiles_select_btn = TextButton('select', 20, [110,25], left = True)
        self.tbl_tiles_load_tb = TextInput([335,25], 'file_path')
        self.tile_name_text = Text('arial',16, '', COLOR_WHITE,True)
        self.tb_help = UserHelp('Tiles', 'Loading and using you tilesheats', 'none')
        
        self.loaded_files = []
        self.loaded_file_tbl = Table([260,400], [0,0], 'Data files', False)
        self.loaded_text = Text('arial',20, color=(0,0,0),bold=True)
        self.small_text = Text('arial',15, color=(0,0,0),bold=True)
        
        self.loaded_tilesheats = []
        self.my_tile_sheats = []
        self.my_tile_sheats_dict = {}
        
        self.btn_places = Button(datas['places_btn'], self.btns_scale)
        self.tbl_places = Table([200,115],[200,200],'Grid create', False)
        self.tile_count_w = TextInput([335,25], 'grid width')
        self.tile_count_h = TextInput([335,25], 'grid height')
        self.tile_grid_create_btn = TextButton('create', 20, [200,25])
        
        self.surfs_bt = Button(datas['surfs_btn'], self.btns_scale)
        self.layares_table = Table([200,300],[0,0],'Layers', True)
        self.layer_add_bt = TextButton('add', 20, [110,25])
        
        self.obj_btn = Button(datas['obj_btn'], self.btns_scale)
        self.obj_table = Table([230,300], [0,0], 'Objects', True)
        self.obj_load_btn = TextButton('load', 20, [110,25])
        self.rendered_objects = []
        self.objects = []
        
        self.save_btn = Button(datas['save_btn'], self.btns_scale)
        self.save_table = Table([300,400],[300,300], 'Save map')
        self.save_button = TextButton('save', 20, [110,25])
        self.saveed_file_name_text_box = TextInput([335,25], 'file_name')
        self.saveed_file_collide_layer_text_box = TextInput([335,25], 'collide_layer')
        
        self.saved_surf = Text('arial',20,'Saved',(20,250,50),True).render('Saved!', (20,250,20))
        self.saved_surf_timer = 0
        
        self.grass_btn = Button(datas['grass_btn'], self.btns_scale)
        self.grass_table = Table([230,300],[300,300],'Grass')
        self.grass_load_btn = TextButton('load', 20, [110,25])
        self.grasses = {}
        self.rendered_grasses = []
        
        
    def update(self, win_size, win_center, mouse_speed):
        global ON_THE_BOARD
        self.size = [(self.buttons_size)*self.buttons_count-10*(self.buttons_count-1), self.buttons_size]
        self.pos = [
            win_center[0]-self.size[0]/2,
            win_center[1]+win_size[1]/2-self.buttons_size-20
        ]
        
        self.btn_tiles.update(pos=[self.pos[0]+5,self.pos[1]+5])
        self.btn_places.update(pos=[self.pos[0]+5+50,self.pos[1]+5])
        self.surfs_bt.update(pos=[self.pos[0]+5+50+50,self.pos[1]+5])
        self.obj_btn.update(pos=[self.pos[0]+5+50+50+50,self.pos[1]+5])
        self.save_btn.update(pos=[self.pos[0]+5+50+50+50+50,self.pos[1]+5])
        self.grass_btn.update(pos=[self.pos[0]+5+50+50+50+50+50,self.pos[1]+5])
        self.tbl_tiles.update(mouse_speed)
        self.tbl_tiles_load_tb.update()
        self.tbl_tiles_load_btn.update()
        self.layer_add_bt.update()
        self.tbl_tiles_select_btn.update()
        self.loaded_file_tbl.update(mouse_speed)
        
        
        self.tbl_places.update(mouse_speed)
        self.layares_table.update(mouse_speed)
        self.obj_table.update(mouse_speed)
        self.save_table.update(mouse_speed)
        self.grass_table.update(mouse_speed)
        self.tile_count_h.update()
        self.tile_count_w.update()
        self.tile_grid_create_btn.update()
        
        if in_rect(self.pos, self.size, Mouse.pos):
            ON_THE_BOARD = True
        
    def load_tile_sheats(self):
        tsh = DataLoader().Load_from_file_tilesheats(self.tbl_tiles_load_tb.text)
        self.loaded_tilesheats = []
        self.my_tile_sheats = []
        for i, tile_sheat_name in enumerate( tsh ):
            tlsh1 = copy(tsh[tile_sheat_name])
            tlsh2 = copy(tsh[tile_sheat_name])
            
            tiles_scale(tlsh1, 5)
            tlsh1.tiles['one'].set_size([40,40])
            self.loaded_tilesheats.append([tile_sheat_name, tlsh1, i+1])
            self.my_tile_sheats.append([i+1,tile_sheat_name, tlsh2])
        
        
        for i, tile_sheat_name in enumerate(tsh):
            dummy_ts = TileSheat()
            tile_sheat = tsh[tile_sheat_name]
            dummy_ts.set_tile_sheat(tile_sheat)
            self.my_tile_sheats_dict[i+1] = copy(dummy_ts)
    
    def load_objects(self, filename: str):
        self.objects = {}
        self.rendered_objects = []
        dobj = DataLoader().Load_from_file_sprites(filename)
        
        for name in dobj:
            obj_1:Sprite = copy(dobj[name])
            obj_2:Sprite = copy(dobj[name])
            obj_2.set_size([40,40])
            self.objects[name] = obj_1
            self.rendered_objects.append([name, obj_2])
            
    def load_grass(self, filename: str):
    
        self.grasses = {}
        self.rendered_grasses = []
        dobj = DataLoader().Load_from_file_grass(filename)
        print(dobj)
        
        for name in dobj:
            obj_1:Grass = copy(dobj[name])
            obj_2:Grass = copy(dobj[name])
            obj_2.sprite.set_size([40,40])
            self.grasses[name] = obj_1
            self.rendered_grasses.append([name, obj_2])
            
    def create_grid(self):
        global LAYERS, LAYER_ID
        
        GRID = []
        for i in range(int(self.tile_count_h.text)):
            gp = []
            for j in range(int(self.tile_count_w.text)):
                gp.append(0)
            GRID.append(gp)
            
        OBJS = []
        for i in range(int(self.tile_count_h.text)):
            ob = []
            for j in range(int(self.tile_count_w.text)):
                ob.append(0)
            OBJS.append(ob)
        LAYER_ID+=1
        GRASES = []
        RECTS = []
        LAYERS.append([GRID, LAYER_ID, None, None, OBJS, GRASES, RECTS])
        #self.tbl_places.opened = False
                
    def render_loaded_tile_sheats(self, pos, size, surf):
        global VABOR_TILE, VABOR_TILE_NAME
        #self.MOUSE_EH.EventsUpdate()
        position = copy([pos[0]+10,pos[1]+30])
        for i, tile_sheat in enumerate(self.loaded_tilesheats):
            if position[1]+70< pos[1]+size[1]-55:
                Draw.draw_rect(surf, position, [70,70], COLOR_4B,radius=5)
                if in_rect(position,[70,70],Mouse.pos):
                    Draw.draw_rect(surf, position, [70,70], COLOR_2B,1,radius=5)
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        
                        VABOR_TILE = tile_sheat[2]
                        VABOR_TILE_NAME = tile_sheat[0]
                
                if VABOR_TILE == tile_sheat[2]:
                    Draw.draw_rect(surf, position, [70,70], COLOR_3B,4,radius=5)
                
            
                tile_sheat[1].tiles['one'].center = [position[0]+35, position[1]+35]
                
                tile_sheat[1].tiles['one'].render(surf)
                self.tile_name_text.draw(surf, [position[0]+35, position[1]+35+35-7], True, tile_sheat[0],COLOR_WHITE)
            
            position[0]+=70
            
            if (position[0]+70-10)>(self.tbl_tiles.pos[0]+self.tbl_tiles.size[0]-20):
                position[1]+=70
                position[0] = pos[0]+10
            
    def render_tbl_tiles(self, pos, size, surf):
        self.tbl_tiles_load_btn.pos = [pos[0]+5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.tbl_tiles_select_btn.pos = [pos[0]+size[0]-self.tbl_tiles_load_btn.size[0]-5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.tbl_tiles_load_tb.pos = [pos[0]+5, pos[1]+size[1]-(self.tbl_tiles_load_btn.size[1])*2-10]
        self.tbl_tiles_load_tb.size[0] = size[0]-10
        
        Draw.draw_rect(surf, [pos[0]+5,pos[1]+25],[size[0]-10,size[1]-60],COLOR_1B,radius=5)
        
        self.tbl_tiles_load_btn.render(surf)
        self.tbl_tiles_select_btn.render(surf)
        self.tbl_tiles_load_tb.render(surf)
        self.render_loaded_tile_sheats(pos, size, surf)
        
        if self.tbl_tiles_load_btn.click:
            self.load_tile_sheats()
    
    def render_grid_create(self, pos, size, surf):
        pos = [
            pos[0]+5, pos[1]+25
        ]
        self.tile_count_w.pos = [pos[0], pos[1]]
        self.tile_count_h.pos = [pos[0], pos[1]+30]
        self.tile_count_w.size[0] = size[0]-10
        self.tile_count_h.size[0] = size[0]-10
        
        self.tile_grid_create_btn.pos = [pos[0], pos[1]+60]
        self.tile_grid_create_btn.size[0] = size[0]-10
        
        self.tile_count_h.render(surf)
        self.tile_count_w.render(surf)
        self.tile_grid_create_btn.render(surf)
        
        if self.tile_grid_create_btn.click:
            self.create_grid()
            self.tbl_places.opened = False
        
    def render_loaded_datas(self, pos, size, surf):
        load_datas = os.listdir('mapcreatordata')
        datas = []
        for text in load_datas:
            try:
                if text.split('.')[1] == 'data':
                    datas.append(text)
            except:...
        
        self.loaded_files = datas
        for i, text in enumerate( self.loaded_files ):
            p = [pos[0]+5,pos[1]+i*25+25]
            Draw.draw_rect(surf, p, [size[0]-10,24], COLOR_4B, radius=3)
            if in_rect(p, [size[0]-10,24], Mouse.pos):
                Draw.draw_rect(surf, p, [size[0]-10,24], COLOR_2B, radius=3, width=1)
                if self.MOUSE_EH.GetEventById('vabor_tile'):
                    if 'tiles' in text:
                        self.tbl_tiles_load_tb.text = "mapcreatordata\\" + text
                        self.load_tile_sheats()
                        self.loaded_file_tbl.opened = True
                    if 'objects' in text:
                        self.load_objects("mapcreatordata\\" + text)
                        self.loaded_file_tbl.opened = True
                    if 'grass' in text:
                        self.load_grass("mapcreatordata\\" + text)
                        self.loaded_file_tbl.opened = True
                        
            self.loaded_text.draw(surf, [p[0]+10, p[1]], False, text,COLOR_WHITE)
        
    def render_objects(self, pos, size, surf):
        global VABOR_OBJ_NAME, VABOR_OBJ
        self.obj_load_btn.pos = [pos[0]+5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.obj_load_btn.size[0] = size[0]-10
        self.obj_load_btn.update()
        self.obj_load_btn.render(surf)
        if self.obj_load_btn.click:
            self.loaded_file_tbl.opened = True
            
        Draw.draw_rect(surf, [pos[0]+5,pos[1]+25],[size[0]-10,size[1]-60],COLOR_1B,radius=5)
            
        position = copy([pos[0]+10,pos[1]+30])
        for i, obj in enumerate(self.rendered_objects):
            if position[1]+70< pos[1]+size[1]-55:
                obj[1].center = [position[0]+35, position[1]+35]
                Draw.draw_rect(surf, position, [70,70], COLOR_4B,radius=5)
                if in_rect(position,[70,70],Mouse.pos):
                    
                    
                    
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        if VABOR_OBJ_NAME == obj[0]:
                            VABOR_OBJ_NAME = None
                        else:
                            VABOR_OBJ_NAME = obj[0]
                            VABOR_OBJ = copy(obj[1])
                    
                    Draw.draw_rect(surf, [position[0],position[1]], [70,70], COLOR_2B,1,radius=5)
                    
                
                if VABOR_OBJ_NAME == obj[0]:
                    Draw.draw_rect(surf, [position[0], position[1]], [70,70], COLOR_3B,4,radius=5)
                
            
                
                
                
                obj[1].render(surf)
                self.tile_name_text.draw(surf, [position[0]+35, position[1]+35+35-7], True, obj[0],COLOR_WHITE)
                
            
            position[0]+=70
            
            if (position[0]+70-10)>(self.obj_table.pos[0]+self.obj_table.size[0]-20):
                position[1]+=70
                position[0] = pos[0]+10
    
    def render_grasses(self, pos ,size, surf):
        global VABOR_GRASSES
        self.grass_load_btn.pos = [pos[0]+5, pos[1]+size[1]-self.grass_load_btn.size[1]-5]
        self.grass_load_btn.size[0] = size[0]-10
        self.grass_load_btn.update()
        self.grass_load_btn.render(surf)
        
        if self.grass_load_btn.click:
            self.loaded_file_tbl.opened = True
            
        self.obj_load_btn.pos = [pos[0]+5, pos[1]+size[1]-self.tbl_tiles_load_btn.size[1]-5]
        self.obj_load_btn.size[0] = size[0]-10
        self.obj_load_btn.update()
        self.obj_load_btn.render(surf)
        if self.obj_load_btn.click:
            self.loaded_file_tbl.opened = True
            
        Draw.draw_rect(surf, [pos[0]+5,pos[1]+25],[size[0]-10,size[1]-60],COLOR_1B,radius=5)
            
        position = copy([pos[0]+10,pos[1]+30])
        for i, grass in enumerate(self.rendered_grasses):
            if position[1]+70< pos[1]+size[1]-55:
                
                grass[1].sprite.center = [position[0]+35, position[1]+35]
                Draw.draw_rect(surf, position, [70,70], COLOR_4B,radius=5)
                if in_rect(position,[70,70],Mouse.pos):
                    
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        if grass[0] not in VABOR_GRASSES:
                            VABOR_GRASSES.append(grass[0])
                        else:
                            VABOR_GRASSES.remove(grass[0])
                    
                    Draw.draw_rect(surf, [position[0],position[1]], [70,70], COLOR_2B,1,radius=5)
                    
                if grass[0] in VABOR_GRASSES:
                    Draw.draw_rect(surf, [position[0], position[1]], [70,70], COLOR_3B,4,radius=5)
                
                grass[1].sprite.render(surf)
                self.tile_name_text.draw(surf, [position[0]+35, position[1]+35+35-7], True, grass[0],COLOR_WHITE)
                
            position[0]+=70
            
            if (position[0]+70-10)>(self.grass_table.pos[0]+self.grass_table.size[0]-20):
                position[1]+=70
                position[0] = pos[0]+10
    
    def save_window_render(self, pos, size, surf):
        pos = [pos[0]+5, pos[1]+25]
        in_the_rect  = {
            'pos': pos,
            'size':[size[0]-10,size[1]-90]
        }
        center_pos = [in_the_rect['pos'][0]+in_the_rect['size'][0]/2, in_the_rect['pos'][1]+in_the_rect['size'][1]/2]
        Draw.draw_rect(surf, in_the_rect['pos'],in_the_rect['size'],COLOR_4B, radius=5)
        
        self.save_button.size[0] = in_the_rect['size'][0]
        self.save_button.pos = [in_the_rect['pos'][0], in_the_rect['pos'][1]+in_the_rect['size'][1]+35]
        self.save_button.render(surf)
        self.save_button.update()
        
        self.saveed_file_name_text_box.pos = [in_the_rect['pos'][0], in_the_rect['pos'][1]+in_the_rect['size'][1]+5]
        self.saveed_file_name_text_box.size[0] = in_the_rect['size'][0]/2-5
        self.saveed_file_name_text_box.update()
        self.saveed_file_name_text_box.render(surf)
        
        self.saveed_file_collide_layer_text_box.pos = [in_the_rect['pos'][0]+in_the_rect['size'][0]/2+2.5, in_the_rect['pos'][1]+in_the_rect['size'][1]+5]
        self.saveed_file_collide_layer_text_box.size[0] = in_the_rect['size'][0]/2-2.5
        self.saveed_file_collide_layer_text_box.update()
        self.saveed_file_collide_layer_text_box.render(surf)
        
        if len(LAYERS)>0:
            
            surf.blit(self.pre_rendered_surf, [center_pos[0]-120,center_pos[1]-120])
            
            Draw.draw_line(surf, [center_pos[0]-120,center_pos[1]-120], [center_pos[0]+120,center_pos[1]-120], 'red',2)
            Draw.draw_line(surf, [center_pos[0]-120,center_pos[1]-120], [center_pos[0]-120,center_pos[1]+120], 'blue',2)
            
            
            self.tile_name_text.draw(surf, [in_the_rect['pos'][0]+5,in_the_rect['pos'][1]+in_the_rect['size'][1]-40], False, f'w: {len(LAYERS[0][0][0])}', (255,0,0))
            self.tile_name_text.draw(surf, [in_the_rect['pos'][0]+5,in_the_rect['pos'][1]+in_the_rect['size'][1]-20], False, f'h: {len(LAYERS[0][0])}', (0,0,255))
            self.tile_name_text.draw(surf, [in_the_rect['pos'][0]+5,in_the_rect['pos'][1]+5], False, f'layers count : {len(LAYERS)}', COLOR_3B)
            
            if self.save_button.click:
                self.SAVEMAP()
        else:
            
            self.tile_name_text.draw(surf, center_pos, True, 'Layers not found!', (255,255,255))
        
    def SAVEMAP(self):
        file_name = self.saveed_file_name_text_box.text
        
        serialized_data = []
        map_data = []
        for layer in LAYERS:
            
            map_data.append([
                layer[0], layer[1], layer[4], layer[5], layer[6]
            ])
        serialized_data = [int(self.saveed_file_collide_layer_text_box.text), map_data]
        with open(f'{file_name}.json','w') as write_file:
            json.dump(serialized_data, write_file)
            
        self.saved_surf_timer = 100
            
    def up(self, arr, index):
        if index-1>=0:
            elem = copy(arr[index])
            del arr[index]
            arr.insert(index-1, elem)
        
    def down(self, arr, index):
        try:
            elem = copy(arr[index])
            del arr[index]
            arr.insert(index+1, elem)
        except:
            ...
        
    def render_layers_adder(self, pos, size, surf):
        global VABOR_LAYER_INDEX
        upos = [
            pos[0]+5, pos[1]+25
        ]
        dpos = [
            pos[0]+5,pos[1]+size[1]
        ]
        self.layer_add_bt.pos = [dpos[0],dpos[1]-self.layer_add_bt.size[1]-5]
        self.layer_add_bt.size[0] = size[0]-10
        #self.MOUSE_EH.EventsUpdate()
        
        self.layer_add_bt.render(surf)
        if in_rect(pos, size, Mouse.pos) and self.MOUSE_EH.GetEventById('vabor_tile'):
            gm.release = True
        
        for i, layer in enumerate( LAYERS ):
            rpos = [upos[0], upos[1]+i*42]
            rsize = [size[0]-10,40]
            if rpos[1]+rsize[1]<self.layares_table.pos[1]+self.layares_table.size[1]-60:
                Draw.draw_rect(surf, rpos, rsize , COLOR_1B, radius=3)
                if in_rect(rpos, [rsize[0]-40,rsize[1]], Mouse.pos):
                    Draw.draw_rect(surf, rpos, rsize , COLOR_3B, width=1, radius=3)
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        if VABOR_LAYER_INDEX == i:
                            VABOR_LAYER_INDEX = None
                        else:
                            VABOR_LAYER_INDEX = i
                if VABOR_LAYER_INDEX == i:
                    Draw.draw_rect(surf, rpos, rsize , COLOR_2B, width=3, radius=3)
                self.loaded_text.draw(surf, [rpos[0]+5, rpos[1]+1], False, 'layer '+str(layer[1]), COLOR_WHITE)
                self.small_text.draw(surf, [rpos[0]+5, rpos[1]+23], False, f'{len(layer[0])}X{len(layer[0][0])}', COLOR_2B)
                
                up_bt_rect = [rpos[0]+rsize[0]-20, rpos[1]]
                down_bt_rect = [rpos[0]+rsize[0]-20, rpos[1]+20]
                dell_rect = [rpos[0]+rsize[0]-40, rpos[1]]
                Draw.draw_rect(surf, up_bt_rect, [20] , COLOR_3B, radius=[0,3,0,0])
                Draw.draw_rect(surf, down_bt_rect, [20] , COLOR_3B, radius=[0,0,3,0])
                Draw.draw_rect(surf, dell_rect, [20,40] , COLOR_CLOSE_1, radius=[3,0,0,3])

                if in_rect(up_bt_rect, [20,20], Mouse.pos):
                    Draw.draw_rect(surf, up_bt_rect, [20] , COLOR_WHITE,width=2, radius=[0,3,0,0])
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        self.up(LAYERS, i)
                if in_rect(down_bt_rect, [20,20], Mouse.pos):
                    Draw.draw_rect(surf, down_bt_rect, [20] , COLOR_WHITE,width=2, radius=[0,0,3,0])
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        self.down(LAYERS, i)
                if in_rect(dell_rect, [20,40], Mouse.pos):
                    Draw.draw_rect(surf, dell_rect, [20,40] , COLOR_CLOSE_2, radius=[3,0,0,3])
                    if self.MOUSE_EH.GetEventById('vabor_tile'):
                        del LAYERS[i]
                        break
                    
                Draw.draw_lines(surf, [[up_bt_rect[0]+4,up_bt_rect[1]+4],[up_bt_rect[0]+20-4,up_bt_rect[1]+4],[up_bt_rect[0]+10,up_bt_rect[1]+4],[up_bt_rect[0]+10,up_bt_rect[1]+16]], COLOR_WHITE, 2)
                Draw.draw_lines(surf, [[down_bt_rect[0]+4,down_bt_rect[1]+16],[down_bt_rect[0]+20-4,down_bt_rect[1]+16],[down_bt_rect[0]+10,down_bt_rect[1]+16],[down_bt_rect[0]+10,down_bt_rect[1]+4]], COLOR_WHITE, 2)
            else:
                rposu = [upos[0], upos[1]+(i-1)*42]
                rsizeu = [size[0]-10,40]
                if rposu[1]+rsizeu[1]<self.layares_table.pos[1]+self.layares_table.size[1]-60:
                    self.loaded_text.draw(surf, [rpos[0]+rsize[0]/2,rpos[1]+rsize[1]/2-10], True, '...',COLOR_WHITE)
        
        if self.layer_add_bt.click:
            self.tbl_places.opened = True
        
    def render(self, win_surf_, win_size, win_center, ms):
        global VABOR_LAYER_INDEX
        self.update(win_size, win_center, ms)
        self.MOUSE_EH.EventsUpdate()
        
        
        self.tbl_tiles.render(render_event=self.render_tbl_tiles,surf=win_surf_)
        self.tbl_places.render(surf=win_surf_, render_event=self.render_grid_create)
        self.loaded_file_tbl.render(surf=win_surf_, render_event=self.render_loaded_datas)
        self.layares_table.render(surf=win_surf_, render_event=self.render_layers_adder)
        self.obj_table.render(surf=win_surf_, render_event=self.render_objects)
        self.save_table.render(surf=win_surf_, render_event=self.save_window_render)
        self.grass_table.render(surf=win_surf_, render_event=self.render_grasses)
        
        Draw.draw_rect(win_surf_, self.pos, self.size, COLOR_BARS_BG, radius=10)
        
        
        self.btn_tiles.render(win_surf_)
        self.btn_places.render(win_surf_)
        self.surfs_bt.render(win_surf_)
        self.obj_btn.render(win_surf_)
        self.save_btn.render(win_surf_)
        self.grass_btn.render(win_surf_)
        
        s = copy(self.size[0])
        percent = 1-(gm.scaling_timer/30)
        size = s*percent 
        
        
        Draw.draw_rect(win.surf, [win_center[0]-self.size[0]/2, win_size[1]-13], [self.size[0], 6], LOAD_COLOR, radius=5)
        Draw.draw_rect(win.surf, [win_center[0]-self.size[0]/2, win_size[1]-13], [size, 6], LOAD_COLOR_NONE, radius=5)
        if self.saved_surf_timer!=0:
            self.saved_surf_timer-=1
            win_surf_.blit(self.saved_surf, [win.get_size()[0]-100,win.get_size()[1]+25])
        
        if self.btn_tiles.click:
            self.tbl_tiles.opened = True
        if self.btn_places.click:
            self.tbl_places.opened = True
        if self.tbl_tiles_select_btn.click:
            self.loaded_file_tbl.opened = True
        if self.surfs_bt.click:
            self.layares_table.opened = True
        if self.obj_btn.click:
            self.obj_table.opened = True
        if self.grass_btn.click:
            self.grass_table.opened = True
            
        if self.btn_tiles.vabor:
            self.tb_help.render(Mouse.pos, win_surf_)
        if self.save_btn.click:
            self.save_table.opened = True
            
        if self.save_btn.click:
            try:
                self.pre_rendered_surf = pygame.transform.scale(copy(gm.layer_dummy),[240,240])
                VABOR_LAYER_INDEX = None
            except:...
            
class UpDownTable:
    def __init__(self) -> None:
        self.pos = [0, 0]
        self.buttons_count = 14
        self.buttons_size = 40
        self.btns_scale = 2
        
        self.auto_connect_bt = TrigerButton(datas['con_bt'],self.btns_scale, True)
        self.auto_connecta_bt = TrigerButton(datas['cona_bt'],self.btns_scale, True)
        self.coloring_bt = TrigerButton(datas['col_bt'],self.btns_scale, True)
        self.pen_bt = TrigerButton(datas['pen_bt'],self.btns_scale, True)
        self.penb_bt = TrigerButton(datas['penb_bt'],self.btns_scale, True)
        self.penr_bt = TrigerButton(datas['penr_bt'],self.btns_scale, True)
        self.penrd_bt = TrigerButton(datas['penrd_bt'],self.btns_scale, True)
        self.gridv_btn = TrigerButton(datas['gridv_btn'],self.btns_scale, True)
        self.alp_btn = TrigerButton(datas['alp_btn'],self.btns_scale, True)
        self.copy_btn = TrigerButton(datas['copy_btn'],self.btns_scale, True)
        self.obj_pen_btn = TrigerButton(datas['pen_obj'],self.btns_scale, True)
        self.obj_viev_rect_btn = TrigerButton(datas['obj_viev_rect_btn'], self.btns_scale, True)
        self.grass_bt = TrigerButton(datas['pen_grass'], self.btns_scale, True)
        self.pen_coll = TrigerButton(datas['pen_col'], self.btns_scale, True)
        
        self.copy_help = UserHelp('How to copy', 'Coped tiles array', 'H')
            
    def update(self):
        global ON_THE_BOARD
        self.size = [self.buttons_size*self.buttons_count+10, self.buttons_size+10]
        self.pos = [
            win_center[0]-self.size[0]/2,
            win_center[1]+win_size[1]/2-self.buttons_size-90-10
        ]
        self.auto_connect_bt.update([self.pos[0]+5,self.pos[1]+5])
        self.auto_connecta_bt.update([self.pos[0]+5+40,self.pos[1]+5])
        self.coloring_bt.update([self.pos[0]+5+40+40,self.pos[1]+5])
        self.pen_bt.update([self.pos[0]+85+40,self.pos[1]+5])
        self.penb_bt.update([self.pos[0]+85+40+40,self.pos[1]+5])
        self.penr_bt.update([self.pos[0]+85+40+40+40,self.pos[1]+5])
        self.penrd_bt.update([self.pos[0]+85+40+40+40+40,self.pos[1]+5])
        self.copy_btn.update([self.pos[0]+85+40+40+40+40+40,self.pos[1]+5])
        self.gridv_btn.update([self.pos[0]+85+40+40+40+40+40+40,self.pos[1]+5])
        self.alp_btn.update([self.pos[0]+85+40+40+40+40+40+40+40,self.pos[1]+5])
        self.obj_pen_btn.update([self.pos[0]+85+40+40+40+40+40+40+40+40,self.pos[1]+5])
        self.obj_viev_rect_btn.update([self.pos[0]+85+40+40+40+40+40+40+40+40+40,self.pos[1]+5])
        self.grass_bt.update([self.pos[0]+85+40+40+40+40+40+40+40+40+40+40,self.pos[1]+5])
        self.pen_coll.update([self.pos[0]+85+40+40+40+40+40+40+40+40+40+40+40,self.pos[1]+5])
        
        if in_rect(self.pos, self.size, Mouse.pos):
            ON_THE_BOARD = True
        
    def render(self, surf):
        self.update()
        Draw.draw_rect(surf, self.pos, self.size, COLOR_BARS_BG, radius=10)
        
        self.auto_connect_bt.render(surf)
        self.auto_connecta_bt.render(surf)
        self.coloring_bt.render(surf)
        self.pen_bt.render(surf)
        self.penb_bt.render(surf)
        self.penr_bt.render(surf)
        self.penrd_bt.render(surf)
        self.gridv_btn.render(surf)
        self.alp_btn.render(surf)
        self.copy_btn.render(surf)
        self.obj_pen_btn.render(surf)
        self.obj_viev_rect_btn.render(surf)
        self.grass_bt.render(surf)
        self.pen_coll.render(surf)
        
        if self.copy_btn.triger:
            self.copy_help.render(Mouse.pos, surf)

class GridManager:
    def __init__(self) -> None:
        self.global_pos = [0, 0]
        self.tile_size = 30
        self.start_tile_size = 30
        self.end_tile_size = 30
        self.mm = MouseEventHandler()
        self.mm.AddEvent(Mouse(Mouse.middle, Mouse.press_event, 'move_press'))
        self.mm.AddEvent(Mouse(Mouse.left, Mouse.press_event, 'set'))
        self.mm.AddEvent(Mouse(Mouse.right, Mouse.press_event, 'cl'))
        self.mm.AddEvent(Mouse(Mouse.left, Mouse.click_event, 'pos1'))
        self.mm.AddEvent(Mouse(Mouse.right, Mouse.click_event, 'pos2'))
        self.GRID = []
        self.vabor_tile = 0
        self.s = None
        self.layer_dummy = None
        self.tile_scaleing = 30/14
        
        self.pen_radius = 100
        self.pen_radius_scale = 1
        self.update_tiler = 0
        
        self.release = False
        self.clicked = False
        self.pressed = False
        
        self.start_pos = None
        self.end_size = [0,0]
        
        self.scaling_timer = 100
        
        
        self.copy_arr = []
        self.copy_surf = None
        self.coped_trig = False
        
        self.objects_deltas = [0,0]
        
        self.timer = 0
        
        self.obj_name_text = Text('arial',15, color='white')
        
        self.rendered = False
        
        
        self.grass_pos1 = None
        self.grass_pos2 = None
        self.g_size = None
        
    def render_grid(self, GRID1, surf, tiles_dict):
        global GRID, VABOR_LAYER_INDEX, LAYERS
        self.render_all_grids(surf, tiles_dict)
        
        if VABOR_LAYER_INDEX is not None:
            try:
                GRID = LAYERS[VABOR_LAYER_INDEX][0]
            except:
                VABOR_LAYER_INDEX = None
                
        self.update_tiler+=1
        self.GRID = GRID1
        if self.scaling_timer>0:
            self.scaling_timer-=1
            
        if VABOR_LAYER_INDEX is not None:
            if dut.coloring_bt.triger or Keyboard.key_pressed('c') or self.scaling_timer!=0 or self.pressed:
                if GRID1 is not None:
                    for y in range(len(self.GRID)):
                        for x in range(len(self.GRID[y])):
                            pos =  [x*self.tile_size+self.global_pos[0],y*self.tile_size+self.global_pos[1]]
                            if pos[0]>0-self.tile_size and pos[1]>0-self.tile_size and pos[0]+self.tile_size/2<win.get_size()[0]+self.tile_size and pos[1]+self.tile_size/2<win.get_size()[1]+self.tile_size:
                                tile = self.GRID[y][x]
                                if tile in tiles_dict.keys():
                                    tile_sheat = tiles_dict[tile]
                                    color = tile_sheat.tiles['one'].get_center_color()
                                    Draw.draw_rect(surf, pos, [self.tile_size], color)
                                    
            
            if dut.auto_connect_bt.triger:
                if self.scaling_timer==1 or self.release:
                    if GRID1!=None and len(tiles_dict)>0:
                        self.render_surfnc(tiles_dict, GRID1)
                        
            elif dut.auto_connecta_bt.triger:
                if self.scaling_timer==1 or self.release:
                    if GRID1!=None and len(tiles_dict)>0:
                        self.render_surfc(tiles_dict, GRID1)
                    
            else:
                if GRID1 is not None:
                    for y in range(len(self.GRID)):
                        for x in range(len(self.GRID[y])):
                            pos =  [x*self.tile_size+self.tile_size/2+self.global_pos[0],y*self.tile_size+self.tile_size/2+self.global_pos[1]]
                            if pos[0]>0-self.tile_size and pos[1]>0-self.tile_size and pos[0]+self.tile_size/2<win.get_size()[0]+self.tile_size and pos[1]+self.tile_size/2<win.get_size()[1]+self.tile_size:
                                tile = self.GRID[y][x]
                                if tile in tiles_dict.keys():
                                    tile_sheat = tiles_dict[tile]
                                    tile_set_size(tile_sheat.tiles['one'], self.tile_size)
                                    tile_sheat.tiles['one'].center = pos
                                    tile_sheat.tiles['one'].render(surf)

            if self.s is not None and self.scaling_timer==0 and (dut.auto_connect_bt.triger or dut.auto_connecta_bt.triger):
                surf.blit(self.s, [self.global_pos[0], self.global_pos[1]])
            
            if GRID1 is not None:

                grid_w = len(GRID1[0])
                grid_h = len(GRID1)
                if dut.gridv_btn.triger:
                    for i in range(grid_h+1):
                        Draw.draw_hline(surf, self.global_pos[1]+i*self.tile_size, self.global_pos[0], self.global_pos[0]+grid_w*self.tile_size, 1, COLOR_GRID )
                    for i in range(grid_w+1):
                        Draw.draw_vline(surf, self.global_pos[0]+i*self.tile_size, self.global_pos[1], self.global_pos[1]+grid_h*self.tile_size, 1, COLOR_GRID )
                else:
                    Draw.draw_rect_fast(surf, self.global_pos, [grid_w*self.tile_size, grid_h*self.tile_size], (255,255,255))
    
            self.render_object_datas()
    
    def render_all_grids(self, surf, tiles_dict):
        if len(LAYERS)>0 :
            if self.scaling_timer==1 or self.release:
                self.layer_dummy = pygame.Surface([len(LAYERS[0][0][0])*self.tile_size,len(LAYERS[0][0])*self.tile_size], flags=pygame.SRCALPHA, depth=32)
                for i, grid in enumerate( LAYERS ):
                    if i!=VABOR_LAYER_INDEX:
                        
                        if len(tiles_dict)>0:
                            grid[2] = create_map_surf_by_tilesheats_and_array_no_connect(tiles_dict, grid[0], self.tile_size)
                            if dut.alp_btn.triger:
                                alpha = (i+1)/len(LAYERS)*255
                                grid[2].set_alpha(alpha)
                        
                            self.layer_dummy.blit(grid[2], [0,0])
                    self.render_objects(grid, self.layer_dummy)
                    
                        
                    
                    
                
                    grid[3] = deepcopy(grid[0])
                    self.rendered = True
                    
                    
            if self.scaling_timer==0:
                if self.layer_dummy is not None:
                    surf.blit(self.layer_dummy, [self.global_pos[0], self.global_pos[1]])
                    
            else:
                for grid in LAYERS:
                    for y in range(len(grid[0])):
                        for x in range(len(grid[0])):
                            pos =  [x*self.tile_size+self.global_pos[0],y*self.tile_size+self.global_pos[1]]
                            if pos[0]>0-self.tile_size and pos[1]>0-self.tile_size and pos[0]+self.tile_size/2<win.get_size()[0]+self.tile_size and pos[1]+self.tile_size/2<win.get_size()[1]+self.tile_size:
                                tile = grid[0][y][x]
                                if tile in tiles_dict.keys():
                                    tile_sheat = tiles_dict[tile]
                                    color = tile_sheat.tiles['one'].get_center_color()
                                    Draw.draw_rect(surf, pos, [self.tile_size], color)

        self.render_object_datas()
    #@NewProcess('nc')
    def render_surfnc(self, tiles_dict, GRID1):
        self.s = create_map_surf_by_tilesheats_and_array_no_connect(tiles_dict, GRID1, self.tile_size)
        self.render_objects(LAYERS[VABOR_LAYER_INDEX], self.s)
        
    #@NewProcess('c')
    def render_surfc(self, tiles_dict, GRID1):
        self.s = create_map_surf_by_tilesheats_and_array(tiles_dict, GRID1, self.tile_size)
        self.render_objects(LAYERS[VABOR_LAYER_INDEX], self.s)
        
    def render_grasses(self):
        for layer in LAYERS:
            l = layer[5]
            
            for i, grass in enumerate(l):
                rect = [grass[1][0][0]*self.tile_size+self.global_pos[0],grass[1][0][1]*self.tile_size+self.global_pos[1]], [grass[1][1][0]*self.tile_size,grass[1][1][1]*self.tile_size]
                for k in range(len(grass[0])):
                    pos = [
                        rect[0][0],
                        rect[0][1]+k*15
                    ]
                    self.obj_name_text.draw(win.surf, pos, text=grass[0][k],color='white')
                if in_rect(rect[0],rect[1],Mouse.pos):
                    Draw.draw_rect_fast(win.surf, rect[0], rect[1], (255,25,25))
                    if self.mm.GetEventById('pos2'):
                        del l[i]
                        break
                else:
                    Draw.draw_rect_fast(win.surf, rect[0], rect[1], (255,255,255))
                    
    def render_rects(self):
        for layer in LAYERS:
            l = layer[6]
            
            for i, grass in enumerate(l):
                
                rect = [grass[0][0]*self.tile_size+self.global_pos[0],grass[0][1]*self.tile_size+self.global_pos[1]], [grass[1][0]*self.tile_size,grass[1][1]*self.tile_size]
                
                  
                if in_rect(rect[0],rect[1],Mouse.pos):
                    Draw.draw_rect_fast(win.surf, rect[0], rect[1], (255,25,25))
                    if self.mm.GetEventById('pos2'):
                        del l[i]
                        break
                else:
                    Draw.draw_rect_fast(win.surf, rect[0], rect[1], (255,255,255))
                    
    def update(self, ms):
        
                
        if GRID is not None:
            self.mm.EventsUpdate()
            if self.mm.GetEventById('move_press'):
                self.global_pos[0]+=ms[0]
                self.global_pos[1]+=ms[1]
            
            
            mx = Mouse.pos[0]-self.global_pos[0]
            my = Mouse.pos[1]-self.global_pos[1]
            map_w = len(GRID[0])*self.tile_size
            map_h = len(GRID)*self.tile_size
            dx = mx/map_w
            dy = my/map_h
            if Mouse.whell[1]!=0:
                self.scaling_timer=30
                
            if Mouse.whell[1]!=0 and self.tile_size+Mouse.whell[1]>4 and not Keyboard.key_pressed('shift'):
                self.tile_size+=Mouse.whell[1]
                
                
                nmap_w = len(GRID[0])*self.tile_size
                nmap_h = len(GRID)*self.tile_size
                nmx = nmap_w*dx
                nmy = nmap_h*dy
                delta_x = nmx-mx
                delta_y = nmy-my
                self.global_pos[0]-=delta_x
                self.global_pos[1]-=delta_y
            self.end_tile_size = self.tile_size
        self.release = False
                
    def draw(self):
        global LAYERS
        if dut.pen_bt.click:
            dut.penb_bt.triger = False
            dut.penr_bt.triger = False
            dut.penrd_bt.triger = False
            dut.copy_btn.triger = False
        if dut.penb_bt.click:
            dut.pen_bt.triger = False
            dut.penr_bt.triger = False
            dut.penrd_bt.triger = False
            dut.copy_btn.triger = False
        if dut.penr_bt.click:
            dut.pen_bt.triger = False
            dut.penb_bt.triger = False
            dut.penrd_bt.triger = False
            dut.copy_btn.triger = False
        if dut.penrd_bt.click:
            dut.pen_bt.triger = False
            dut.penb_bt.triger = False
            dut.penr_bt.triger = False
            dut.copy_btn.triger = False
        if dut.copy_btn.click:
            dut.pen_bt.triger = False
            dut.penb_bt.triger = False
            dut.penr_bt.triger = False
            dut.penrd_bt.triger = False
        if dut.obj_pen_btn.click:
            dut.pen_bt.triger = False
            dut.penb_bt.triger = False
            dut.penr_bt.triger = False
            dut.penrd_bt.triger = False
            dut.copy_btn.triger = False
            
            
        if dut.auto_connect_bt.click:
            dut.auto_connecta_bt.triger = False
        
        if dut.auto_connecta_bt.click:
            dut.auto_connect_bt.triger = False
            
        self.release = False
        self.pressed = False
        try:
            if VABOR_LAYER_INDEX is not None:
                GRID = LAYERS[VABOR_LAYER_INDEX][0]
                if GRID is not None:
                    
                    if dut.pen_bt.triger:
                        if self.clicked and not (self.mm.GetEventById('set') or self.mm.GetEventById('cl')):
                            self.release = True
                            self.clicked = False
                        
                        if in_rect(self.global_pos, [len(GRID[0])*self.tile_size, len(GRID)*self.tile_size], Mouse.pos) and not GLOBAL_PRESS_WIN:
                            mp = Mouse.pos
                            mx = mp[0]-self.global_pos[0]
                            my = mp[1]-self.global_pos[1]
                            
                            mx-=mx%self.tile_size
                            my-=my%self.tile_size
                            
                            index_x = int(mx//self.tile_size)
                            index_y = int(my//self.tile_size)
                            
                            Draw.draw_rect(win.surf, [self.global_pos[0]+index_x*self.tile_size,self.global_pos[1]+index_y*self.tile_size], [self.tile_size], (255,255,255), 2, 4)
                            
                            if self.mm.GetEventById('set'):
                                GRID[index_y][index_x] = VABOR_TILE
                                self.pressed = True
                            elif self.mm.GetEventById('cl'):
                                GRID[index_y][index_x] = 0
                                self.pressed = True
                            
                            if self.mm.GetEventById('pos1'):
                                self.clicked = True
                        
                    if dut.penb_bt.triger:
                        if self.clicked and not (self.mm.GetEventById('set') or self.mm.GetEventById('cl')):
                            self.release = True
                            self.clicked = False
                        
                        radius = self.pen_radius*self.pen_radius_scale
                        Draw.draw_circle(win.surf, Mouse.pos, radius, (255,255,255),2)
                        if Keyboard.key_pressed('shift'):
                            self.pen_radius_scale+=Mouse.whell[1]/10
                            
                        if self.mm.GetEventById('pos1'):
                            self.clicked = True
                        
                        for y in range(len(GRID)):
                            for x in range(len(GRID[y])):
                                if self.mm.GetEventById('set') and not GLOBAL_PRESS_WIN:
                                    self.pressed = True
                                    pos = [self.global_pos[0]+x*self.tile_size,self.global_pos[1]+y*self.tile_size]
                                    if in_circle(Mouse.pos, radius, pos):
                                        GRID[y][x] = VABOR_TILE
                                if self.mm.GetEventById('cl') and not GLOBAL_PRESS_WIN:
                                    pos = [self.global_pos[0]+x*self.tile_size,self.global_pos[1]+y*self.tile_size]
                                    self.pressed = True
                                    if in_circle(Mouse.pos, radius, pos):
                                        GRID[y][x] = 0
                    
                    if dut.penr_bt.triger or dut.penrd_bt.triger:
                        if self.mm.GetEventById('pos1') and not GLOBAL_PRESS_WIN:
                            self.start_pos = Mouse.pos
                        if self.start_pos is not None:
                            
                            
                            stp = copy(self.start_pos)
                            if self.mm.GetEventById('set'):
                                self.end_size = [
                                    Mouse.pos[0]-self.start_pos[0],
                                    Mouse.pos[1]-self.start_pos[1]
                                ]
                                self.copy_size = copy(self.end_size)
                                
                                if self.end_size[0]<0:
                                    stp[0] += self.end_size[0]
                                    self.end_size[0] = abs(self.end_size[0])
                                if self.end_size[1]<0:
                                    stp[1] += self.end_size[1]
                                    self.end_size[1] = abs(self.end_size[1])
                                Draw.draw_rect_fast(win.surf, stp, self.end_size, (255,255,255))
                                
                                for y in range(len(GRID)):
                                    for x in range(len(GRID[y])):
                                        if in_rect(stp, self.end_size, [self.global_pos[0]+x*self.tile_size+self.tile_size/2,self.global_pos[1]+y*self.tile_size+self.tile_size/2]):
                                            
                                            
                                            if dut.penrd_bt.triger:
                                                if GRID[y][x]!=0:
                                                    Draw.draw_rect(win.surf, [self.global_pos[0]+x*self.tile_size,self.global_pos[1]+y*self.tile_size], [self.tile_size], 'red',1, 4)
                                            else:
                                                Draw.draw_rect(win.surf, [self.global_pos[0]+x*self.tile_size,self.global_pos[1]+y*self.tile_size], [self.tile_size], COLOR_WHITE,1, 4)
                            else:
                                stp = copy(self.start_pos)
                                if self.copy_size[0]<0:
                                    stp[0] += self.copy_size[0]
                                    self.end_size[0] = abs(self.copy_size[0])
                                if self.copy_size[1]<0:
                                    stp[1] += self.copy_size[1]
                                    self.end_size[1] = abs(self.copy_size[1])
                                
                                for y in range(len(GRID)):
                                    for x in range(len(GRID[y])):
                                        if in_rect(stp, self.end_size, [self.global_pos[0]+x*self.tile_size+self.tile_size/2,self.global_pos[1]+y*self.tile_size+self.tile_size/2]):
                                            if dut.penr_bt.triger:
                                                GRID[y][x] = VABOR_TILE
                                            if dut.penrd_bt.triger:
                                                GRID[y][x] = 0
                                
                                self.start_pos = None
                                self.end_size = [0,0]
                                if dut.auto_connect_bt.triger:
                                    self.s = create_map_surf_by_tilesheats_and_array_no_connect(dt.my_tile_sheats_dict, GRID, self.tile_size)
                                elif dut.auto_connecta_bt.triger:
                                    self.s = create_map_surf_by_tilesheats_and_array(dt.my_tile_sheats_dict, GRID, self.tile_size)

                    if dut.copy_btn.triger:
                        if self.mm.GetEventById('pos2'):
                            self.copy_arr = []
                            self.coped_trig = False
                            self.copy_surf = None
                        if self.mm.GetEventById('pos1') and not GLOBAL_PRESS_WIN and Keyboard.key_pressed('h'):
                            self.start_pos = Mouse.pos
                        if self.start_pos is not None:
                            
                            
                            stp = copy(self.start_pos)
                            if self.mm.GetEventById('set'):
                                self.end_size = [
                                    Mouse.pos[0]-self.start_pos[0],
                                    Mouse.pos[1]-self.start_pos[1]
                                ]
                                self.copy_size = copy(self.end_size)
                                
                                if self.end_size[0]<0:
                                    stp[0] += self.end_size[0]
                                    self.end_size[0] = abs(self.end_size[0])
                                if self.end_size[1]<0:
                                    stp[1] += self.end_size[1]
                                    self.end_size[1] = abs(self.end_size[1])
                                Draw.draw_rect_fast(win.surf, stp, self.end_size, (255,255,255))
                                
                            else:
                                sp = [self.start_pos[0]-self.global_pos[0],self.start_pos[1]-self.global_pos[1]]
                                self.start_indexes = [
                                    int(((sp[0]-(sp[0]%self.tile_size))//self.tile_size)),
                                    int(((sp[1]-(sp[1]%self.tile_size))//self.tile_size))
                                ]
                                end_p = [
                                    sp[0]+self.end_size[0],
                                    sp[1]+self.end_size[1]
                                ]
                                self.stop_indexes = [
                                    int(((end_p[0]-(end_p[0]%self.tile_size))//self.tile_size)),
                                    int(((end_p[1]-(end_p[1]%self.tile_size))//self.tile_size))
                                ]
                                
                                try:
                                    self.copy_arr = self.get_sub_place(self.start_indexes, self.stop_indexes, LAYERS[VABOR_LAYER_INDEX][0])
                                    self.copy_surf = create_map_surf_by_tilesheats_and_array_no_connect(dt.my_tile_sheats_dict, self.copy_arr, self.tile_size)
                                    self.copy_surf.set_alpha(120)
                                    self.start_pos = None
                                    self.coped_trig = True
                                except:...
                            

                        if self.coped_trig and len(self.copy_arr)>0:
                            
                            if self.scaling_timer==1:
                                self.copy_surf = create_map_surf_by_tilesheats_and_array_no_connect(dt.my_tile_sheats_dict, self.copy_arr, self.tile_size)
                                self.copy_surf.set_alpha(120)
                            mp = Mouse.pos
                            
                            mp = [
                                (mp[0]-mp[0]%self.tile_size+self.global_pos[0]%self.tile_size),
                                (mp[1]-mp[1]%self.tile_size+self.global_pos[1]%self.tile_size),
                            ]
                            imp = (
                                int((mp[0]-self.global_pos[0]-(mp[0]-self.global_pos[0])%self.tile_size)//self.tile_size),
                                int((mp[1]-self.global_pos[1]-(mp[1]-self.global_pos[1])%self.tile_size)//self.tile_size)
                            )
                            if self.scaling_timer==0 and not Keyboard.key_pressed('h'):
                                win.surf.blit(self.copy_surf, mp)
                                Draw.draw_rect_fast(win.surf, mp, self.copy_surf.get_size(), (255,255,255))
                                
                            if self.mm.GetEventById('pos1'):
                                self.replace_elemets_in_arr(LAYERS[VABOR_LAYER_INDEX][0], self.copy_arr, imp)
                                self.scaling_timer = 10
        except:...
    
    def draw_objects(self):
        global LAYERS
        self.timer+=1
        if dut.obj_pen_btn.triger:
            if VABOR_LAYER_INDEX is not None and VABOR_OBJ_NAME is not None:
                layer = LAYERS[VABOR_LAYER_INDEX][4]
                
                if self.clicked and not (self.mm.GetEventById('set') or self.mm.GetEventById('cl')):
                    self.release = True
                    self.clicked = False
                
                obj = dt.objects[VABOR_OBJ_NAME]
                        
                if in_rect(self.global_pos, [len(layer[0])*self.tile_size, len(layer)*self.tile_size], Mouse.pos) and not GLOBAL_PRESS_WIN:
                    mp = Mouse.pos
                    mx = mp[0]-self.global_pos[0]
                    my = mp[1]-self.global_pos[1]
                            
                    mx-=mx%self.tile_size
                    my-=my%self.tile_size
                            
                    index_x = int(mx//self.tile_size)
                    index_y = int(my//self.tile_size)
                            
                    Draw.draw_rect(win.surf, [self.global_pos[0]+index_x*self.tile_size,self.global_pos[1]+index_y*self.tile_size], [self.tile_size], (255,255,255), 2, 4)
                    
                    if VABOR_OBJ!=None:
                        pos = [self.global_pos[0]+index_x*self.tile_size,self.global_pos[1]+index_y*self.tile_size]
                        obj.scale = self.tile_scaleing*self.tile_size/self.start_tile_size
                        obj.center = [
                                    pos[0]+self.tile_size/2+self.objects_deltas[0]*self.tile_scaleing*self.tile_size/self.start_tile_size,
                                    pos[1]+self.tile_size-obj.get_pre_size()[1]/2+self.objects_deltas[1]*self.tile_scaleing*self.tile_size/self.start_tile_size
                                ]
                        obj.render(win.surf)
                        
                        if self.timer%10==0:
                            if Keyboard.key_pressed('up'):
                                self.objects_deltas[1]-=1
                            if Keyboard.key_pressed('down'):
                                self.objects_deltas[1]+=1
                            if Keyboard.key_pressed('left'):
                                self.objects_deltas[0]-=1
                            if Keyboard.key_pressed('right'):
                                self.objects_deltas[0]+=1

                        if not ON_THE_BOARD:
                            if self.mm.GetEventById('pos1'):
                                
                                obj_data = [VABOR_OBJ_NAME, copy(self.objects_deltas)]
                                
                                layer[index_y][index_x] = obj_data
                                self.pressed = True
                    if self.mm.GetEventById('cl'):
                        layer[index_y][index_x] = 0
                        self.pressed = True
                            
                    if self.mm.GetEventById('pos1'):
                        self.clicked = True
                
    def draw_grasses(self):
        
        if dut.grass_bt.triger:
            if VABOR_LAYER_INDEX is not None and len(VABOR_GRASSES)!=0:
                layer = LAYERS[VABOR_LAYER_INDEX][5]
                l =  LAYERS[VABOR_LAYER_INDEX][4]
                
                
                
                
                        
                if in_rect(self.global_pos, [len(l[0])*self.tile_size, len(l)*self.tile_size], Mouse.pos) and not GLOBAL_PRESS_WIN:
                    mp = Mouse.pos
                    mx = mp[0]-self.global_pos[0]
                    my = mp[1]-self.global_pos[1]
                            
                    mx-=mx%self.tile_size
                    my-=my%self.tile_size
                            
                    index_x = int(mx//self.tile_size)
                    index_y = int(my//self.tile_size)
                    if self.grass_pos1 is not None and self.grass_pos2 is not None:
                        self.g_size = [self.grass_pos2[0]-self.grass_pos1[0]+1, 1]
                        Draw.draw_rect(win.surf, [self.global_pos[0]+self.grass_pos1[0]*self.tile_size,self.global_pos[1]+self.grass_pos1[1]*self.tile_size], [self.g_size[0]*self.tile_size,self.g_size[1]*self.tile_size], (255,255,255), 2, 4)
                    
                    
                    pos1 = [index_x,index_y]
                        
                    if self.mm.GetEventById('pos1'):
                        self.grass_pos1 = copy(pos1)
                    if self.grass_pos1 is not None and self.mm.GetEventById('set'):
                        self.grass_pos2 = copy(pos1)
                        self.grass_pos2[1] = self.grass_pos1[1]
                    if self.grass_pos1 is not None and not self.mm.GetEventById('set') and self.g_size is not None and self.grass_pos1[0]!=self.grass_pos2[0]:
                        print('grass setup')
                        layer.append([copy(VABOR_GRASSES), [copy(self.grass_pos1),copy(self.g_size)]])
                        self.g_size = None
                        self.grass_pos1 = None
                        self.grass_pos2 = None
                
    def draw_rects(self):
        if dut.pen_coll.triger:
            if VABOR_LAYER_INDEX is not None:
                layer = LAYERS[VABOR_LAYER_INDEX][6]
                l =  LAYERS[VABOR_LAYER_INDEX][4]
                
                
                
                
                        
                if in_rect(self.global_pos, [len(l[0])*self.tile_size, len(l)*self.tile_size], Mouse.pos) and not GLOBAL_PRESS_WIN:
                    mp = Mouse.pos
                    mx = mp[0]-self.global_pos[0]
                    my = mp[1]-self.global_pos[1]
                            
                    mx-=mx%self.tile_size
                    my-=my%self.tile_size
                            
                    index_x = int(mx//self.tile_size)
                    index_y = int(my//self.tile_size)
                    if self.grass_pos1 is not None and self.grass_pos2 is not None:
                        self.g_size = [self.grass_pos2[0]-self.grass_pos1[0]+1, self.grass_pos2[1]-self.grass_pos1[1]+1]
                        Draw.draw_rect(win.surf, [self.global_pos[0]+self.grass_pos1[0]*self.tile_size,self.global_pos[1]+self.grass_pos1[1]*self.tile_size], [self.g_size[0]*self.tile_size,self.g_size[1]*self.tile_size], (255,255,255), 2, 4)
                    
                    
                    pos1 = [index_x,index_y]
                        
                    if self.mm.GetEventById('pos1'):
                        self.grass_pos1 = copy(pos1)
                    if self.grass_pos1 is not None and self.mm.GetEventById('set'):
                        self.grass_pos2 = copy(pos1)
                        
                    if self.grass_pos1 is not None and not self.mm.GetEventById('set') and self.g_size is not None and self.grass_pos1!=self.grass_pos2:
                        print('rect setup')
                        layer.append([copy(self.grass_pos1),copy(self.g_size)])
                        self.g_size = None
                        self.grass_pos1 = None
                        self.grass_pos2 = None
                        
    def render_object_datas(self):
        if dut.obj_viev_rect_btn.triger:
            for layer in LAYERS:
                objs = layer[4]
                for y in range(len(objs)):
                    for x in range(len(objs[y])):
                        if objs[y][x]!=None and objs[y][x]!=0:
                            pos = [
                                    self.global_pos[0]+x*self.tile_size,
                                    self.global_pos[1]+y*self.tile_size
                            ]
                            obj = copy(dt.objects[objs[y][x][0]])
                            obj.scale = self.tile_scaleing*self.tile_size/self.start_tile_size
                            
                            center = [
                                pos[0]+self.tile_size//2+objs[y][x][-1][0]*self.tile_scaleing*self.tile_size/self.start_tile_size,
                                pos[1]+self.tile_size-obj.get_pre_size()[1]//2+objs[y][x][-1][1]*self.tile_scaleing*self.tile_size/self.start_tile_size
                            ]
                            size = obj.get_pre_size()
                            Draw.draw_rect_fast(win.surf, [center[0]-size[0]/2,center[1]-size[1]/2], size, (250,250,20))
                            
                            Draw.draw_rect_fast(win.surf, pos, [self.tile_size, self.tile_size], (200,200,200))
                            Draw.draw_line(win.surf, pos, [pos[0]-objs[y][x][1][0]*self.tile_scaleing*self.tile_size/self.start_tile_size,pos[1]-objs[y][x][1][1]*self.tile_scaleing*self.tile_size/self.start_tile_size], 'red',2)

                            self.obj_name_text.draw(win.surf, [center[0]-size[0]/2+5,center[1]-size[1]/2+0], False, objs[y][x][0], 'white')

    def render_objects(self, layer, surf):
            objs = layer[4]
            
            for y in range(len(objs)):
                for x in range(len(objs[y])):
                    if objs[y][x]!=None and objs[y][x]!=0:
                            pos = [
                                x*self.tile_size,
                                y*self.tile_size
                            ]
                        
                            
                            
                            obj = copy(dt.objects[objs[y][x][0]])
                            obj.scale = self.tile_scaleing*self.tile_size/self.start_tile_size
                            
                            obj.center = [
                                pos[0]+self.tile_size//2+objs[y][x][-1][0]*self.tile_scaleing*self.tile_size/self.start_tile_size,
                                pos[1]+self.tile_size-obj.get_pre_size()[1]//2+objs[y][x][-1][1]*self.tile_scaleing*self.tile_size/self.start_tile_size
                            ]
                            obj.render(surf)
                            #if dut.obj_viev_rect_btn.triger:
                            #    Draw.draw_rect_fast(win.surf, pos, [self.tile_size, self.tile_size], (200,200,200))
                            #    Draw.draw_line(win.surf, pos, [pos[0]-objs[y][x][1][0]*self.tile_scaleing*self.tile_size/self.start_tile_size,pos[1]-objs[y][x][1][1]*self.tile_scaleing*self.tile_size/self.start_tile_size], 'red',2)
                            
    def replace_elemets_in_arr(self, end_arr, copy_arr, start_indexes):
        len_x = len(copy_arr[0])
        len_y = len(copy_arr)
        
        for i in range(start_indexes[1], start_indexes[1]+len_y):
            for j in range(start_indexes[0], start_indexes[0]+len_x):
                try:
                    if end_arr[i][j]==0:
                        end_arr[i][j] = copy_arr[i-start_indexes[1]][j-start_indexes[0]]
                except:...
        
    def get_sub_place(self,start, stop, arr):
        new_arr = []
        for i in range(start[1], stop[1]+1):
            m = copy(arr[i][start[0]:stop[0]+1])
            new_arr.append(m)
        return new_arr
    
    def render_ui(self, surf):
        if self.rendered:
            self.obj_name_text.draw(surf, [win.get_size()[0]-100,5], False, 'Rendered !', (20,240,80))
        else:
            self.obj_name_text.draw(surf, [win.get_size()[0]-100,5], False, 'Not rendered !', (240,20,80))
        
def render_mouse_pos():
    Draw.draw_circle(win.surf, Mouse.pos, 3, COLOR_WHITE)
        


dt = DownTable()
dut = UpDownTable()
gm = GridManager()
Mouse.set_hide()

while win(fps='max',base_color=COLOR_BG):
    GLOBAL_PRESS_WIN = False

    win_size = get_win_size()
    win_center = get_win_center()
    mouse_speed = Mouse.speed
    END_GRID = deepcopy(GRID)
            
            
    gm.update(mouse_speed)
    gm.render_grid(GRID, win.surf, dt.my_tile_sheats_dict)
    gm.render_grasses()
    gm.render_rects()
            
            
            
    dut.render(win.surf)
    dt.render(win.surf, win_size, win_center, mouse_speed)
            
    gm.draw()
    gm.draw_objects()
    gm.draw_grasses()
    gm.draw_rects()
    gm.render_ui(win.surf)
    render_mouse_pos()
            
    ON_THE_BOARD = False
        

    
    
    
    
    
    
    