''' Doc_String '''

from headers.headers            import *
from headers.animation_engine   import Animation_Engine
from headers.player             import Player
from headers.animation_NPC      import NPC_Animation
from headers.controller         import Controller
import pickle


####################################################################
'''#################################################################



####################################################################
####################################################################

I also need to update the Background Builder program.
I need to be able to take a finished image and to draw tiles over it.
This process should not completely replace the movement tiles,
    nor should it remove the other data that notes music and NPC's.
    It should take data that it's been given,
        Check if the tile already has data,
        and either re-write it, or write new data for the tile.

#################################################################'''
####################################################################

def get_valid_spaces( movables ):
    path_tiles   = ['empty','cement','flower_1','flower_2','door','grass',
                    'water','water_0','water_1','water_2','tall_grass']
    valid_spaces = []
    for (x,y),tile in movables.items():
        if tile in path_tiles:  valid_spaces.append((x,y))
        elif 'ledge' in tile:   valid_spaces.append((x,y))
    return valid_spaces

def get_int(value):
    to_return = value
    try: to_return = int(value)
    except: pass
    return to_return

def get_bool(value):
    original = value
    try:
        if value == 'True':  value = True
        if value == 'False': value = False
        if value == 'None':  value = None
    except: return original
    return value

def get_text(value):
    if type(value) != str: return value
    value = value.replace('NEWLINE','\n')
    value = value.replace('COMMA',',')
    return value

def dir_to_turn(direction):
    x,y = 0,0
    if   direction == 'down': y =  1
    elif direction == 'left': x = -1
    elif direction == 'up': y = -1
    elif direction == 'right': x =  1
    return x,y

####################################################################
####################################################################

def load_music(bg):
    chdir('maps')
    chdir(bg)
    with open('music.txt','r') as file:
        dat = file.read()
    chdir(main_dir)
    song = ''
    if dat != '.': song = dat
    return song

def load_scripts(bg):
    chdir('maps')
    chdir(bg)
    try:
        with open('script.txt','r') as file:
            dat = file.read().splitlines()
    except:
        chdir(main_dir)
        return []
    chdir(main_dir)
    scripts = []
    
    if dat[0] == '.': return scripts
    data = [[j.strip() for j in i.split(',')] for i in dat if i]
    
    for line in data:
        script = {}
        for string in line:
            k,v = [get_bool(get_text(get_int(string.strip())))
                   for string in string.split(':')]
            v = [i.strip() for i in v.split(';')]
            if len(v) == 1: v = v[0]
            script[k] = v
        scripts.append(script)
    return scripts

def load_bgs(bg):
    chdir('maps')
    chdir(bg)
    with open('bgs.txt','r') as file:
        dat = file.read().splitlines()
    chdir(main_dir)
    bgs = [{'name':bg,'x_off':0,'y_off':0,'hide':False}]
    
    if dat[0] == '.': return bgs
    data = [[j.strip() for j in i.split(',')] for i in dat if i]
    
    for line in data:
        extra_bg = {}
        for string in line:
            k,v = [get_bool(get_text(get_int(string.strip())))
                   for string in string.split(':')]
            extra_bg[k] = v
        bgs.append(extra_bg)
    return bgs

def load_signs(bg):
    chdir('maps')
    chdir(bg)
    with open('signs.txt','r') as file:
        dat = file.read().splitlines()
    chdir(main_dir)
    signs = []
    
    if dat[0] == '.': return signs
    data = [[j.strip() for j in i.split(',')] for i in dat if i]
    
    for line in data:
        sign = {}
        for string in line:
            k,v = [get_bool(get_text(get_int(string.strip())))
                   for string in string.split(':')]
            sign[k] = v
        signs.append(sign)
    return signs

def load_doors(bg):
    chdir('maps')
    chdir(bg)
    with open('doors.txt','r') as file:
        dat = file.read().splitlines()
    chdir(main_dir)
    doors = {}
    
    if dat[0] == '.': return doors
    data = [[j.strip() for j in i.split(',')] for i in dat if i]
    
    for line in data:
        door = {}
        for string in line:
            k,v = [get_bool(get_text(get_int(string.strip())))
                   for string in string.split(':')]
            door[k] = v
        pos_x = door.pop('from_x')
        pos_y = door.pop('from_y')
        doors[(pos_x,pos_y)] = door
    return doors

def load_tiles(bg):
    chdir('maps')
    chdir(bg)
    with open('tiles.txt','r') as file:
        dat = file.read().splitlines()
    chdir(main_dir)
    tiles = {}
    
    if dat[0] == '.': return tiles
    data = [[j.strip() for j in i.split(',')] for i in dat if i]
    
    for line in data:
        x, y, tile = [get_bool(get_text(get_int(string.split(':')[-1].strip())))
                      for string in line]
        if tile == None: tile = 'empty'
        tiles[(x,y)] = tile
    return tiles

def load_npcs(bg):
    chdir('maps')
    chdir(bg)
    chdir('npcs')
    
    npcs = []
    npc_data = []
    for file_name in listdir():
        with open(file_name,'r') as file:
            data = [i for i in file.read().splitlines() if i]
            npc_data.append(data)
    chdir(main_dir)
    
    for dat in npc_data:
        if dat[0] == '.': continue
        npc = {'move':[]}
        for line in dat:
            item_type, values = [string.strip() for string in line.split('=')]
            values = [[j.strip() for j in i.split(':')] for i in values.split(',')]
            values = [[k,get_bool(get_text(get_int(v)))] for k,v in values]
            if item_type == 'pos':
                for key,value in values: npc[key] = value
            if item_type == 'move':
                x,y = [value for xy,value in values]
                npc['move'].append((x,y))
            if item_type == 'interact':
                key,value = values[0]
                npc['interact'] = {key:value}
        
        npc.setdefault('name',npc['type'])
        npc.setdefault('battle',False)
        npc.setdefault('frozen',False)
        npc.setdefault('facing',0)
        npcs.append(npc)
    return npcs

####################################################################
####################################################################































####################################################################
####################################################################


class App:
        
    def __init__(self, queue=None):
        
        self.freeze         = False
        self.queue          = queue
        self.current_song   = None
        self.controller     = Controller(self)
        self.ani_engine     = Animation_Engine( self )
        self.player         = Player()
        self.player.connect(self.ani_engine)
        
        
        "TELL MAIN_LOOP TO RUN WITH ERROR PASSING OR NOT"
        self.show_error = True
        self.show_error = False
        
        self.walk_thru_walls = True
        self.walk_thru_walls = False
        
        
        "GATHER && LOAD INITIAL DATA"
        self.subpos         = 0,0
        self.actions        = []
        self.npcs           = []
        self.menu_open      = False
        self.valid_spaces   = []
        self.doors          = []
        self.surfing        = False
        self.freeze_frames  = 0
        self.awaiting_input = False
        self.frozen         = False
        self.scripted_scene = {'first_step':False}
        
        self.load_save()
        
        
        self.do_debug = False
##        self.do_debug = True
        
        if self.do_debug: self.ani_engine.toggle_debug()
        
        
##        self.ani_engine.root.destroy()
    
    
    #######################################################
    ##############  SCRIPTED INTERACTIONS  ################
    #######################################################
    
    def run_script(self, script):
        frozen = script.get('frozen',[])
        talk   = script.get('talk',False)
        sequence = script.get('sequence',[])
        print(sequence)
        sequence.reverse()
        
        if 'player' in frozen: self.frozen = True
        for npc in self.npcs:
            if npc.name in frozen: npc.frozen = True
        
        
        for item in [i.split('.') for i in sequence]:
            name = item[0]
            actions = item[1:]
            if not actions[-1].isnumeric():
                if actions[0] == 'talk': actions.append(talk)
                if actions[0] == 'unfreeze': actions.append(frozen)
                actions = [tuple(actions)]
            else:  actions = [tuple(actions[:-1]) for i in range(int(actions[-1])*8)]
            
            if name != 'player':
                npc = [npc_ for npc_ in self.npcs if npc_.name == name][0]
                npc.actions.extend(actions)
            else: self.actions.extend(actions)
        
    
    #######################################################
    ###################  INTERACTIONS  ####################
    #######################################################
    
    def interact_with(self):
        x,y     = self.calc_position()
        xx,yy   = facing_dict[self.player.facing]
        tile    = self.movables.get((x,y),'empty')
        looking_at      = x+xx,y+yy
        looking_at_tile = self.movables.get(looking_at,'empty')
        
        for npc in self.npcs:
            if npc.calc_position() == looking_at: return npc.interact_with()
        if self.start_surfing(xx, yy, looking_at_tile): return 0
        if looking_at_tile == 'sign': return self.check_for_sign(looking_at)
        
        print(' Looking at:',looking_at, looking_at_tile)
        print(' standing on:', x, y, tile,'\n')
    
    def check_for_sign(self, looking_at):
        x,y = looking_at
        for sign in self.signs:
            if (x == sign['x'])  and  (y == sign['y']):
                print(str(sign['text']))
                print()
        return 0
    
    def cut_tree(self, tree):
        self.ani_engine.delete_npc(tree)
        self.npcs.remove(tree)
        x,y = tree.calc_position()
        self.movables[(x,y)] = 'grass'
        del tree
        return 0
    
    
    #######################################################
    ###################  LOADING DATA  ####################
    #######################################################
    
    def save(self):
        x,y = self.calc_position()
        data = {'bg':self.last_bg,'x':x,'y':y,'facing':self.player.facing}
        with open('save_data','wb') as pickle_file: pickle.dump(data, pickle_file)
    
    def load_save(self):
        with open('save_data','rb') as pickle_file: data = pickle.load(pickle_file)
##        self.load( {'bg':'professor_elm', 'x':6, 'y':8, 'facing':0} )
        self.load( data )
    
    
    #######################################################
    ################  LOADING BACKGROUNDS  ################
    #######################################################
    
    def check_for_doors(self, x, y):
        if (x,y) in self.doors:
            data = self.doors[(x,y)]
            self.load_door( data )
    
    def load_door(self, data):
        do_washout = data.get('washout',True)
        if do_washout:
            self.do_freeze()
            self.freeze_frames = 3
            self.ani_engine.washout(1)
        self.load(data)
        if do_washout: self.ani_engine.washout(2)
    
    def load(self, data):
        self.last_bg        = data['bg']
        self.player.facing  = data['facing']
        self.subpos         = data['x']*16,data['y']*16
        self.signs          = load_signs(data['bg'])
        self.doors          = load_doors(data['bg'])
        bgs                 = load_bgs(data['bg'])
        self.movables       = load_tiles(data['bg'])
        song                = load_music(data['bg'])
        npcs                = load_npcs(data['bg'])
        scripts             = load_scripts(data['bg'])
        
        
        self.ani_engine.clear()
        self.load_music( song )
        self.valid_spaces = get_valid_spaces( self.movables )
        self.ani_engine.create_bgs( bgs )
        self.ani_engine.create_animated_tiles( self.movables )
        self.create_npcs( npcs )
        for (x,y),door in self.doors.items(): self.valid_spaces.append((x,y))
        for script in scripts:
            completed_script = self.scripted_scene.get(script['name'],False)
            if not completed_script:
                self.run_script(script)
                self.scripted_scene[script['name']] = True
    
    
    #######################################################
    ####################  CONTROLLER  #####################
    #######################################################
    
    def key_press(self, key, value):
        if self.frozen: return False
        if self.awaiting_input:
            self.un_freeze()
            self.un_freeze_npcs()
            self.awaiting_input = False
            return False
        if self.freeze: return False
        
        "MENU KEYS"
        if key == 'q': self.toggle_menu()
        if self.menu_open: pass
        
        else:
            if key == 'w':      self.move_player(x =  0, y = -1)
            if key == 'a':      self.move_player(x = -1, y =  0)
            if key == 's':      self.move_player(x =  0, y =  1)
            if key == 'd':      self.move_player(x =  1, y =  0)
            if key == '5':      self.interact_with()
            if key == 'e':      self.interact_with()
            if key == 'Shift':  self.ani_engine.toggle_debug()
    
    def key_release(self, key):
        "If we're redirecting inputs, remember to redirect KEY_RELEASES too"
        pass
    
    def toggle_menu(self):
        self.menu_open = not self.menu_open
        print('self.menu_open:',self.menu_open)
        if self.menu_open:  pass
        else:               pass
    
    
    #######################################################
    #######################  DEBUG  #######################
    #######################################################
    
    def _debug_(self):
        def print_(msg,tag='',end='\n'): self.ani_engine.print_debug(msg + end,tag)
        self.ani_engine.clear_debug_text()
        
        self.show_npc_status(print_)
        
    def show_npc_status(self, print_):
        print_(f"freeze frozen battle name")
        print_(f"{self.freeze:^6}    {self.frozen:^6}    {'0':^6}    player")
        for npc in self.npcs:
            print_("{:^6}    {:^6}    {:^6}    {}".format(
                npc.freeze, npc.frozen, npc.can_battle, npc.name,
                ))
        
    def show_screen_objs(self, print_):
        print_('screen_objects:'.upper(),tag='tag1')
        for obj in self.ani_engine.screen_objects:
            tags = self.ani_engine.c.gettags(obj)
            if not tags: continue
            print_('  '+str(tags[0].upper()),tag='tag1')
    
    
    #######################################################
    #######################  NPCS  ########################
    #######################################################
    
    def create_npcs(self, npcs):
        self.npcs   = []
        for npc_obj in npcs:
            npc          = self.ani_engine.create_npc( npc_obj )
            npc.main_app = self
            self.npcs.append(npc)
    
    def npc_random_update(self):
        npcs = [npc for npc in self.npcs if not npc.frozen]
        if not npcs: return 0
        move_timer = round(100/len(npcs))
        if randint(1,move_timer) == 1:
            npc = choice(npcs)
            npc.random_move()
        
    def get_npc_positions(self):
        pos = []
        for npc in self.npcs: pos.append((npc.sx//16, npc.sy//16))
        return pos
    
    
    #######################################################
    #######################  MAIN  ########################
    #######################################################
    
    def update(self):
        self.ani_engine.update()
        self.do_action()
        self.controller.get_input()
        self.npc_random_update()
        if self.player.turning: self.player.turning -= 1
        if self.freeze_frames:
            self.freeze_frames -= 1
            if not self.freeze_frames: self.un_freeze('')
        if self.do_debug: self._debug_()
    
    def load_music(self, song):
        if self.queue:
            print('load_music({})'.format(song))
            if self.current_song != song:
                self.queue.put(song)
                self.current_song = song
    
    
    #######################################################
    ######################  PLAYER  #######################
    #######################################################
    
    def done_moving(self):
        self.un_freeze()
        if type(self.player.moving) != bool:
            "Then player has finished walk animation"
            "It's a bool when turning"
            self.player.moving = False
            x,y = self.calc_position()
            tile = self.movables.get((x,y),'empty')
            self.stop_surfing(tile)
            self.check_for_doors(x,y)
            for npc in self.npcs: npc.check_battle()
            self.check_encounter(tile)

    def check_encounter(self, tile):
        if ('water' in tile) or (tile == 'tall_grass'):
            if randint(1,15) == 1:
##                print('pokemon encounter')
                pass

    def un_freeze(self, msg=''):
        if self.freeze:
            if msg: print('player un_freeze',msg)
            self.freeze = False

    def do_freeze(self, msg=''):
        if not self.freeze:
            if msg: print('player freeze',msg)
            self.freeze = True

    def do_freeze_npcs(self, msg=''):
        for npc in self.npcs: npc.do_freeze(msg)

    def un_freeze_npcs(self, msg=''):
        for npc in self.npcs: npc.un_freeze(msg)
    
    def start_battle(self, npc):
        print('\n  start_battle with:',npc.name,'\n')
        self.awaiting_input = True
        self.do_freeze()
        self.do_freeze_npcs()
        self.end_battle(npc)
    
    def end_battle(self, npc):
        print('\n  end_battle with:',npc.name,'\n')
        npc.can_battle = False
    
    def do_action(self):
        if not self.actions: return 0
        self.do_freeze()
        action = self.actions.pop()
        action_type, args = action[0], action[1:]
        
        if action_type == 'turn':
            if len(args) == 1: x,y = dir_to_turn(args[0])
            else: x,y = args
            self.player.facing  = player_turn(x,y)
            self.player.turning = 3
        elif action_type == 'quick_turn':
            self.player.facing = player_turn(*args)
        elif action_type == 'move':
            if len(args) == 1: x,y = dir_to_turn(args[0])
            else: x,y = args
            if type(self.player.moving) == bool: self.player.moving = x,y
            self.subpos = ((x*2) + self.subpos[0], (y*2) + self.subpos[1])
        elif action_type == 'run':
            self.subpos = ((args[0]*4) + self.subpos[0], (args[1]*4) + self.subpos[1])
        elif action_type == 'swim':
            self.subpos = (args[0] + self.subpos[0], args[1] + self.subpos[1])
        elif action_type == 'start_surf':
            self.subpos = (args[0] + self.subpos[0], args[1] + self.subpos[1])
            
        if action[0] == 'unfreeze':
            frozen = args[0]
            if 'player' in frozen: self.frozen = False
            for npc in self.npcs:
                if npc.name in frozen: npc.frozen = False
        
        else: pass
        if len(self.actions) == 0:
            self.done_moving()
        return
    
    def move_player(self, x, y):
        "Check if player needs to TURN"
        if facing_dict[self.player.facing] != (x,y):
            if self.controller.key_space: self.actions = [('quick_turn',x,y)]
            else: self.actions = [('wait',),('wait',),('turn',x,y)]
        else:
            px,py = self.calc_position()
            px,py = px+x,py+y
            tile = self.movables.get((px,py),'empty')
            moving = False
            
            if (self.can_move(px,py,tile))  or  (self.walk_thru_walls):
                moving = True
                self.player.moving = x,y
                
                if self.controller.key_space:
                    self.actions = [('run',x,y) for i in range(4)]
                else:
                    self.actions = [('move',x,y) for i in range(8)]
                
                if 'ledge' in tile:
                    if self.check_for_ledge(tile):
                        self.actions = [('move',x,y) for i in range(16)]
                    else: moving = False
                if 'water' in tile:
                    self.actions = [('move',x,y) for i in range(8)]
            
            "CANT move... Play bump into noise"
            if not moving:
                self.actions = [('wait',) for i in range(3)]
    
    
    
    #######################################################
    ##################  PLAYER MOVEMENT  ##################
    #######################################################
    
    def can_move(self, x, y, tile):
        if self.check_for_surf(x,y,tile) == False: return False
        npc_positions = self.get_npc_positions()
        valid_spaces = [i for i in self.valid_spaces if i not in npc_positions]
        if (x,y) in valid_spaces:   return True
        else:                       return False
    
    def calc_position(self):
        return round(self.subpos[0]/16), round(self.subpos[1]/16)
    
    def check_for_surf(self, x, y, tile):
        if not 'water' in tile: return True
        return self.surfing
    
    def start_surfing(self, x, y, tile):
        if self.surfing: return False
        if 'water' in tile:
            self.actions = [('start_surf',x,y) for i in range(16)]
            self.player.moving = x,y
            self.surfing = True
            return True
        return False
    
    def check_for_ledge(self, tile):
        ledge_type  = "ledge_"+['down','left','up','right'][self.player.facing]
        return ledge_type == tile
    
    def stop_surfing(self, tile):
        if not self.surfing: return False
        if 'water' not in tile: self.surfing = False
    
    
    #######################################################
    #######################################################
    


####################################################################
####################################################################




















####################################################################
####################################################################

def run(App, queue=None):
    framerate   = 1/45
    window      = App(queue)
    
    def update_():
        window.update()
        sleep(framerate)
    
    while True:
        if window.show_error: update_()
        else:
            try: update_()
            except TclError:
                '''This is just what happens when it trys to update a
                canvas that isnt there anymore'''
                break
            except Exception as e:
                '''As long as we have it break out of this loop
                then the music player will close successfully'''
                print('run(App) loop closed with unhandled exception:\n\t',e)
                break

####################################################################
####################################################################

if __name__ == '__main__':
    run(App)

####################################################################
####################################################################

