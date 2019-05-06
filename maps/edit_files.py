''' Doc_String '''

from os import listdir, mkdir, getcwd, chdir, path
from my_headers import ii


####################################################################
####################################################################


####################################################################
####################################################################

print()

maindir = getcwd()

folders = ['cherrygrove','home','house1','house2','my_room',
         'newbark','professor_elm','route_27','route_29']



for folder in folders:
    print('{:#^80}'.format(f" {folder} "))
    chdir(folder)
    
    
    
    files = [i for i in listdir() if i[-4:] == '.txt']
    
    
    for file in files:
        with open(file,'r') as file_obj: dat = file_obj.read()
        if len(dat): continue
        print(file, len(dat))
        
        with open(file,'w') as file_obj: file_obj.write('.')
    
    chdir(maindir)
    print()


##files = listdir()








####################################################################
####################################################################


##def main():
##    to_make = 'bgs','doors','music','signs','tiles'
##    new_data = {k:[] for k in to_make}
##    npcs = {}
##    if 'data.txt' not in listdir(): return 0
##    with open('data.txt','r') as f: data = f.read().splitlines()
##    
##    for line in data:
##        if not line: continue
##        
##        if line.startswith('sign='):
##            new_data['signs'].append(line.replace('sign=',''))
##        if line.startswith('extra_bg='):
##            new_data['bgs'].append(line.replace('extra_bg=',''))
##        if line.startswith('music='):
##            new_data['music'].append(line.replace('music=',''))
##        
##        if line.startswith('move='):
##            if line == 'move=#': continue
##            if ':' in line:
##                new_line = [[j.strip() for j in i.split(':')]
##                      for i in line.split('=')[-1].split(',')]
##                dat = ''.join([f"{k}:{v:>3},   " for k,v in new_line]
##                              )[:-4].replace('tile:','tile: ')
##            else:
##                x,y = [i for i in line.split('=')[-1].split(',')]
##                dat = f"x:{x:>3},   y:{y:>3},   tile: None"
##            new_data['tiles'].append(dat)
##        
##        if line.startswith('door='):
##            new_line = [[j.strip() for j in i.split(':')]
##                  for i in line.split('=')[-1].split(',')]
##            bg = new_line.pop(2)
##            wash = ['washout','  True']
##            if len(new_line) == 6:
##                new_line.pop()
##                wash = ['washout',' False']
##            new_line.extend([wash,bg])
##            dat = ''.join([f"{k}:{v:>3},   " for k,v in new_line]
##                          )[:-4].replace('bg:','bg: ')
##            new_data['doors'].append(dat)
##        
##        
##        if line.startswith('npc='):
##            _,values = [i.strip() for i in line.split('=')]
##            name = values.split(',')[0].split(':')[-1]
##            print(name)
##            facing = ['facing','0']
##            frozen = ['frozen','False']
##            type_  = ['type',name]
##            if ':' in line:
##                vv = [i.strip().split(':') for i in values.split(',') if 'name' not in i]
##                if 'type' in [k for k,v in vv]:
##                    type_ = vv.pop([k for k,v in vv].index('type'))
##                if 'facing' in [k for k,v in vv]:
##                    facing = vv.pop([k for k,v in vv].index('facing'))
##                if 'frozen' in [k for k,v in vv]:
##                    frozen = vv.pop([k for k,v in vv].index('frozen'))
##                frozen = [f"{i:>6}" for i in frozen]
##                
##                vv.extend([facing,frozen,type_])
##                dat = 'pos='+''.join([f"{k}:{v:>3},   " for k,v in vv])[:-4].replace(
##                    'type:','type: ')
##            else:
##                name, x, y = [i.strip() for i in values.split(',')]
##                vv = [['x',x], ['y',y]]
##                vv.extend([facing,frozen,type_])
##                dat = 'pos='+''.join([f"{k}:{v:>3},   " for k,v in vv])[:-4].replace(
##                    'type:','type: ')
##            npcs[name] = {'pos':dat,'move':[],'data':''}
##        
##        if line.startswith('npc_move='):
##            _,values = line.split('=')
##            name = values.split(',')[0]
##            x,y = values.replace(f"{name},",'').split(',')
##            dat = f"move=x:{x.strip():>3}, y:{y.strip():>3}"
##            npcs[name]['move'].append(dat)
##        
##        if line.startswith('npc_interact='):
##            _,values = line.split('=')
##            name = values.split(',')[0].split(':')[-1]
##            dat = f"interact={values.replace('name:','').replace(name+', ','')}"
##            npcs[name]['interact'] = dat
##
##
##    ####################################################################
##
##    for name,value_dict in npcs.items():
##        for key,val in value_dict.items():
##            if key == 'data': continue
##            if key == 'move': npcs[name]['move'] = '\n'.join(npcs[name]['move'])
##            npcs[name]['data'] += npcs[name][key]
##            npcs[name]['data'] += '\n\n'
##        npcs[name]['data'] = npcs[name]['data'].replace('\n\n\n','\n')[:-2]
##
##
##
##    for k,v in new_data.items():
##        joiner = '\n\n'
##        if k == 'tiles': joiner = '\n'
##        new_data[k] = joiner.join(new_data[k])
##
##
##    ####################################################################
##
##
##    for k,v in new_data.items():
##        print(f"\t    {k.upper()}  \n")
##        file_name = f"{k}.txt"
##        with open(file_name,'w') as f: f.write(v)
##    
##    
##    try: mkdir('npcs')
##    except: print('already made NPC file','\n')
##    
##    mainfile = getcwd()
##    npcdir = path.join(mainfile,'npcs')
##    chdir(npcdir)
##    
##    for name,value_dict in npcs.items():
##        print(f"\t    {name.upper()}  \n")
##        file_name = f"{name}.txt"
##        with open(file_name,'w') as f: f.write(npcs[name]['data'])
##    
##    chdir(mainfile)


####################################################################
####################################################################





####################################################################
####################################################################


##for file in files:
##    ext = file.split('.')[-1]
##    if (ext != 'txt')  or  (file in ['data.txt','rebuild.txt']): continue
##    
####    with open(file,'r') as f:
####        data = f.read().splitlines()
####    tofile = []
####    
####    for line in data:
####        if not line: continue
####        k,v = line.split('=')
####        tofile.append(v)
####    
####    tofile = '\n'.join(tofile)
####    print(f"\n{'#'*80}\n")
##    print(file.upper(),'\n')
####    print(f'"{tofile}"')
####    
####    with open(file,'w') as f:
####        f.write(tofile)






##with open('bgs.txt','r') as file:
##    data = file.read()
##data = data.replace(' ','')
##data = data.replace('glow_0','grass')
##data = data.replace('glow_1','ledge')
##data = data.replace('glow_2','encounter_grass')
##print(data)
##
##
##with open('data.txt','w') as file:
##    file.write(data)


####################################################################
####################################################################



























####################################################################
####################################################################


####################################################################
####################################################################


####################################################################
####################################################################

