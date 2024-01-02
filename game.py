from api.lib import *
from api.libvfx import *
from api.gameengine import *

# create game window ----------------------------------------------------------------------------------------------------
mathtab = 4
win = Window(size=[1920//mathtab,1080//mathtab],flag=Flags.WINDOW_RESIZE|pygame.FULLSCREEN|pygame.SCALED|pygame.DOUBLEBUF,pos=[50,50])
# create game window ----------------------------------------------------------------------------------------------------

# load sounds -----------------------------------------------------------------------------------------------------------
sounds = {
    'jump':Sound('sounds\jump.wav'),
    'shoot':Sound('sounds\Shoot.wav'),
    'mash_exp':Sound('sounds\mash_expl.wav'),
    'hit':Sound('sounds\Hit.wav'),
    'kill':Sound('sounds\kill.wav')
}
m = pygame.mixer.Sound('sounds\music.wav')
m.play(-1)
# load sounds -----------------------------------------------------------------------------------------------------------

# load font and create pixel-text ---------------------------------------------------------------------------------------
pixel_font = pygame.font.Font('sounds\Minecraft Seven_2.ttf',8)
count_text = Text(pixel_font,8,'None','white')

pixel_font = pygame.font.Font('sounds\Minecraft Seven_2.ttf',10)
new_level_text = Text(pixel_font,8,'None','white')
# load font and create pixel-text ---------------------------------------------------------------------------------------

# Mouse events listener -------------------------------------------------------------------------------------------------
mouse_events_handler = MouseEventHandler()
mouse_events_handler.AddEvent(Mouse(Mouse.left,Mouse.click_event, 'click'))
mouse_cursor = Sprite('gameres\mouse_cursor.png')
Mouse.set_hide()
# Mouse events listener -------------------------------------------------------------------------------------------------

# Load Sheats -----------------------------------------------------------------------------------------------------------
tile_sheats = load_tile_sheats(r'mapcreatordata\tilesheats.data')
objects_sheats = load_objects_sheat(r'mapcreatordata\objects.data')
grass_sheat = load_grass_sheat('mapcreatordata\grasses.data')
# Load Sheats -----------------------------------------------------------------------------------------------------------

hurt_anim = AnimatedSprite('gameres\hurt_anim.png',5)
hurt_anim.scale = 1
hurt_no = Sprite('gameres\hurt_no.png')

lesson_sprite = AnimatedSprite('gameres\lesson.png',30)
lesson_sprite.scale = 1

bee_anim = AnimatedSprite(r'gameres\bee\bee_anim.png',3)
bee_anim.scale = 1

# Set global gravity ----------------------------------------------------------------------------------------------------
Colliders.GRAVITY = Vector2(0,0.4)
# Set global gravity ----------------------------------------------------------------------------------------------------

# Bee classes -----------------------------------------------------------------------------------------------------------
class BeeHouse:
    def __init__(self, pos) -> None:
            self.pos = pos
            self.animate = AnimatedSprite(r'gameres\bee\bee_house_anim.png',5)
            self.animate.scale = 1
            self.timer = 1
            
    def render(self, surf, gloabal_pos):
            self.timer+=1
            self.animate.center = [self.pos[0]+int(gloabal_pos[0])-8,self.pos[1]+int(gloabal_pos[1]-7)]
            self.animate.render(surf)
            self.animate.update()
            
    def update(self, mash_gun_bullets, space, spavn,player):
            if distance(player.collider.center,self.pos)<200:
                if self.timer%200==0:
                    spavn._pos = self.pos
                    space.add(bee_boom_p2, spavn, 10,1)
                    
                    for i in range(random.randint(5,15)):
                        mash_gun_bullets.append(Bee(copy([self.pos[0]-8,self.pos[1]-7])))
                        print('add')

class Bee:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.speed = Vector2(random.randint(-100,100),random.randint(-100,100))
        self.speed.normalyze()
        self.speed*=10
        self.life_time = 300+random.randint(0,50)
        self.delta = 0.6
        
    def render(self, surf, gloabal_pos):
        self.life_time-=1
        pos = [self.pos[0]+gloabal_pos[0],self.pos[1]+gloabal_pos[1]]
        
        #Draw.draw_circle(surf, pos, 5,'red')
        bee_anim.mirror_x = True
        if self.speed.x<0:
            bee_anim.mirror_x = False
        bee_anim.center = pos
        bee_anim.update()
        bee_anim.render(surf)
        
    def update(self):
        
        self.speed*=self.delta
        self.pos[0]+=self.speed.x
        self.pos[1]+=self.speed.y
# Bee classes -----------------------------------------------------------------------------------------------------------


# Mash class ------------------------------------------------------------------------------------------------------------
class Mash:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.animate = AnimatedSprite('gameres\mash\mashrom_anim.png',5)
        self.animate.scale = 1
        self.timer = 0
        
    def render(self, surf, gloabal_pos):
        self.timer+=1
        self.animate.center = [self.pos[0]+int(gloabal_pos[0])-7,self.pos[1]+int(gloabal_pos[1]-4)]
        self.animate.render(surf)
        self.animate.update()
    
class Gun_Mash:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.animate = AnimatedSprite('gameres\gunmash\mash_gun_anim.png',5)
        self.animate.scale = 1
        self.timer = 1
        
    def render(self, surf, gloabal_pos):
        self.timer+=1
        self.animate.center = [self.pos[0]+int(gloabal_pos[0])-8,self.pos[1]+int(gloabal_pos[1]-7)]
        self.animate.render(surf)
        self.animate.update()
        
    def update(self, mash_gun_bullets, space, spavn,player):
        if distance(player.collider.center,self.pos)<200:
            if self.timer%200==0:
                spavn._pos = self.pos
                space.add(mash_gun_boom_p2, spavn, 10,1)
                
                for i in range(random.randint(1,2)):
                    mash_gun_bullets.append(Gun_Mash_Bullet(copy([self.pos[0]-8,self.pos[1]-7])))
mash_bullet_anim = AnimatedSprite('gameres\gunmash\mash_gun_bull_anim.png',20)
mash_bullet_anim.scale = 1

class Gun_Mash_Bullet:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.speed = Vector2(random.randint(-100,100),random.randint(-100,100))
        self.speed.normalyze()
        self.speed*=3
        self.life_time = 300
        
    def render(self, surf, gloabal_pos):
        self.life_time-=1
        pos = [self.pos[0]+gloabal_pos[0],self.pos[1]+gloabal_pos[1]]
        
        #Draw.draw_circle(surf, pos, 5,'red')
        mash_bullet_anim.center = pos
        mash_bullet_anim.update()
        mash_bullet_anim.render(surf)
        
    def update(self):
        self.speed.normalyze()
        self.speed*=3
        self.pos[0]+=self.speed.x
        self.pos[1]+=self.speed.y
    
# Mash class ------------------------------------------------------------------------------------------------------------

# Bullet class ----------------------------------------------------------------------------------------------------------
bullet_sprite = Sprite(r'gameres\bullet.png',False,True)
class Bullet:
    def __init__(self, pos, speed:Vector2) -> None:
        self.pos = pos
        self.speed = speed
        self.speed.normalyze()
        self.speed*=-8
        self.angle = self.speed.get_angle()-90
        
        self.life_time = 400
        
    def render(self, surf, gloabal_pos):
        self.life_time-=1
        bullet_sprite.center = [self.pos[0]+gloabal_pos[0],self.pos[1]+gloabal_pos[1]]
        bullet_sprite.angle = self.angle
        self.pos[0]+=self.speed.x
        self.pos[1]+=self.speed.y
        bullet_sprite.render(surf)
# Bullet class ----------------------------------------------------------------------------------------------------------

# Player dash particle --------------------------------------------------------------------------------------------------
p = Particle()
p.RADIUS = 3
p.RADIUS_RANDOMER = 0
p.RADIUS_RESIZE = -0.3
p.RESIZE_START_TIME = 0
p.SPEED = Vector2(0,0)
p.COLOR = (49,13,113)
p.LINES = True


p_kill = Particle()
p_kill.RADIUS = 3
p_kill.RADIUS_RANDOMER = 0
p_kill.RADIUS_RESIZE = -0.01
p_kill.RESIZE_START_TIME = 0
p_kill.SPEED = Vector2(0,2)
p_kill.SPEED_RANDOMER = 3
p_kill.SPEED_DURATION = 70
p_kill.SPEED_ANGLE = -90
p_kill.COLOR = (49,13,113)
p_kill.SHADOWING = True
p_kill.COLLIDER_BOUNSING = Vector2(0.6,0.6)
p_kill.SHADOW_DX = 3
p_kill.SHADOW_DY = 3

# Player dash particle --------------------------------------------------------------------------------------------------

# Player dash particle --------------------------------------------------------------------------------------------------
p_mash_bull = Particle()
p_mash_bull.RADIUS = 2
p_mash_bull.RADIUS_RANDOMER = 0
p_mash_bull.RADIUS_RESIZE = -0.1
p_mash_bull.RADIUS_RANDOMER = 3
p_mash_bull.RESIZE_START_TIME = 0
p_mash_bull.SPEED = Vector2(0,0.5)
p_mash_bull.SPEED_DURATION = 180
p_mash_bull.COLOR_FROM_DICT = [
    (128, 29, 211),
    (213, 170, 249)
]
p_mash_bull.SHADOWING = True
p_mash_bull.SHADOW_DX = 3
p_mash_bull.SHADOW_DY = 3

# Player dash particle --------------------------------------------------------------------------------------------------

# Mash particle ---------------------------------------------------------------------------------------------------------
mash_p = Particle()
mash_p.RADIUS = 1
mash_p.RADIUS_RANDOMER= 2
mash_p.RADIUS_RESIZE = -0.1
mash_p.RESIZE_START_TIME = 50
mash_p.SPEED = Vector2(0,1)
mash_p.SPEED_RANDOMER = 5
mash_p.SPEED_DURATION = 45
mash_p.SPEED_ANGLE=-90
mash_p.COLOR = (120,46,255)
mash_p.COLOR_FROM_DICT = [
    (120,46,255),
    (91,27,206)
]
mash_p.SHADOWING = True
mash_p.COLLIDER_BOUNSING = Vector2(0.4,0.4)
mash_p.SHADOW_DX = 3
mash_p.SHADOW_DY = 3
# Mash particle ---------------------------------------------------------------------------------------------------------

# Mash boom particle ----------------------------------------------------------------------------------------------------
mash_gun_boom_p = Particle()
mash_gun_boom_p.RADIUS = 2
mash_gun_boom_p.RADIUS_RANDOMER= 4
mash_gun_boom_p.RADIUS_RESIZE = -0.4
mash_gun_boom_p.RESIZE_START_TIME = 100
mash_gun_boom_p.SPEED = Vector2(0,1)
mash_gun_boom_p.SPEED_RANDOMER = 5
mash_gun_boom_p.SPEED_DURATION = 180
mash_gun_boom_p.SPEED_ANGLE=-90
mash_gun_boom_p.COLOR = (120,46,255)
mash_gun_boom_p.COLOR_FROM_DICT = [
    (128, 29, 211),
    (213, 170, 249)
]
mash_gun_boom_p.SHADOWING = True
mash_gun_boom_p.COLLIDER_BOUNSING = Vector2(0.4,0.4)
mash_gun_boom_p.SPEED_FRICTION = 0.95
mash_gun_boom_p.TILE_USING = True
mash_gun_boom_p.TILE_POINT_SET_TIME = 3
mash_gun_boom_p.PULSING = True
mash_gun_boom_p.SHADOW_DX = 3
mash_gun_boom_p.SHADOW_DY = 3


mash_gun_boom_p2 = Particle()
mash_gun_boom_p2.RADIUS = 1
mash_gun_boom_p2.RADIUS_RANDOMER= 5
mash_gun_boom_p2.RADIUS_RESIZE = -0.4
mash_gun_boom_p2.RESIZE_START_TIME = 100
mash_gun_boom_p2.SPEED = Vector2(0,1)
mash_gun_boom_p2.SPEED_RANDOMER = 5
mash_gun_boom_p2.SPEED_DURATION = 180
mash_gun_boom_p2.SPEED_ANGLE=-90
mash_gun_boom_p2.COLOR = (120,46,255)
mash_gun_boom_p2.COLOR_FROM_DICT = [
    (128, 29, 211),
    (213, 170, 249)
]
mash_gun_boom_p2.SHADOWING = True
mash_gun_boom_p2.COLLIDER_BOUNSING = Vector2(0.4,0.4)
mash_gun_boom_p2.SPEED_FRICTION = 0.95
mash_gun_boom_p2.TILE_USING = True
mash_gun_boom_p2.TILE_POINT_SET_TIME = 3
mash_gun_boom_p2.PULSING = True
mash_gun_boom_p2.SHADOW_DX = 3
mash_gun_boom_p2.SHADOW_DY = 3
# Mash boom particle ----------------------------------------------------------------------------------------------------

bee_boom_p2 = Particle()
bee_boom_p2.RADIUS = 1
bee_boom_p2.RADIUS_RANDOMER= 5
bee_boom_p2.RADIUS_RESIZE = -0.4
bee_boom_p2.RESIZE_START_TIME = 50
bee_boom_p2.SPEED = Vector2(0,1)
bee_boom_p2.SPEED_RANDOMER = 5
bee_boom_p2.SPEED_DURATION = 180
bee_boom_p2.SPEED_ANGLE=-90
bee_boom_p2.COLOR = (120,46,255)
bee_boom_p2.COLOR_FROM_DICT = [
    (219,140,40),
    (255,194,116)
]
bee_boom_p2.SHADOWING = True
bee_boom_p2.COLLIDER_BOUNSING = Vector2(0.4,0.4)
bee_boom_p2.SPEED_FRICTION = 0.95
bee_boom_p2.TILE_USING = True
bee_boom_p2.TILE_POINT_SET_TIME = 50
bee_boom_p2.TILE_POINTS_SIZE_RESIZE = -0.2
bee_boom_p2.PULSING = True
bee_boom_p2.SHADOW_DX = 3
bee_boom_p2.SHADOW_DY = 3
bee_boom_p2.GRAVITY_VECTOR = [0,0.1]

bee_kill_p = Particle()
bee_kill_p.RADIUS = 1
bee_kill_p.RADIUS_RANDOMER= 3
bee_kill_p.RADIUS_RESIZE = -0.4
bee_kill_p.RESIZE_START_TIME = 50
bee_kill_p.SPEED = Vector2(0,1)
bee_kill_p.SPEED_RANDOMER = 5
bee_kill_p.SPEED_DURATION = 180
bee_kill_p.SPEED_ANGLE=-90
bee_kill_p.COLOR = (120,46,255)
bee_kill_p.COLOR_FROM_DICT = [
    (219,140,40),
    (255,194,116)
]
bee_kill_p.SHADOWING = True
bee_kill_p.COLLIDER_BOUNSING = Vector2(0.4,0.4)
bee_kill_p.SPEED_FRICTION = 0.95
bee_kill_p.TILE_USING = True
bee_kill_p.TILE_POINT_SET_TIME = 2
bee_kill_p.TILE_POINTS_SIZE_RESIZE = -0.2
bee_kill_p.SHADOW_DX = 3
bee_kill_p.SHADOW_DY = 3
bee_kill_p.GRAVITY_VECTOR = [0,0.1]

# Mash gun boom particle ----------------------------------------------------------------------------------------------------
mash_boom_p = Particle()
mash_boom_p.RADIUS = 3
mash_boom_p.RADIUS_RANDOMER= 7
mash_boom_p.RADIUS_RESIZE = -0.4
mash_boom_p.RESIZE_START_TIME = 100
mash_boom_p.SPEED = Vector2(0,1)
mash_boom_p.SPEED_RANDOMER = 5
mash_boom_p.SPEED_DURATION = 180
mash_boom_p.SPEED_ANGLE=-90
mash_boom_p.COLOR = (120,46,255)
mash_boom_p.COLOR_FROM_DICT = [
    (120,46,255),
    (91,27,206)
]
mash_boom_p.SHADOWING = True
mash_boom_p.COLLIDER_BOUNSING = Vector2(0.4,0.4)
mash_boom_p.SPEED_FRICTION = 0.9
mash_boom_p.SHADOW_DX = 3
mash_boom_p.SHADOW_DY = 3
# Mash gun boom particle ----------------------------------------------------------------------------------------------------

# Gun particle N1 -------------------------------------------------------------------------------------------------------
gun_p = Particle()
gun_p.SHAPE = particle_shapes.IMAGE
gun_p.SPRITE = Sprite('gameres\particle_point.png', False, True)
gun_p.SPRITE_START_SCALE = 0.5
gun_p.RADIUS = 3
gun_p.SPRITE_ANGLE_TYPE = sprite_angle_types.TO_VECTOR
gun_p.SPRITE_ADD_ANGLE = -45
gun_p.RADIUS_RANDOMER = 0
gun_p.SPRITE_SCALE_RESIZE = -0.1
gun_p.SPEED_FRICTION = 0.8
gun_p.RESIZE_START_TIME = 0
gun_p.SPEED = Vector2(0,5)
gun_p.SPEED_DURATION = 20
gun_p.COLOR = (49,13,113)
gun_p.SPEED_RANDOMER = 5
gun_p.RESIZE_START_TIME = 40
# Gun particle N1 -------------------------------------------------------------------------------------------------------

# Gun particle N2 -------------------------------------------------------------------------------------------------------
gun_p_2 = Particle()
gun_p_2.SHAPE = particle_shapes.IMAGE
gun_p_2.SPRITE = Sprite('gameres\particle_point.png', False, True)
gun_p_2.SPRITE_START_SCALE = 0.5
gun_p_2.SPRITE_SCALE_RANDOMER = 2
gun_p_2.RADIUS = 3
gun_p_2.SPRITE_ANGLE_TYPE = sprite_angle_types.TO_VECTOR
gun_p_2.SPRITE_ADD_ANGLE = -45
gun_p_2.RADIUS_RANDOMER = 0
gun_p_2.SPRITE_SCALE_RESIZE = -0.1
gun_p_2.SPEED_FRICTION = 0.9
gun_p_2.SPEED = Vector2(0,5)
gun_p_2.SPEED_DURATION = 180
gun_p_2.COLOR = (49,13,113)
gun_p_2.SPEED_RANDOMER = 20
gun_p_2.RESIZE_START_TIME = 100
# Gun particle N1 -------------------------------------------------------------------------------------------------------


class ColoredCircle:
    def __init__(self, pos ,color, start_width, rad_sum, width_min) -> None:
        self.pos = pos
        self.color = color
        self.start_width = start_width
        
        self.rad_sum = rad_sum
        self.wid_min = width_min
        
        self.radius = 0
        
    def render(self, surf, global_pos):
        pos = [
            self.pos[0]+global_pos[0],
            self.pos[1]+global_pos[1]
        ]
        if int(self.start_width)!=0:
            Draw.draw_circle(surf, [pos[0]+3,pos[1]+3], int(self.radius), 'black', int(self.start_width))
            Draw.draw_circle(surf, pos, int(self.radius), self.color, int(self.start_width))
        self.radius+=self.rad_sum
        self.start_width-=self.wid_min


class Scene:
    def __init__(self, scene_file, lm, time) -> None:
        self.scene_file = scene_file
        self.spedrun_time = time
        
        self.lm = lm
        
        # create game level object --------------------------------------------------------------------------------------
        self.level_object = Game(win)
        self.level_object.set_camera_delta(1)
        # create game level object --------------------------------------------------------------------------------------
        
        
        # create gun objects --------------------------------------------------------------------------------------------
        self.gun = Object_construct('gun',[1,1], True)
        self.gun.set_sprite(Sprite('gameres\gun.png',False, False))
        self.gun_kd = 0
        # create gun objects --------------------------------------------------------------------------------------------
        
        
        # create mash-out objects ---------------------------------------------------------------------------------------
        self.mash_out_obj = Sprite('gameres\mash_out_obj.png')
        # create mash-out objects ---------------------------------------------------------------------------------------
        
        
        # create level map ----------------------------------------------------------------------------------------------
        self.surf = None
        self.bg_surf = None
        self.create_level_surf(self.scene_file)
        # create level map ----------------------------------------------------------------------------------------------
        
        
        # create collide map --------------------------------------------------------------------------------------------
        self.collider_space = Colliders(win.surf)
        self.create_level_collide_surf(self.scene_file)
        # create collide map --------------------------------------------------------------------------------------------
        
        
        # create player objects -----------------------------------------------------------------------------------------
        self.hp_count = 3
        self.obj_player = Object_construct('player', [8,12], False, self.collider_space, [3.5])
        self.obj_player.set_pos([100,0])
        self.obj_player.set_animation_sprites(AnimatedSprite(r'gameres\stay_anim.png',10),'stay')
        self.obj_player.set_animation_sprites(AnimatedSprite(r'gameres\run_anim.png',10),'run')
        self.obj_player.at_anim_sprite = 'stay'
        # create player objects -----------------------------------------------------------------------------------------
        
        
        # create grass manager ------------------------------------------------------------------------------------------
        self.grass_manager = None
        self.create_level_grass_manager(self.scene_file)
        # create grass manager ------------------------------------------------------------------------------------------
        
        
        # create objects -------------------------------------------------------------------------------------------
        self.all_objects_in_the_map = self.get_all_objects_for_map(self.scene_file)
        self.mashs = []
        self.bullets = []
        self.gun_mashs = []
        self.gun_mashs_bullets = []
        
        self.bee_houses = []
        self.bees = []
        for y in range(len(self.all_objects_in_the_map)):
            for x in range(len(self.all_objects_in_the_map[y])):
                if type(self.all_objects_in_the_map[y][x])==list and self.all_objects_in_the_map[y][x][0] == 'mash':
                    mash = Mash([(x+1)*14,(y+1)*14])
                    self.mashs.append(mash)
                if type(self.all_objects_in_the_map[y][x])==list and self.all_objects_in_the_map[y][x][0] == 'mash_gun':
                    mash = Gun_Mash([(x+1)*14,(y+1)*14])
                    self.gun_mashs.append(mash)
                if type(self.all_objects_in_the_map[y][x])==list and self.all_objects_in_the_map[y][x][0] == 'bee_house':
                    mash = BeeHouse([(x+1)*14,(y+1)*14])
                    self.bee_houses.append(mash)
                if type(self.all_objects_in_the_map[y][x])==list and self.all_objects_in_the_map[y][x][0] == 'player':
                    self.obj_player.set_pos([(x+1)*14,(y+1)*14])
        self.mashs_start_count = len(self.mashs)
        self.mashs_kill_count = 0
        self.mash_cam_timer = 0
        self.mash_collide = None
        # create objects -------------------------------------------------------------------------------------------
        
        
        # Start and stop animates ---------------------------------------------------------------------------------------
        self.anim_delta = 1
        self.end_level_anim = 1
        self.new_level_anim_p = 1
        self.reloading = False
        # Start and stop animates ---------------------------------------------------------------------------------------
        
        
        # attrs ---------------------------------------------------------------------------------------------------------
        self.timer = 0
        self.new = False
        self.started = False
        self.killed_object = None
        # attrs ---------------------------------------------------------------------------------------------------------
        
        
        # Scene Init ----------------------------------------------------------------------------------------------------
        self.particle_systems_init()
        self.add_all_object_in_scene()
        # Scene Init ----------------------------------------------------------------------------------------------------
        
        
        self.bg_circles = []
        for i in range(100):
            self.bg_circles.append([
                [random.randint(50,win.surf.get_width()-50),random.randint(50,win.surf.get_height()-50)],
                random.randint(10,30),
                [random.randint(-100,100)/100,random.randint(-100,100)/100],
                
            ])
            
        
        self.colored_circles = []
        self.level_object.scale = 5
        
        
        
    #? Create level surf -------------------------------------------------------------------------------------------------
    def create_level_surf(self, scene_file):
        self.surf = create_map_surf(tile_sheats,objects_sheats,14,scene_file)
        self.bg_surf = self.surf.copy()
        arr = pygame.surfarray.pixels3d(self.bg_surf)
        arr[:,:,0] = 0
        arr[:,:,1] = 0
        arr[:,:,2] = 0
    # Create level surf -------------------------------------------------------------------------------------------------
    
    
    #? Create collide surf -----------------------------------------------------------------------------------------------
    def create_level_collide_surf(self, scene_file):
        self.collide_surf = create_collide_space(scene_file,14)
        self.collider_space.adds(self.collide_surf)
    # Create collide surf -----------------------------------------------------------------------------------------------
        
    def create_level_grass_manager(self, scene_file):
        self.grass_manager = create_grass_managers(grass_sheat, scene_file, 14)
        self.level_object.set_grass_managers(self.grass_manager)
        self.level_object.set_grass_detect_object(self.obj_player)
        
    def get_all_objects_for_map(self, scene_file):
        return get_object_arr(scene_file)
    
    def particle_systems_init(self):
        self.p_space = ParticleSpace([0,0],[0,0],win)
        self.p_space_2 = ParticleSpace([0,0],[0,0],win)
        self.p_space_3 = ParticleSpace([0,0],[0,0],win)
        self.p_space_3.set_partsim_space(self.collider_space)
        self.p_spavn = ParticleSpawner()

    def add_all_object_in_scene(self):
        self.level_object.set_camera_target(self.obj_player)
        self.level_object.set_camere_zoom_delta(0.01)
        self.level_object.set_camera_zoom(1)

        self.level_object.add_render_objects(self.bg_surf.copy(),[3,3]) # surf size [2000,2000]
        self.level_object.add_render_objects(self.surf,[0,0])
        self.level_object.add_render_objects(self.p_space,[0,0])
        self.level_object.add_render_objects(self.obj_player,[0,0])


        self.level_object.add_render_objects(self.gun,[0,0])
        self.level_object.add_render_objects(self.p_space_2,[0,0])
        self.level_object.add_render_objects(self.p_space_3,[0,0])
        
    def reload(self):
        if round(self.end_level_anim,2)==-0:
            self = self.__init__(self.scene_file,self.lm,self.spedrun_time)
            
    def new_level(self):
        if round(self.new_level_anim_p,2)==0:
            self.lm.scene_index+=1
        
    def start_level_anim(self):
        Draw.draw_rect(win.surf, [0,0],[win.surf.get_width(),win.surf.get_height()/2*self.anim_delta], 'black')
        Draw.draw_rect(win.surf, [0,win.surf.get_height()-win.surf.get_height()/2*self.anim_delta+1],[win.surf.get_width(),win.surf.get_height()/2*self.anim_delta], 'black')
        if self.anim_delta>0:
            self.anim_delta-=0.03
            
    def stop_level_anim(self):
        Draw.draw_rect(win.surf, [0,0],[win.surf.get_width(),win.surf.get_height()/2*(1-self.end_level_anim+0.02)], 'black')
        Draw.draw_rect(win.surf, [0,win.surf.get_height()-win.surf.get_height()/2*(1-self.end_level_anim+0.02)+1],[win.surf.get_width(),win.surf.get_height()/2*(1-self.end_level_anim+0.02)], 'black')
        if self.end_level_anim>0:
            self.end_level_anim-=0.01
            
    def new_level_anim(self):
        Draw.draw_rect(win.surf, [0,0],[win.surf.get_width(),win.surf.get_height()/2*(1-self.new_level_anim_p+0.02)], 'black')
        Draw.draw_rect(win.surf, [0,win.surf.get_height()-win.surf.get_height()/2*(1-self.new_level_anim_p+0.02)+1],[win.surf.get_width(),win.surf.get_height()/2*(1-self.new_level_anim_p+0.02)], 'black')
        if self.new_level_anim_p>0:
            self.new_level_anim_p-=0.02
        self.level_object.scale+=0.1
            
    def render_hp(self):
        pos = [win.surf.get_width()/2-13*3/2,win.surf.get_height()-10+3]
        hurt_anim.update()
        c = [win.surf.get_width()/2,win.surf.get_height()+3]
        Draw.draw_polygone(win.surf,[
            [c[0]-50,c[1]],
            [c[0]+50,c[1]],
            
            [c[0]+30,c[1]-22],
            [c[0]-30,c[1]-22],
        ], 'black', outline=[(30,30,30),1])
        for i in range(3):
            hurt_no.center = [pos[0]+i*20,pos[1]]
            hurt_no.render(win.surf)
        for i in range(self.hp_count):
            hurt_anim.center = [pos[0]+i*20,pos[1]]
            hurt_anim.render(win.surf)
            
    def render_lesson(self):
        if self.lm.scene_index == 0 and not self.started:
            pos = [win.surf.get_width()/2, win.surf.get_height()/2+50]
            lesson_sprite.center = pos
            lesson_sprite.render(win.surf)
            lesson_sprite.update()
            count_text.draw(win.surf, [pos[0]-3,pos[1]+20],False, 'shoot', (255,255,255))
            self.mash_out_obj.center = [pos[0]-18,pos[1]+28]
            self.mash_out_obj.render(win.surf)
        
    #def render_bg(self):
    #    for i in range(15):
    #        Draw.draw_aline(win.surf, [i*50-(self.level_object.scale-1)*100-self.level_object.camera.shake_vector.x*5,0],[i*50+(self.level_object.scale-1)*100-self.level_object.camera.shake_vector.x*5,win.surf.get_height()], (70/3,10/3,100/3), 16)
        
    def render_bg(self):
        for c in self.bg_circles:
            Draw.draw_circle(win.surf, [c[0][0]+self.level_object.camera.shake_vector.x*5,c[0][1]+self.level_object.camera.shake_vector.y*5], c[1], (70/3,10/3,100/3), 5)
            c[0][0]+=c[2][0]
            c[0][1]+=c[2][1]
            if c[0][0]+c[1]>win.surf.get_width() or c[0][0]-c[1]<0: c[2][0]*=-1
            if c[0][1]+c[1]>win.surf.get_height() or c[0][1]-c[1]<0: c[2][1]*=-1
        #for i in range(7):
        #    Draw.draw_aline(win.surf, [0,i*50-(self.level_object.scale-1)*100-self.level_object.camera.shake_vector.x*5],[win.surf.get_width(),i*50+(self.level_object.scale-1)*100-self.level_object.camera.shake_vector.x*5], (70/3,10/3,100/3), 32)
        
    def loop(self):
        # gun kd update  ---------------------------------------------------------------------------------------------------
        if self.gun_kd<100:
            self.gun_kd+=1
        # gun kd update  ---------------------------------------------------------------------------------------------------
        
        
        # timer update -----------------------------------------------------------------------------------------------------
        if self.mashs_start_count != self.mashs_kill_count and self.started:
            self.timer+=1
        # timer update -----------------------------------------------------------------------------------------------------

        # mouse events update ----------------------------------------------------------------------------------------------
        mouse_events_handler.EventsUpdate()
        # mouse events update ----------------------------------------------------------------------------------------------
        
        
        # camera update ----------------------------------------------------------------------------------------------------
        self.level_object.camera_update()
        # camera update ----------------------------------------------------------------------------------------------------
        
        
        # gun update -------------------------------------------------------------------------------------------------------
        self.gun.set_pos(self.obj_player.collider.center)
        self.gun.sprite.angle = angle_to_float(self.gun.collider.center, 
                                                [Mouse.pos[0]-self.level_object.gloabal_pos[0]
                                                ,Mouse.pos[1]-self.level_object.gloabal_pos[1]])-90
        if self.gun.collider.center_x>Mouse.pos[0]-self.level_object.gloabal_pos[0]:
            self.gun.mirror_y = True
            self.obj_player.mirror_x = True
        else:
            self.gun.mirror_y = False
            self.obj_player.mirror_x = False
        # gun update -------------------------------------------------------------------------------------------------------
        
        
        # gun mashs update -------------------------------------------------------------------------------------------------
        if self.mashs_start_count!=self.mashs_kill_count and self.started:
            for gun_mash in self.gun_mashs:
                gun_mash.update(self.gun_mashs_bullets, self.p_space_2,self.p_spavn,self.obj_player )
        self.gun_mashs_bullets = list(filter(lambda elem: elem.life_time>0, self.gun_mashs_bullets))
        # gun mashs update -------------------------------------------------------------------------------------------------
        
        # bee house update -------------------------------------------------------------------------------------------------
        bee_zlost = False
        bee_zlosts = []
        if self.mashs_start_count!=self.mashs_kill_count and self.started:
            for bee_h in self.bee_houses:
                bee_h.update(self.bees, self.p_space_2,self.p_spavn,self.obj_player )
                if distance(self.obj_player.collider.center, bee_h.animate.center)<200:
                    bee_zlost = True
                    bee_zlosts.append((1-1/distance(self.obj_player.collider.center, bee_h.animate.center)/200)/1.4)
                    
        if bee_zlost:
            bes_z = max(bee_zlosts)
            for bee in self.bees:
                bee.delta = bes_z
        else:
            for bee in self.bees:
                bee.delta = 0.6
        #self.bees = list(filter(lambda elem: elem.life_time>0, self.bees))
        for i, bee in enumerate(self.bees):
            if bee.life_time<=0:
                self.p_spavn._pos = bee.pos
                self.p_space_2.add(bee_kill_p, self.p_spavn, 5, 1)
                del self.bees[i]
                break
        # bee house update -------------------------------------------------------------------------------------------------
            
        
        # particle systems update ------------------------------------------------------------------------------------------
        self.p_space.tick()
        self.p_space_2.tick()
        self.p_space_3.tick()
        self.collider_space.update()
        # particle systems update ------------------------------------------------------------------------------------------
        
        
        # player movements -------------------------------------------------------------------------------------------------
        if self.obj_player.rendered:
            self.p_spavn._pos = copy([self.obj_player.collider.center[0],self.obj_player.collider.center[1]+3])
            if round(self.obj_player.collider._speed.lenght) !=0:
                self.p_space.add(p, self.p_spavn, 1,1)
            if self.obj_player.collider.get_collides()['down'] and round(self.obj_player.collider._speed.x) !=0:
                self.obj_player.at_anim_sprite = 'run'
                self.p_space.add(p, self.p_spavn, 1, 1)
            else:
                self.obj_player.at_anim_sprite = 'stay'
            
            if Keyboard.key_pressed('up') and self.obj_player.collider.get_collides()['down']:
                self.obj_player.collider._speed.y = -7
                sounds['jump'].play()
                self.started = True
            if Keyboard.key_pressed('left'):
                self.obj_player.collider._speed.x = -2
                self.started = True
            if Keyboard.key_pressed('right'):
                self.started = True
                self.obj_player.collider._speed.x = 2
                
        self.level_object.set_camere_zoom_delta(0.05)
        self.obj_player.collider._speed.x*=0.9
        if self.obj_player.collider.y>800: self.obj_player.collider.y = 0
        # player movements -------------------------------------------------------------------------------------------------
            
        
        # player shooting --------------------------------------------------------------------------------------------------
        if mouse_events_handler.GetEventById('click') and self.gun_kd == 100:
            sounds['shoot'].play()
            vec = Vector2.Normal(self.obj_player.collider.center,
                                                                [Mouse.pos[0]-self.level_object.gloabal_pos[0]
                                                                ,Mouse.pos[1]-self.level_object.gloabal_pos[1]])
            otdacha = copy(vec)
            otdacha.normalyze()
            otdacha*=6
            self.obj_player.collider._speed+=otdacha
            self.bullets.append(Bullet(self.obj_player.collider.center, vec))
            self.gun_kd = 0
        # player shooting --------------------------------------------------------------------------------------------------
            
        
        # mashs pulsing ----------------------------------------------------------------------------------------------------
        for i, mash in enumerate(self.mashs):
            if mash.timer%80==0:
                self.p_spavn._pos = [mash.pos[0]-7,mash.pos[1]-4.5-10]
                self.p_space_3.add(mash_p, self.p_spavn, 2,1)
        # mashs pulsing ----------------------------------------------------------------------------------------------------
                
                
        #? bullet triggered flag
        in_circle = False
        #? bullet triggered flag
        
        # bullet updates ---------------------------------------------------------------------------------------------------
        for i ,bullet in enumerate( self.bullets ):
            # bullet update with default mashs -----------------------------------------------------------------------------
            for k, mash in  enumerate(self.mashs):
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<50:
                    
                    self.mash_collide = mash
                    self.mash_cam_timer = 20
                    in_circle = True
                
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<10:
                    self.p_spavn._pos = bullet.pos
                    self.level_object.camera.set_shake_amplitude(15)
                    sounds['mash_exp'].play()
                    gun_p.SPEED_ANGLE = 180-bullet.angle
                    self.p_space_2.add(gun_p, self.p_spavn, 10, 1)
                    self.mashs_kill_count+=1
                    self.p_space_2.add(mash_boom_p, self.p_spavn, 10,1)
                    
                    self.colored_circles.append(ColoredCircle(mash.pos, (91,27,206),10, 2,0.3))
                    
                    self.p_space_3.add(mash_p, self.p_spavn, 10,1)
                    del self.mashs[k]
                    break
            # bullet update with default mashs -----------------------------------------------------------------------------
            
            
            # bullet update with gun mashs ---------------------------------------------------------------------------------
            for kk, mash in  enumerate(self.gun_mashs):
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<50:
                    
                    self.mash_collide = mash
                    self.mash_cam_timer = 20
                    in_circle = True
                
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<10:
                    self.p_spavn._pos = bullet.pos
                    sounds['mash_exp'].play()
                    gun_p.SPEED_ANGLE = 180-bullet.angle
                    self.p_space_2.add(gun_p, self.p_spavn, 10, 1)
                    self.level_object.camera.set_shake_amplitude(15)
                    
                    self.colored_circles.append(ColoredCircle(mash.pos, (128,29,211),30, 2,0.6))
                    
                    self.p_space_2.add(mash_gun_boom_p, self.p_spavn, 20,1)
                    del self.gun_mashs[kk]
                    break
            # bullet update with gun mashs ---------------------------------------------------------------------------------
            
            for kk, mash in  enumerate(self.bee_houses):
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<50:
                    
                    self.mash_collide = mash
                    self.mash_cam_timer = 20
                    in_circle = True
                
                if distance(bullet.pos, [mash.pos[0]-7,mash.pos[1]-4.5])<10:
                    self.p_spavn._pos = bullet.pos
                    sounds['mash_exp'].play()
                    gun_p.SPEED_ANGLE = 180-bullet.angle
                    self.p_space_2.add(gun_p, self.p_spavn, 10, 1)
                    self.level_object.camera.set_shake_amplitude(15)
                    
                    self.p_space_2.add(bee_boom_p2, self.p_spavn, 20,1)
                    self.colored_circles.append(ColoredCircle(mash.pos, (255,194,116),10, 2,0.1))
                    for i in range(10+random.randint(0,10)):
                        self.bees.append(Bee(copy(mash.pos)))
                    del self.bee_houses[kk]
                    break
            
                    
            #? dell flag
            dell = False
            #? dell flag
            
            
            # bullet collide with map --------------------------------------------------------------------------------------
            for collide in self.collide_surf:
                
                if in_rect(collide.xy, collide.wh, bullet.pos):
                    self.p_spavn._pos = bullet.pos
                    gun_p.SPEED_ANGLE = 180-bullet.angle
                    self.p_space_2.add(gun_p, self.p_spavn, 10, 1)
                    self.p_space_2.add(gun_p_2, self.p_spavn, 20, 1)
                    sounds['hit'].play()
                    dell = True
                    del self.bullets[i]
                    break
            # bullet collide with map --------------------------------------------------------------------------------------
            
            
            # bullet dell break --------------------------------------------------------------------------------------------
            if dell:
                break
            # bullet dell break --------------------------------------------------------------------------------------------
            
            
            # bullet life update -------------------------------------------------------------------------------------------
            if bullet.life_time<=0:
                del self.bullets[i]
                break
            # bullet life update -------------------------------------------------------------------------------------------

        # bullet updates ---------------------------------------------------------------------------------------------------
        
        
        # camera set player object -----------------------------------------------------------------------------------------
        if self.mash_cam_timer == 0:
            self.mash_collide = None
            self.level_object.set_camera_target(self.obj_player)
            self.level_object.set_camera_zoom(1)
            self.level_object.set_camera_delta(0.05)
        # camera set player object -----------------------------------------------------------------------------------------
        
        
        # camera set mash timer update -------------------------------------------------------------------------------------
        if self.mash_cam_timer>0:
            self.mash_cam_timer-=1
        # camera set mash timer update -------------------------------------------------------------------------------------
            
            
        # camera set mash object -------------------------------------------------------------------------------------------
        if self.mash_collide is not None:
            self.level_object.set_camera_target(self.mash_collide)
            self.level_object.set_camera_delta(0.1)
            self.level_object.set_camera_zoom(1.5)
            try:
                if in_circle:
                    bullet.speed.normalyze()
                    bullet.speed*=1.2
                else:
                    bullet.speed.normalyze()
                    bullet.speed*=8
            except:...
        # camera set mash object -------------------------------------------------------------------------------------------
        
        
        # bees update ------------------------------------------------------------------------------------------------------
        for i, b in enumerate(self.bees):
            b.update()
            normal = Vector2.Normal(b.pos, self.obj_player.collider.center)
            normal.normalyze()
            normal*=1
            b.speed-=normal
            
            for i2 ,b2 in enumerate(self.bees):
                if i!=i2:
                    if distance(b.pos, b2.pos)<5:
                        n = Vector2.Normal(b.pos, b2.pos)
                        n.normalyze()
                        b.pos[0]+=n.x
                        b.pos[1]+=n.y
                        b2.pos[0]-=n.x
                        b2.pos[1]-=n.y
            if distance(b.pos, self.obj_player.collider.center)<50:
                
                self.level_object.set_camera_zoom(1.5)
                
            if distance(b.pos, self.obj_player.collider.center)<7 and not self.reloading:
                if self.hp_count==1:
                    self.reloading = True
                    self.killed_object = b
                    self.obj_player.rendered= False
                    self.gun.rendered = False
                
                sounds['kill'].play()
                self.p_spavn._pos = self.obj_player.collider.center
                self.p_space_3.add(p_kill, self.p_spavn, 5,1)
                
                
                self.hp_count-=1
                if self.hp_count!=0:
                    del self.bees[i]
                    break
                
        # bees update ------------------------------------------------------------------------------------------------------
        
        # mash guns bullets update -----------------------------------------------------------------------------------------
        for i,  bullet in enumerate(self.gun_mashs_bullets):
            bullet.update()
            normal = Vector2.Normal(bullet.pos, self.obj_player.collider.center)
            normal.normalyze()
            normal*=0.1
            bullet.speed-=normal
            if distance(bullet.pos, self.obj_player.collider.center)<50:
                
                self.level_object.set_camera_zoom(1.5)
            if distance(bullet.pos, self.obj_player.collider.center)<7 and not self.reloading:
                if self.hp_count==1:
                    self.reloading = True
                    self.killed_object = bullet
                    self.obj_player.rendered= False
                    self.gun.rendered = False
                
                sounds['kill'].play()
                self.p_spavn._pos = self.obj_player.collider.center
                self.p_space_3.add(p_kill, self.p_spavn, 5,1)
                
                
                self.hp_count-=1
                if self.hp_count!=0:
                    del self.gun_mashs_bullets[i]
                    break
            if bullet.life_time%10==0:
                self.p_spavn._pos = bullet.pos
                self.p_space_2.add(p_mash_bull,self.p_spavn,2,1)
        # mash guns bullets update -----------------------------------------------------------------------------------------
        
        
        # camera set killed gun mash object --------------------------------------------------------------------------------
        if self.killed_object is not None :
            self.level_object.set_camera_target(self.killed_object)
            self.level_object.set_camera_delta(0.1)
        # camera set killed gun mash object --------------------------------------------------------------------------------
                    
                    
        # particle space updates -------------------------------------------------------------------------------------------
        self.p_space.update(lambda x,y:..., lambda x:...)
        self.p_space_2.update(lambda x,y:..., lambda x:...)
        self.p_space_3.update(lambda x,y:..., lambda x:...)
        # particle space updates -------------------------------------------------------------------------------------------
        
        
        # render all level -------------------------------------------------------------------------------------------------
        self.level_object.obj_rendering([self.mashs,self.bullets,self.gun_mashs,self.gun_mashs_bullets, self.bee_houses, self.bees, self.colored_circles], self.render_bg)
        # render all level -------------------------------------------------------------------------------------------------
        
        
        # camera black zoom ------------------------------------------------------------------------------------------------
        if self.level_object.scale !=1:
            Draw.draw_rect(win.surf, [0,0],[win.surf.get_width(),win.surf.get_height()/2*(1-1/(self.level_object.scale))], 'black')
            Draw.draw_rect(win.surf, [0,win.surf.get_height()-win.surf.get_height()/2*(1-1/(self.level_object.scale))+1],[win.surf.get_width(),win.surf.get_height()/2*(1-1/(self.level_object.scale))], 'black')
        # camera black zoom ------------------------------------------------------------------------------------------------
        
        
        # render lesson ----------------------------------------------------------------------------------------------------
        self.render_lesson()
        # render lesson ----------------------------------------------------------------------------------------------------
        
        self.start_level_anim()
        if self.timer>=self.spedrun_time*60:self.reloading = True
        if self.reloading:
            self.stop_level_anim()
        self.reload()
        Draw.draw_line(win.surf, [0,0],[0+self.gun_kd/100*win.surf.get_size()[0],0],'white',5)
        
        self.mash_out_obj.center = [10,25]
        self.mash_out_obj.render(win.surf)
        count_text.draw(win.surf, [20,18],text=f'{self.mashs_kill_count} / {self.mashs_start_count}',color='white')
        count_text.draw(win.surf, [win.surf.get_width()-40,5],text=f'Fps: {int(win.fps)}',color='white')
        if self.mashs_start_count != self.mashs_kill_count:
            count_text.draw(win.surf, [5,5],text=f'Time: {round(self.timer/60,1)}s / {int(self.spedrun_time)}s',color='white')
        else:
            count_text.draw(win.surf, [5,5],text=f'Time: {round(self.timer/60,1)}s / {int(self.spedrun_time)}s',color='gray')
            
            new_level_text.draw(win.surf, [win.surf.get_width()/2,win.surf.get_height()-40],text=f'Press [Enter] to continue',color='white',centering=True)
            if Keyboard.key_pressed('enter'):
                self.new = True
        self.render_hp()
        if self.new:
            self.new_level_anim()
        self.new_level()
        mouse_cursor.center = Mouse.pos
        mouse_cursor.render(win.surf)



class LevelsManager:
    def __init__(self) -> None:
        self.scene_index = 0
        self.scenes = [
            Scene('levels\level1.json',self,60),
            Scene('levels\level2.json',self,30),
            Scene('levels\level3.json',self,30),
            Scene('levels\level4.json',self,30),
            Scene('levels\level5.json',self,25),
        ]

    def get_at_scene(self):
        return self.scenes[self.scene_index]
    
    def new_level(self):
        self.scene_index+=1
        
    def reload_at_scene(self):
        self.get_at_scene().reload()

lm = LevelsManager()



while win(fps=60, fps_view=0, base_color=(55,55,70)):
    
    lm.get_at_scene().loop()
    
    
    
    #win.fps_view()
    