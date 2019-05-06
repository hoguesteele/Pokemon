''' Doc_String '''

from my_headers import ii
from multiprocessing import Process, Queue, active_children
from queue import Empty
from os import path


music_folder = r'C:\Users\Hogue\Desktop\Code Challenges\Pokemon\MUSIC\WAV'

####################################################################
####################################################################
import pyaudio
import wave






CHUNK = 1024
paud = pyaudio.PyAudio()



song = path.join( music_folder, r"60 New Bark Town's Theme.wav")


wf = wave.open(song, 'rb')

stream = paud.open(format=8, channels=2, rate=44100, output=True)

data = wf.readframes(CHUNK)

n = 1
while data != '':
    n +=1
##    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

paud.terminate()

####################################################################
####################################################################


def _play_( data ):
    stream.write(data)
    data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    paud.terminate()
    return 0


##def _play_( file_path ):
##    CHUNK = 1024
##    paud = pyaudio.PyAudio()
##    wf = wave.open(file_path, 'rb')
##    
##    stream = paud.open(format=8, channels=2, rate=44100, output=True)
##
##    data = wf.readframes(CHUNK)
##
##    while data != '':
##        stream.write(data)
##        data = wf.readframes(CHUNK)
##
##    stream.stop_stream()
##    stream.close()
##
##    paud.terminate()
##    return 0


####################################################################
####################################################################

def _player_( file_path ):
    "Get AudioSegment instance"
    FP = path.join(music_folder, file_path)
    raw_song = AudioSegment.from_file(FP, 'wav')
    "Lower volume"
    song = raw_song - 9
    "Play the file"
    play(song)
    return 0

def close_last_player( player ):
    "Ends last audio player process"
    if type(player) == Process:
        if player.is_alive():
            player.terminate()

def poll_queue( queue ):
    "Blocks until SONG is sent, then starts Process to play SONG"
    player = None
    
    while True:
        "Wait until new song sent via the queue"
        song_path = queue.get(block=True,timeout=None)
        
        if song_path == 'break' or '':
            close_last_player( player )
            break
        
        "end last audio player process"
        close_last_player( player )
        
        "Start a process that listens for the next Audio track"
        player = Process(target=_player_, args=( song_path, ))
        player.daemon = True
        player.start()

####################################################################
####################################################################

def run(q):
    while True:
        IN = input()
        q.put(IN)
        if IN == '':
            break

####################################################################
####################################################################

def main_loop():
    
    "Create QUEUE and start progress_bar process"
    queue = Queue()
    
    "Start a process that listens for the next Audio track"
    music_player = Process(target=poll_queue, args=( queue, ))
    music_player.start()
    
    queue.put(song)
    "Start the main App"
    run(queue)
    
    
    ## Close Processes ##
    "Check if music player is still running"
    if music_player.is_alive():
        queue.put('break')
        music_player.terminate()

####################################################################
####################################################################

##if __name__ == '__main__':
##    
##    main_loop()
    
####################################################################
####################################################################
