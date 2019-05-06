''' Doc_String '''




####################################################################
r'''################################################################


pydub makes stuff quieter by:
applying a gain to the audio_segment like this:

def apply_gain(self, volume_change):
    
    self._data --> is a bytes object
    
    
    sample_rate = struct.unpack_from('<I', data[pos + 4:pos + 8])[0]
    wav_data = read_wav_audio(data)
    self.sample_width = wav_data.bits_per_sample // 8
    
    
    dat = audioop.mul(self._data, self.sample_width, db_to_float(float(volume_change)))
    
    return self._spawn(data=dat)



#################################################################'''
####################################################################

def _stream_( data_queue, exit_queue ):
    "Blocks until SONG is sent, then starts Process to play SONG"
    paud   = pyaudio.PyAudio()
    stream = paud.open(format=8, channels=2, rate=44100, output=True)
    print('starting _stream_')
    
    while True:
        "Wait until new song sent via the queue"
        data = data_queue.get(block=True,timeout=None)
        if data == '': break
        stream.write(data)
    
    stream.stop_stream()
    stream.close()
    paud.terminate()
    print('close _stream_')
    
    return 0

####################################################################
####################################################################

def poll_queue( song_queue, data_queue, exit_queue ):
    "Blocks until SONG is sent, then starts Process to play SONG"
    player = None
    print('starting poll_queue')
    
    while True:
        "Wait until new song sent via the queue"
        song = song_queue.get(block=True,timeout=None)
        
        
        if song == 'lower':
            print('lower (NOT IMPLIMENTED)')
            continue
        
        "End last audio player process"
        if player != None:
            print('terminating _mixer_')
            player.terminate()
        
        if song == '': break
        print('s:',song)
        print('r:',repr(song))
        
        
        "Start a process that listens for the next Audio track"
        player = Process(target=_mixer_, args=( song, data_queue ))
        player.daemon = True
        player.start()
    
    print('close poll_queue')

####################################################################
####################################################################

def _mixer_( song, data_queue ):
    "sends song data to the stream process"
    print('starting _mixer_')
    CHUNK = 1024
    wf    = wave.open(song, 'rb')
    data  = wf.readframes(CHUNK)
    
    while data != '':
        data_queue.put(data)
        data = wf.readframes(CHUNK)
    return 0

####################################################################
####################################################################

def run(song_queue):
    "Proxy that allows us to select a song and it sends the song to the mixer"
    songs = listdir()[10:20]
    for i,s in enumerate(songs): print(i,s)
    print()
    
    while True:
        IN = input()
        if IN == ' ' or IN == 'lower':
            song_queue.put('lower')
            continue
        if IN == '':
            song_queue.put(IN)
            break
        song = songs[int(IN)]
        song_queue.put(song)

####################################################################
####################################################################

def main_loop():
    
    
    "Create QUEUE and start progress_bar process"
    song_queue = Queue()
    data_queue = Queue()
    exit_queue = Queue()
    
    "Start a process that listens for & plays audio data"
    stream_proc = Process(target=_stream_, args=( data_queue, exit_queue ))
    stream_proc.start()
    
    "Start a process that listens for the next Audio track"
    music_player = Process(target=poll_queue, args=( song_queue, data_queue, exit_queue ))
    music_player.start()
    
    "Start the main App"
    run(song_queue)
    
    
    ## Close Processes ##
    "Check if music player is still running"
    if stream_proc.is_alive():
        data_queue.put('')
        stream_proc.join(1)
        if stream_proc.is_alive():
            print('terminating stream_proc')
            stream_proc.terminate()
    
    if music_player.is_alive():
        song_queue.put('')
        music_player.join(1)
        if music_player.is_alive():
            print('terminating music_player')
            music_player.terminate()
    

####################################################################
r'''################################################################

bits per sec = 4 * sample_rate * secs


#################################################################'''
####################################################################

import audioop
import pyaudio
import wave
from multiprocessing import Process, Queue, active_children
from queue import Empty
from os import path, chdir, listdir
from time import ctime



music_folder = r'C:\Users\Hogue\Desktop\Code Challenges\Pokemon\MUSIC\WAV'
chdir(music_folder)

if __name__ == '__main__':
    
    main_loop()
    pass

    
####################################################################
####################################################################













