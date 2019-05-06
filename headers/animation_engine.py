''' Doc_String '''

from headers.headers        import *
from headers.animation_NPC  import NPC_Animation
from headers.player         import Player
from tkinter                import font
from math                   import ceil

####################################################################
'''#################################################################
#################################################################'''
####################################################################

class TK_Base:
        
    def __init__(self, main_app):
        self.main_app = main_app
        
        "CREATE MAIN TK WINDOW"
        self.root = root = Tk()
        root.title('Pokemon Test')
        root.resizable(width=False,height=False)
        root.geometry('+{}+{}'.format(750,50))
        
        "MENU"
        self.menubar = Menu(self.root)
        self.menubar.add_command(label='Save',command=self.main_app.save)
        self.root.config(menu=self.menubar)
        
        "CANVAS"
        BLOCK_W, BLOCK_H = 10*scale,9*scale
        self.c = Canvas(root,bg='black',width=16*BLOCK_W,height=16*BLOCK_H)
        self.c.pack(side=TOP,expand=TRUE,fill=BOTH)
        
        "DEBUG_BOX"
        self.show_debug = False
        self.debug_text = Text(root,width=45,height=5,takefocus=False)
        self.debug_text['state'] = DISABLED
        
        
        
        self.debug_text.tag_config("font",font=font.Font(family='Helvetica'))
        
        self.debug_text.tag_config("tag1",foreground="grey")
        self.debug_text.tag_config("tag2",foreground="green")
        
        self.debug_text.tag_bind("tag1","<1>",lambda event:self.click("tag1"))
        self.debug_text.tag_bind("tag2","<1>",lambda event:self.click("tag2"))
        
    def click(self,tags):
        print('clicked:',tags)
        
    def clear_debug_text(self):
        self.debug_text['state'] = NORMAL
        self.debug_text.delete(1.0,END)
        self.debug_text['state'] = DISABLED
        
    def toggle_debug(self):
        self.show_debug = not self.show_debug
        if self.show_debug:
            self.debug_text.pack(side=TOP,expand=TRUE,fill=BOTH)
        else:
            self.debug_text.pack_forget()
            self.clear_debug_text()
        
    def print_debug(self, msg, tag=''):
        self.debug_text['state'] = NORMAL
        self.debug_text.insert(INSERT,msg,(tag, 'font'))
        num_lines = len(self.debug_text.get(1.0,END).splitlines())
        self.debug_text['height'] = ceil(num_lines*(7/6))
        self.debug_text['state'] = DISABLED

####################################################################
####################################################################

class BG_Class:
    def __init__(self, bg, x, y, c_obj):
        self.bg         = bg
        self.sx         = x*16
        self.sy         = y*16
        self.c_obj      = c_obj
        self.image_hold = None
    def reset_pos(self, x, y):
        self.sx         = x*16
        self.sy         = y*16
    def __str__(self):
        return self.bg

####################################################################
####################################################################

class Animated_Tile:
    def __init__(self,x,y,tile,lift=False):
        self.sx         = x*16
        self.sy         = y*16
        self.tile       = tile
        self.lift       = lift
        self.state      = 0
        self.image_hold = None
        self.c_obj      = None
    def __str__(self):
        return self.tile

####################################################################
####################################################################




















####################################################################
####################################################################

class Animation_Engine( TK_Base ):
    def __init__(self, main_app):
        super().__init__(main_app)
        
        self.screen_objects = []
        self.animated_tiles = []
        self.bgs            = []
        self.main_bg        = None
        self.player_ani     = None
        self.frame          = 0
        
        self.back_curtain()
    
    
    
    #######################################################
    #################  WASHOUT / CURTAIN  #################
    #######################################################
        
    def washout(self, frame):
        chdir('image_assets')
        img               = Image.open( 'washout_{}.png'.format(frame) )
        self.hold_washout = ImageTk.PhotoImage(img)
        self.washout_obj  = self.c.create_image(2,2,image=self.hold_washout,
                                                anchor=NW,tags='washout')
        chdir(main_dir)
        self.update()
        if frame == 2: self.c.delete(self.washout_obj)
    
    def back_curtain(self):
        chdir('image_assets')
        img                 = Image.open('blackout.png')
        self.hold_blackout  = ImageTk.PhotoImage(img)
        self.blackout_obj   = self.c.create_image(2,2,image=self.hold_blackout,
                                                  anchor=NW,tags='blackout')
        self.screen_objects.append(self.blackout_obj)
        chdir(main_dir)
        self.update()
    
    
    #######################################################
    #######################  MAIN  ########################
    #######################################################
        
    def draw(self):
        for obj in self.screen_objects:
            if hasattr(obj,'draw'):  obj.draw()
        self.move_sprites()
    
    def update(self):
        self.root.update_idletasks()
        self.root.update()
        self.draw()
        self.update_animated_tiles()
    
    def clear(self):
        saved_objs = []
        for obj in self.screen_objects:
            if    (obj == self.player_ani) \
               or (obj == self.blackout_obj) \
               or (obj in self.bgs):
                saved_objs.append(obj)
            else: self.c.delete(obj.c_obj)
        self.screen_objects = saved_objs
        self.animated_tiles = []
    
    def create_npc(self, npc_data ):
        npc = NPC_Animation( self.c, npc_data, self )
        self.screen_objects.append(npc)
        return npc
    
    def delete_npc(self, npc):
        for obj in self.screen_objects:
            if obj == npc: self.c.delete(obj.c_obj)
        return 0
    
    
    #######################################################
    ####################  BACKGROUNDS  ####################
    #######################################################
        
    def load_BG(self, bg, x_off=0, y_off=0):
        chdir('maps')
        chdir(bg)
        pic             = Image.open('main.png')
        cw,ch           = pic.size
        CW,CH           = cw*scale,ch*scale
        pic             = pic.resize( (CW,CH) )
        BG_HOLD         = ImageTk.PhotoImage(pic)
        bg              = BG_Class(bg,x_off,y_off,None)
        x,y             = self.get_sprite_pos( bg )
        c_obj           = self.c.create_image(x,y,image=BG_HOLD,anchor=NW,tags=f"{bg}")
        bg.image_hold   = BG_HOLD
        bg.c_obj        = c_obj
        self.screen_objects.append(bg)
        chdir(main_dir)
        self.c.lower(c_obj)
        self.c.lower(self.blackout_obj)
        return bg
    
    def create_bgs(self, bgs):
        loading = []
        for index, bg_data in enumerate(bgs):
            name, x_off, y_off = bg_data['bg'], bg_data['x_off'], bg_data['y_off']
            hide = bg_data.get('hide',False)
            if name in [str(b) for b in self.bgs]:
                bg = self.bgs[[str(b) for b in self.bgs].index(name)]
                if not hide: bg.reset_pos(x_off,y_off)
            else: bg = self.load_BG( name, x_off, y_off )
            if index == 0: self.main_bg = bg
            if hide: self.c.lower(bg.c_obj)
            loading.append( bg )
        
        to_delete = [bg for bg in self.bgs if bg not in loading]
        for bg in to_delete:
            self.screen_objects.remove( bg )
            self.bgs.remove( bg )
        self.bgs = loading
    
    
    #######################################################
    #################  CHARACTER SPRITES  #################
    #######################################################
    
    def get_sprite_pos(self, obj):
        player_pos  = self.main_app.subpos
        sx,sy       = player_pos
        ox,oy       = obj.sx,obj.sy
        if type(obj) == NPC_Animation:
            if obj.type_ == 'cut_tree': oy -= 0
            if obj.type_ == 'pokeball': oy -= 2
            else:                       oy -= 4
        x           = (64-sx+ ox)*scale +2
        y           = (64-sy+ oy)*scale +2
        return x,y

    def move_sprites(self):
        for obj in self.screen_objects:
            if obj == self.player_ani: continue
            if obj == self.blackout_obj: continue
            x,y = self.get_sprite_pos( obj )
            self.c.coords(obj.c_obj,x,y)
    
    
    #######################################################
    ##################  ANIMATED TILES  ###################
    #######################################################
    
    def draw_animated_tiles(self):
        for tile in self.animated_tiles:
            chdir('image_assets')
            chdir('animated_tiles')
            img             = '{}.png'.format(tile.tile)
            pic             = Image.open(img)
            cw,ch           = pic.size
            CW,CH           = cw*scale,ch*scale
            pic             = pic.resize( (CW,CH) )
            tile.image_hold = ImageTk.PhotoImage(pic)
            x,y             = self.get_sprite_pos( tile )
            tile.c_obj      = self.c.create_image(x,y,image=tile.image_hold,
                                                  anchor=NW,tags='animated_tile')
            self.screen_objects.append(tile)
            chdir(main_dir)
            self.c.lower(tile.c_obj)
    
    def update_animated_tiles(self):
        for tile in self.animated_tiles:
            if tile.lift: self.c.lift(tile.c_obj)
            else:
                tile.state += 1
                if tile.state == 32: tile.state = 0
                if tile.state < 16:
                    self.c.lower(self.main_bg.c_obj)
                    self.c.lower(self.blackout_obj)
                else:
                    self.c.lower(tile.c_obj)

    def create_animated_tiles(self, movables):
        tile_names = [('flower_',False),
                      ('tall_grass',True),
                      ]
        for (x,y),tile in movables.items():
            if tile == None: continue
            for name, lift_ in tile_names:
                if tile.startswith(name):
                    animated_tile = Animated_Tile(x,y,tile,lift_)
                    self.animated_tiles.append(animated_tile)
        self.draw_animated_tiles()
    
    
    #######################################################
    #######################################################



####################################################################
####################################################################





####################################################################
####################################################################

