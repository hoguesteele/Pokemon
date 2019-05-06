''' Doc_String '''

from headers.headers import *




####################################################################
####################################################################

class Player():
        
    def __init__(self):
        
        self.movements      = get_character_sprites()
        
        self.c_obj          = None
        self.arm            = 'right'
        self.hold_Image     = None
        self.sprite         = None
        self.frame          = 0
        
        self.moving         = False
        self.turning        = False
        self.facing         = 0
        
        
    def __str__(self):
        return 'Player'
    
    def connect(self, ani_eng):
        self.c              = ani_eng.c
        ani_eng.player_ani  = self
        ani_eng.screen_objects.append(self)
    
    def draw_sprite(self, sprite):
        if self.c_obj != None: self.c.delete(self.c_obj)
        pos_x = (16*scale*4)+5
        pos_y = (16*scale*4)-10
        self.hold_Image = ImageTk.PhotoImage(sprite)
        self.c_obj      = self.c.create_image(pos_x,pos_y,image=self.hold_Image,anchor=NW)

    def get_sprite(self, frame):
        m           = self.movements
        up          = m['up']
        down        = m['down']
        left        = m['left']
        right       = m['right']
        move_up     = m['move_up']
        move_down   = m['move_down']
        move_left   = m['move_left']
        move_right  = m['move_right']
        
        if self.arm == 'right':
            move_up     = m['move_up_alt']
            move_down   = m['move_down_alt']
        
        if self.moving and frame in [3,4,5,6]:
            up,down,left,right = move_up,move_down,move_left,move_right
        elif self.turning:
            up,down,left,right = move_up,move_down,move_left,move_right
        return [down,left,up,right][self.facing]

    def draw(self):
        frame       = self.frame
        last        = self.sprite
        self.sprite = self.get_sprite( frame )
        if last != self.sprite: self.draw_sprite(self.sprite)
        
        if self.moving:
            self.frame += 1
            if self.frame == 8:
                self.frame = 0
                if self.arm == 'right': self.arm = 'left'
                else: self.arm = 'right'
                return True
        return False
    


####################################################################
####################################################################



####################################################################
####################################################################

