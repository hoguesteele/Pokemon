''' Doc_String '''

import audioop
import pyaudio
import wave
from os import chdir, listdir
from time import time, sleep
import socket




####################################################################
####################################################################

music_folder = r'C:\Users\Hogue\Desktop\Code Challenges\Pokemon V5\MUSIC\WAV'
chdir(music_folder)
CHUNK = 1024

####################################################################
####################################################################

def client_program(song):
    host = socket.gethostname()
    port = 5000
    client_socket = socket.socket()
    
    
    print('Attempting to connect to Host')
    while True:
        try:
            client_socket.connect((host, port))
            break
        except ConnectionRefusedError as e: sleep(1)
    print('Connected! Sending data')
    
    
    "Getting data from song"
    wf          = wave.open(song, 'rb')
    data        = wf.readframes(CHUNK)
    start       = time()
    play_time   = 5
    
    
    while (time() - start) < play_time:
        data = wf.readframes(CHUNK)
        if (not data)  or  (data == ''): break
        client_socket.send(data)
    
    print()
    print('Song ended')
    print('Connection Closed')
    client_socket.close()
    return 0
    

####################################################################
####################################################################






####################################################################
####################################################################


if __name__ == '__main__':
    "Choosing song"
    songs = listdir()[10:20]
    for i,s in enumerate(songs): print('{:>2}  {}'.format(i,s))
    print('\n  Pick a song to play:\n\t',end='')
    song = songs[int(input())]
    print('\n{} {}\n\n'.format('Playing:',song))
    
    client_program(song)


####################################################################
####################################################################











####################################################################
####################################################################

