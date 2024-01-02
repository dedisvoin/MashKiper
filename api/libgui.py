from liball import *


win = Window()

GLOBAL_MOUSE_EVENT_HANDLER = MouseEventHandler()

class _press_effects:
    SOLID_COLORS = 'SOLID_COLORS'
    GRADIENT_COLORS = 'GRADIENT_COLORS'
    
class _coords:
    UP_LEFT = 'UPLEFT'
    UP_CENTER = 'UPCENTER'
    UP_RIGHT = 'UPRIGHT'
    LEFT_CENTER = 'LEFTCENTER'
    RIGHT_CENTER = 'RIGHTCENTER'
    DOWN_LEFT = 'UPLEFT'
    DOWN_CENTER = 'UPCENTER'
    DOWN_RIGHT = 'UPRIGHT'
    CENTER = 'CENTER'
    

class _button:
    def __init__(self, 
                    win_ : Window,
                    start_size_: Tuple[float, float],
                    start_pos_: Tuple[int, int],
                    press_effect_: _press_effects,
                    press_color_: Any,
                    default_color_: Any,
                    togled_color_: Any,
                    release_color_: Any,
                    color_remove_speed_: float = 0.1,
                    color_replace_speed_: float = 0.3,
                    color_click_replace_speed_: float = 0.05,
                    radius_: float | int = 0,
                    listening_mouse_button_ = Mouse.left,
                    press_event_id: Any = None,
                    click_event_id: Any = None,
                    pos_coord: Tuple[int, int] = _coords.UP_LEFT,
                    resizing: bool = False,
                    resize_size: Tuple[int ,int] = [0,0],
                    resize_speed: float = 0.5,
                    togled_: float = False) -> None:
        
        self._win = win_
        
        self._start_size = start_size_
        self._start_pos = start_pos_
        self._press_effects = press_effect_
        
        self._at_color = [0, 0, 0]
        
        self._pos_coord = pos_coord
        
        self._togled = togled_
        self.togl = False
        
        self._resizing = resizing
        self._resize_size = resize_size
        self._resize_speed = resize_speed
        
        self._press_color = Color( press_color_ )
        self._default_color = Color( default_color_ )
        self._togled_color = Color( togled_color_ )
        self._release_color = Color( release_color_ )
        
        self._color_remove_speed = color_remove_speed_
        self._color_replace_speed = color_replace_speed_
        self._color_click_replace_speed = color_click_replace_speed_
        
        self._radius = radius_
        self._lmb = listening_mouse_button_
        self._press_event_id = press_event_id
        self._click_event_id = click_event_id
    
        self._size = copy(start_size_)
        self._pos = copy(start_pos_)
        
        self._r_pos = copy(self._pos)
        
        self._init()
        
    @property
    def pos(self):
        return self._pos
    
    @property
    def size(self):
        return self._size
    
    def _init(self):
        global GLOBAL_MOUSE_EVENT_HANDLER
        GLOBAL_MOUSE_EVENT_HANDLER.AddEvent(Mouse(self._lmb, Mouse.press_event, self._press_event_id))
        GLOBAL_MOUSE_EVENT_HANDLER.AddEvent(Mouse(self._lmb, Mouse.click_event, self._click_event_id))
    
    def _render(self):
        Draw.draw_rect(self._win.surf, self._r_pos, self.size, self._at_color.rgb, 0, self._radius)
        
    def in_rect(self, pos: Tuple[int, int]) -> bool:
        return in_rect(self._r_pos, self.size, pos)
    
    def _posing(self):
        if self._pos_coord == _coords.CENTER:
            self._r_pos = [
                self.pos[0]-self.size[0]/2,
                self.pos[1]-self.size[1]/2
            ]
        if self._pos_coord == _coords.LEFT_CENTER:
            self._r_pos = [
                self.pos[0],
                self.pos[1]-self.size[1]/2
            ]
    
    def update(self):
        self._at_color = self._default_color
        
        
        if self.in_rect(Mouse.pos):
            if GLOBAL_MOUSE_EVENT_HANDLER.GetEventById(self._click_event_id):
                self.togl = not self.togl
            
            if self._press_effects == _press_effects.SOLID_COLORS:
                if GLOBAL_MOUSE_EVENT_HANDLER.GetEventById(self._press_event_id):
                    self._at_color = copy(self._press_color)
                else:
                    self._at_color = copy(self._release_color)
                    
            elif self._press_effects == _press_effects.GRADIENT_COLORS:
                if not self.togl:
                    if GLOBAL_MOUSE_EVENT_HANDLER.GetEventById(self._press_event_id):
                        self._at_color.mutate(self._press_color, self._color_click_replace_speed)
                    else:    
                        self._at_color.mutate(self._release_color, self._color_remove_speed)
            
                
            
                    
                
            if self._resizing:
                self._size[0] += -(self._size[0]-self._resize_size[0])*self._resize_speed
                self._size[1] += -(self._size[1]-self._resize_size[1])*self._resize_speed
                
            
                
        else:
            
            if self._resizing:
                self._size[0] += -(self._size[0]-self._start_size[0])*self._resize_speed
                self._size[1] += -(self._size[1]-self._start_size[1])*self._resize_speed
                
            
            if self._press_effects == _press_effects.GRADIENT_COLORS and not self._togled:
                self._at_color.returned(self._color_remove_speed)
        if self.togl:
            self._at_color.mutate(self._togled_color, self._color_replace_speed)
            
        self._posing()
        



bt = _button(win, 
            [200,40],
            [300,100],
            _press_effects.SOLID_COLORS,
            [200,200,200],
            [200,200,200],
            [14,190,100],
            [200,200,200],
            0.3,
            0.3,
            0.3,
            15, press_event_id='1', 
            click_event_id='2',
            pos_coord=_coords.LEFT_CENTER,
            resizing=1,
            resize_size=[440,40],
            resize_speed=0.3,
            togled_=1)

while win():
    bt.update()
    bt._render()
    
    GLOBAL_MOUSE_EVENT_HANDLER.EventsUpdate()
