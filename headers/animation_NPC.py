''' Doc_String '''

from headers.headers import *




####################################################################
####################################################################

move_sprite_dict   = {0:'move_down',1:'move_left',2:'move_up',3:'move_right'}
facing_sprite_dict = {0:'down',1:'left',2:'up',3:'right'}

####################################################################
####################################################################

def get_random_move():
    f   = randint(0,3)
    x,y = 0,0
    if   f == 0: y =  1
    elif f == 1: x = -1
    elif f == 2: y = -1
    elif f == 3: x =  1
    return x,y

####################################################################
####################################################################

def get_tiles_in_view(px,py,facing):
    x,y = 0,0
    if   facing == 0: y =  1
    elif facing == 1: x = -1
    elif facing == 2: y = -1
    elif facing == 3: x =  1
    
    in_view = []
    for i in range(1,5):
        next_ = x*i + px,  y*i + py
        in_view.append(next_)
    
    return in_view

####################################################################
####################################################################

def get_tile_in_front(facing):
    x,y = 0,0
    if   facing == 0: y =  1
    elif facing == 1: x = -1
    elif facing == 2: y = -1
    elif facing == 3: x =  1
    return x,y

####################################################################
####################################################################

def get_turning_direction(player_pos,pos):
    px,py = player_pos
    xx,yy = pos
    return px-xx, py-yy

####################################################################
####################################################################

class NPC_Animation():
        
    def __init__(self, c, data, ani_engine):
        
        self.ani_engine = ani_engine
        self.main_app   = None
        self.c          = c
        self.type_      = data['type']
        self.name       = data['name']
        self.sx         = data['x'] * 16
        self.sy         = data['y'] * 16
        self.freeze     = False
        self.actions    = []
        
        self.move_spots = data['move']
        self.facing     = data.get('facing',0)
        self.frozen     = data.get('frozen',0)
        self.interact   = data.get('interact',None)
        self.can_battle = data.get('battle',False)
        self.movements  = get_character_sprites(self.type_)
        
        self.moving         = False
        self.c_obj          = None
        self.arm            = 'right'
        self.sprite_hold    = None
        self.sprite         = None
        self.frame          = 0
        self.turn_back      = None
        
##        self.can_battle = True
        
    def __str__(self):
        return self.name
        
    
    
    
    
    
    
    def interact_with(self):
        if self.interact == None: return 0
        "Get the NPC to look at you"
        px,py = self.main_app.calc_position()
        xx,yy = self.calc_position()
        self.turn_back = get_tile_in_front(self.facing)
        self.turn(px-xx, py-yy)
        
        interaction_type = [i for i in self.interact.keys()][0]
        
        if self.can_battle:
            self.check_battle()
        
        elif interaction_type == 'talk':
            self.main_app.awaiting_input = True
            self.main_app.do_freeze()
            self.main_app.do_freeze_npcs()
            print(self.interact['talk'])
            print()
            
        elif interaction_type == 'action':
            action = getattr(self.main_app, self.interact['action'])
            action(self)
        
        return 0
    
    
    
    
    
    
    def walk_to_player(self):
        still_walking = False
        x,y = get_tile_in_front(self.facing)
        if self.can_move(x,y):
            self.moving = x,y
            self.actions = [('move',x,y) for i in range(8)]
            return True
        return still_walking
    
    def check_for_clear_path(self):
        x,y = self.calc_position()
        player_pos = self.main_app.calc_position()
        in_view = get_tiles_in_view(x,y,self.facing)
        for spot in in_view:
            if spot == player_pos: break
            if spot not in self.move_spots: return False
        return True
    
    def check_battle(self):
        if not self.can_battle:             return False
        if not self.can_see_player():       return False
        if not self.check_for_clear_path(): return False
        if not self.walk_to_player(): self.main_app.start_battle(self)
        return True
    
    def can_see_player(self):
        x,y = self.calc_position()
        player = self.main_app.calc_position()
        return player in get_tiles_in_view(x,y,self.facing)
    
    def done_moving(self):
        self.frame = 0
        self.moving = False
        self.move_arm()
        if not self.check_battle(): self.un_freeze()
    
    
    
    
    
    
    
    
    
    
    def draw_sprite(self, sprite):
        if self.c_obj      != None: self.c.delete(self.c_obj)
        pos_x,pos_y         = self.ani_engine.get_sprite_pos(self)
        self.sprite_hold    = ImageTk.PhotoImage(sprite)
        self.c_obj = self.c.create_image(pos_x,pos_y,image=self.sprite_hold,anchor=NW)


    def get_sprite(self, frame=0):
        '''some characters dont have sprites for certain movements
        ex: many are missing alternate move steps'''
        m           = self.movements
        up          = m.get('up')
        down        = m.get('down')
        left        = m.get('left')
        right       = m.get('right')
        move_up     = m.get('move_up')
        move_down   = m.get('move_down')
        move_left   = m.get('move_left')
        move_right  = m.get('move_right')
        
        if self.arm == 'right':
            move_up     = m.get('move_up_alt')
            move_down   = m.get('move_down_alt')
        
        if self.moving and frame in [3,4,5,6]:
            up,down,left,right = move_up,move_down,move_left,move_right
        
        return [down,left,up,right][self.facing]

    def move_arm(self):
        if self.arm == 'right': self.arm = 'left'
        else: self.arm = 'right'

    def turn(self, x,y):
        facing_rn = self.facing
        if   x > 0: self.facing=3
        elif x < 0: self.facing=1
        elif y > 0: self.facing=0
        elif y < 0: self.facing=2
        
        attempt = facing_sprite_dict[self.facing]
        if attempt not in self.movements.keys():
            self.facing = facing_rn

    def un_freeze(self, msg=''):
        if self.freeze:
            if msg: print(self.name,'un_freeze',msg)
            self.freeze = False
            if self.turn_back:
                self.turn(*self.turn_back)
                self.turn_back = None

    def do_freeze(self, msg=''):
        if not self.freeze:
            if msg: print(self.name,'freeze',msg)
            self.freeze = True

    def random_move(self):
        if self.freeze: return False
        if self.frozen: return False
        x,y = get_random_move()
        
        self.turn(x,y)
        if self.can_move(x,y):
            self.moving = x,y
            self.actions = [('move',x,y) for i in range(8)]

    def do_action(self):
        if not self.actions: return 0
        self.do_freeze()
        action = self.actions.pop()
        action_type, args = action[0], action[1:]
        
        if action_type == 'turn':
            self.turn(*args)
            
        elif action_type == 'move':
            self.frame += 1
            self.sx += args[0]*2
            self.sy += args[1]*2
            
        elif action_type == 'notice':
            self.main_app.ani_engine.draw_pop_up(args[0],args[1],action_type)
            
        if action[0] == 'wait':
            return 0
        
        if len(self.actions) == 0: self.done_moving()
    
    def can_move(self, x, y):
        attempt = move_sprite_dict[self.facing]
        if attempt not in self.movements.keys():
            return False
        
        xx,yy = self.calc_position()
        new_spot = (x+xx, y+yy)
        if new_spot in self.move_spots:
            if new_spot != self.main_app.calc_position():
                return True
        return False

    def draw(self):
        last        = self.sprite
        self.sprite = self.get_sprite( self.frame )
        if last != self.sprite: self.draw_sprite(self.sprite)
        self.do_action()
    
    def calc_position(self):
        return self.sx//16, self.sy//16
        


####################################################################
####################################################################


####################################################################
####################################################################

