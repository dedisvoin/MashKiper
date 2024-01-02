from copy import copy
from api.lib import *
from api.libvfx import *
import json


def load_tile_sheats(file_name):
    tsh = DataLoader().Load_from_file_tilesheats(file_name)
    my_tile_sheats_dict = {}
    my_tile_sheats = []
    for i, tile_sheat_name in enumerate( tsh ):

        tlsh2 = copy(tsh[tile_sheat_name])

        my_tile_sheats.append([i+1,tile_sheat_name, tlsh2])
        
        
    for i, tile_sheat_name in enumerate(tsh):
        dummy_ts = TileSheat()
        tile_sheat = tsh[tile_sheat_name]
        dummy_ts.set_tile_sheat(tile_sheat)
        my_tile_sheats_dict[i+1] = copy(dummy_ts)
        
    return my_tile_sheats_dict

def load_objects_sheat(file_name):

        objects = {}

        dobj = DataLoader().Load_from_file_sprites(file_name)
        
        for name in dobj:
            obj_1:Sprite = copy(dobj[name])
            obj_2:Sprite = copy(dobj[name])
            obj_2.set_size([40,40])
            objects[name] = obj_1
            
        return objects

def load_grass_sheat(file_name):
    grasses = {}
    dobj = DataLoader().Load_from_file_grass(file_name)

        
    for name in dobj:
        obj_1:Grass = copy(dobj[name])

        grasses[name] = obj_1
    return grasses

def render_objects(layer ,tile_size, start_tile_size, tile_pixel_count, surf, objects):
    objs = layer[2]
    tile_scaling = start_tile_size/tile_pixel_count
            
    for y in range(len(objs)):
        for x in range(len(objs[y])):
            if objs[y][x]!=None and objs[y][x]!=0:
                    pos = [
                        x*tile_size,
                        y*tile_size
                    ]
                        
                    obj = copy(objects[objs[y][x][0]])
                    obj.scale = tile_scaling*tile_size/start_tile_size
                            
                    obj.center = [
                        pos[0]+tile_size//2+objs[y][x][-1][0]*tile_scaling*tile_size/start_tile_size,
                        pos[1]+tile_size-obj.get_pre_size()[1]//2+objs[y][x][-1][1]*tile_scaling*tile_size/start_tile_size
                    ]
                    if obj.attr == 1:
                        obj.render(surf)

def create_map_surf(tiles_dict, objects_dict, tile_size, map_file, start_tile_size=30, tile_pixel_size=14):
    layers = open(map_file, 'r')
    
    layers = json.load(layers)[1]
    
    layer_dummy = pygame.Surface([len(layers[0][0][0])*tile_size,len(layers[0][0])*tile_size]).convert_alpha()
    layer_dummy.set_alpha(255)
    layer_dummy.set_colorkey((0,0,0))
    for i, grid in enumerate( layers ):
        
        
        g = create_map_surf_by_tilesheats_and_array(tiles_dict, grid[0], tile_size)
    
        layer_dummy.blit(g, [0,0])
        
        render_objects(grid, tile_size,start_tile_size,tile_pixel_size,layer_dummy,objects_dict)
                
    return layer_dummy

def create_collide_space(file_name, tile_size = 20, trenie_vector = Vector2(0.3,1)):
    layers = open(file_name, 'r')
    
    collide_layar_index = json.load(layers)[0]
    layers = open(file_name, 'r')
    collide_layars = json.load(layers)[1]
    collide_map_layers = []
    
    collide_layer = collide_layars[collide_layar_index][0]
    
    
    if len(collide_layars[collide_layar_index][4])==0:
    
        layer_width = len(collide_layer[0])
        layer_height = len(collide_layer)
        collider_y = 0
        for i in range(layer_height):
            collider_start = False
            collider_width = 0
            collider_x = 0
            
            for j in range(layer_width):
                if collide_layer[i][j]!=0 and not collider_start:
                    collider_start = True
                    collider_x = j
                
                
                if collider_start and collide_layer[i][j]==0:
                    collider_start = False
                    
                    
                    collider = Colliders.CRect([collider_x*tile_size, collider_y*tile_size], [collider_width*tile_size, tile_size ], trenie=trenie_vector)
                    collide_map_layers.append(collider)
                    collider_width = 0
                if collider_start:
                    
                    collider_width+=1
            collider_y+=1
            
        return collide_map_layers

    else:
        colliders = collide_layars[collide_layar_index][4]
        for collider in colliders:
            c = Colliders.CRect([collider[0][0]*tile_size, collider[0][1]*tile_size], [collider[1][0]*tile_size, collider[1][1]*tile_size ], trenie=trenie_vector)
            collide_map_layers.append(c)
        return collide_map_layers

def create_map_layer(tiles_dict, objects_dict, tile_size, map_file, start_tile_size=30, tile_pixel_size=14, layer_index=0):
    layers = open(map_file, 'r')
    
    layers = json.load(layers)[1]
    
    layer_dummy = pygame.Surface([len(layers[0][0][0])*tile_size,len(layers[0][0])*tile_size]).convert_alpha()
    layer_dummy.set_alpha(255)
    layer_dummy.set_colorkey((0,0,0))
    grid = layers[layer_index]
    
        
        
    g = create_map_surf_by_tilesheats_and_array(tiles_dict, grid[0], tile_size)
    
    layer_dummy.blit(g, [0,0])
        
    render_objects(grid, tile_size,start_tile_size,tile_pixel_size,layer_dummy,objects_dict)
                
    return layer_dummy

def create_grass_managers(grasses_dict,map_file,tile_size):
    layers = open(map_file, 'r')
    layers = json.load(layers)[1]
    
    gms = []
    
    for layer in layers:
        
        l = layer[3]
        
        for grass in l:
            print(grass)
            using_grasses = [grasses_dict[use_grass] for use_grass in grass[0]]
            gm = GrassManager([grass[1][0][0]*tile_size,(grass[1][0][1]+1)*tile_size],[grass[1][1][0]*tile_size,grass[1][1][1]*tile_size], using_grasses, 5*grass[1][1][0])

            gms.append(gm)
    return gms

def get_object_arr(map_file):
    layers = open(map_file, 'r')
    
    layers = json.load(layers)
    obj_layer_index = layers[0]
    layers = layers[1]
    
    objects = layers[obj_layer_index][2]
    return objects

class Object_construct:
    def __init__(self, name_id, size, startick=True, collider_space=None, max_y_vel = []) -> None:
        self.name_id = name_id
        self.size = size
        self.startick = startick
        if not self.startick:
            self.collider = Colliders.CRect([0,0], self.size, statick=False, max_velosityes_y=max_y_vel)
            collider_space.add(self.collider)
        else:
            self.collider = Colliders.CRect([0,0], self.size, statick=False)
        
        self.using_attr = 'None'
        
        self.sprite:Sprite = None
        
        self.anim_sprites:Dict[AnimatedSprite] = {}
        self.at_anim_sprite = None
        
        self.mirror_x = False
        self.mirror_y = False
        self.radius = math.sqrt((self.size[0]/2**2)+(self.size[1]/2)**2)
        
        self.rendered = True
        
        
        
    def set_mirrors(self):
        for name in self.anim_sprites:
            
            self.anim_sprites[name].mirror_x = self.mirror_x
            self.anim_sprites[name].mirror_y = self.mirror_y
            
        
        if self.sprite is not None:
            self.sprite.mirror_x = self.mirror_x
            self.sprite.mirror_y = self.mirror_y
        
            
    def set_pos(self, pos):
        self.collider.xy = pos
        
    
        
    def set_sprite(self, sprite):
        self.sprite = sprite
        self.using_attr = 'sprite'
    
    def set_animation_sprites(self, animate:AnimatedSprite, name):
        animate.scale = 1
        self.anim_sprites[name] = animate
        self.using_attr = 'animate'
        
    def render(self, global_pos, surf):
        if self.rendered:
            self.set_mirrors()
            
            if self.using_attr == 'sprite':
                self.sprite.center = [self.collider.center_x+int(global_pos[0]), self.collider.center_y+int(global_pos[1])]
                self.sprite.render(surf)
            elif self.using_attr == 'animate':
                
                self.anim_sprites[self.at_anim_sprite].center = [self.collider.center_x+int(global_pos[0]), self.collider.center_y+int(global_pos[1])]
                self.anim_sprites[self.at_anim_sprite].update()
                self.anim_sprites[self.at_anim_sprite].render(surf)
            else:
                Draw.draw_rect(surf, [self.collider.x+global_pos[0], self.collider.y+global_pos[1]], self.collider.wh, 'gray',1)

class Game:
    def __init__(self, win) -> None:
        self.gloabal_pos = [0,0]
        self.render_objects = []
        self.win:Window = win
        
        self.camera = Camera(win)
        self.grass_manager:list[GrassManager] = []
        
        self.scale = 1
        self.delta_scale = 1
        
        self.angle = 0
        self.delta_angle = 0
        
        self.cam_delta = 0.3
        self.cam_zoom_delta = 0.1
        
        
    def set_grass_detect_object(self, obj):
        for gm in self.grass_manager:
            gm.set_grass_collide_obj(obj)
    
        
    def add_render_objects(self, obj, d_pos):
        self.render_objects.append([obj, d_pos])
    
    def set_camera_target(self, target):
        try:
            self.camera.set_target(target.collider)
        except:
            self.camera.set_target(target.pos)   
            
    def set_camera_zoom(self, zoom):
        self.delta_scale = zoom
        
    def set_grass_managers(self,gm):
        self.grass_manager = gm
        
    def set_camera_delta(self, delta):
        self.cam_delta = delta
        
    def set_camere_zoom_delta(self, delta=0.1):
        self.cam_zoom_delta = delta
        
    def camera_update(self):
        self.camera.update(delta= self.cam_delta, global_pos=self.gloabal_pos)
        
        
    def obj_rendering(self, render_arrss=None, render_method=None):
        Draw.draw_rect(self.win.surf, [0,0],self.win.get_size(), (70/2,10,100/2))
        if render_method is not None:
            render_method()
        
        for obj in self.render_objects:
            if type(obj[0]) == pygame.Surface:
                self.win.surf.blit(obj[0], [self.gloabal_pos[0]+obj[1][0],self.gloabal_pos[1]+obj[1][1]])
            elif type(obj[0]) == ParticleSpace:
                obj[0].render(self.gloabal_pos)
            else:
                obj[0].render([self.gloabal_pos[0],self.gloabal_pos[1]], self.win.surf)
                
        if render_arrss is not None:
            for arr in render_arrss:
                for obj in arr:
                    obj.render(self.win.surf, self.gloabal_pos)
            
                
        for gm in self.grass_manager:
            gm.update()
            gm.Render(self.win, self.gloabal_pos)
            
        
        surf = self.win.surf.copy()
        
        
        surf = pygame.transform.scale(surf, [self.win.surf.get_size()[0]*self.scale, self.win.surf.get_size()[1]*self.scale])
        surf = pygame.transform.rotate(surf, self.angle)
        
        
        self.win.surf.blit(surf,[0,0],[(surf.get_width()-self.win.surf.get_width())/2,
                                    (surf.get_height()-self.win.surf.get_height())/2,
                                    self.win.surf.get_width(), 
                                    self.win.surf.get_height()])
        
        self.scale-=(self.scale-self.delta_scale)*self.cam_zoom_delta
        self.angle-=(self.angle-self.delta_angle)*0.1
        if abs(self.angle)<0.5:self.angle = 0
        
        
    
    
    