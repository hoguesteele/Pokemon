''' Doc_String '''


from my_headers import ii
from tkinter    import *
from random     import randint, choice
from keyboard   import is_pressed
from os         import chdir, getcwd, listdir
from PIL        import ImageTk, Image
from time       import sleep
from headers.music_headers import *

####################################################################
####################################################################

main_dir    = getcwd()
framerate   = 1/60
scale       = 3

####################################################################
####################################################################

def get_character_sprites(character='player'):
    chdir('image_assets')
    chdir('character sprites')
    
    img_files = []
    for file in listdir():
        if file.startswith( character ): img_files.append(file)
    
    sprites = {}
    for file in img_files:
        without_character_name = file.replace(character+'_','')
        character_position = without_character_name.replace('.png','')
        
        PL = Image.open(file)
        cw,ch = PL.size
        CW,CH = cw*scale,ch*scale
        PL = PL.resize( (CW,CH) )
        
        sprites[character_position] = PL

    chdir(main_dir)
    return sprites

####################################################################
####################################################################

facing_dict = {0:(0, 1),  1:(-1,0),  2:(0,-1),  3:(1, 0)}

####################################################################
####################################################################

def player_turn( x,y ):
    if   x > 0: return 3
    elif x < 0: return 1
    elif y > 0: return 0
    elif y < 0: return 2

####################################################################
####################################################################

####################################################################
####################################################################
'''#################################################################

#################################################################'''
####################################################################







####################################################################
####################################################################
