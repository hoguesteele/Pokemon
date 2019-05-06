''' Doc_String '''

from headers.headers import *




####################################################################
####################################################################

class Controller:
    def __init__(self, main_app):
        
        "VARIABLES"
        self.main_app  = main_app
        self.key_names = ['q','e','4','5','w','a','s','d','space','Shift']
        
        "ATTRIBUTE CREATION"
        for key_name in self.key_names:
            name = 'key_{}'.format(key_name)
            setattr(self,name,0)
        
        "COOL DOWNS / PREVENTS SENDING EVENT MULTIPLE TIMES WHILE KEY IS HELD DOWN"
        self.hold_key_names = ['q','e','4','5','Shift','space']
        for key_name in self.hold_key_names:
            name = 'key_{}_held'.format(key_name)
            setattr(self,name,0)


    "FUNCTIONS"
    
    def key_release(self, key_name):
        setattr(self, 'key_{}'.format(key_name), 0)
        self.main_app.key_release( key_name )
        
        "IF WE HAVE A COOLDOWN FOR THAT KEY, TURN IT OFF"
        if key_name in self.hold_key_names:
            setattr(self, 'key_{}_held'.format(key_name), False)
    
    def key_press(self, key, key_name):
        "SKIP SENDING INPUTS FOR CERTAIN KEYS WHEN THEY'RE CURRENTLY PRESSED"
        held_down = getattr(self,'key_{}_held'.format(key_name), False)
        if held_down == True: return 0
        
        "SET KEY_VALUE TO +1 UNTIL VALUE == 8"
        "SEND INPUTS TO THE MAIN_APP"
        if key < 8: setattr(self, 'key_{}'.format(key_name), key+1)
        self.main_app.key_press( key_name, key )
        
        "IF WE HAVE A COOLDOWN FOR THAT KEY, TURN IT ON"
        if key_name in self.hold_key_names:
            setattr(self, 'key_{}_held'.format(key_name), True)
    
    def get_input(self):
        for key_name in self.key_names:
            key = getattr(self,'key_{}'.format(key_name))
            if is_pressed(key_name):                self.key_press(key, key_name)
            if not is_pressed(key_name) and key:    self.key_release(key_name)


####################################################################
####################################################################



####################################################################
####################################################################

