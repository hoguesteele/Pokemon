''' Doc_String '''

import audioop
import pyaudio
import wave
from multiprocessing import Process, Queue, active_children
from queue import Empty
from os import chdir, listdir
from time import time



####################################################################
####################################################################

music_folder = r'C:\Users\Hogue\Desktop\Code Challenges\Pokemon V5\MUSIC\WAV'
chdir(music_folder)

####################################################################
####################################################################

songs = listdir()[10:20]
for i,s in enumerate(songs): print('{:>2}  {}'.format(i,s))
print('\n  Pick a song to play:\n\t',end='')
##IN = input()
##song = songs[int(IN)]
song = songs[0]
song = songs[2]

print('\nPlaying:',song,'\n\n')



paud    = pyaudio.PyAudio()
stream  = paud.open(format=8, channels=2, rate=44100, output=True)
CHUNK   = 1024
wf      = wave.open(song, 'rb')
data    = wf.readframes(CHUNK)

start   = time()
secs    = 1
qsecs   = 0.25
durr    = 5

while (time() - start) < durr:
    data = wf.readframes(CHUNK)
    if (not data)  or  (data == ''): break
    stream.write(data)
    
    "Show elapsed play time"
    if (time() - start) >= qsecs:
        qsecs += 0.25
        if (time() - start) >= secs:
            print(secs,end='')
            secs += 1
        else: print('.',end='')


stream.stop_stream()
stream.close()
paud.terminate()


####################################################################
####################################################################






####################################################################
####################################################################


##if __name__ == '__main__':
##    
##    song = choose_song()
##    client_program(song)
##    
##    #


####################################################################
####################################################################











####################################################################
####################################################################

