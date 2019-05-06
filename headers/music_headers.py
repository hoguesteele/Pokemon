''' Doc_String '''

music_folder = r'C:\Users\Hogue\Desktop\Code Challenges\Pokemon V5\MUSIC\WAV'


from my_headers import ii
from multiprocessing import Process, Queue, active_children
from queue import Empty
from os import path


####################################################################
####################################################################

from warnings import filterwarnings
filterwarnings( 'ignore', ".*Couldn't find ffplay or avplay*.")
filterwarnings( 'ignore', ".*Couldn't find ffmpeg or avconv*.")
from pydub import AudioSegment
from pydub.playback import play

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
        
        if song_path == 'break':
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



####################################################################
'''#################################################################

Ideally:

We have the ability to play SOUND EFFECTS as needed,
And we can have songs FADE OUT on queue


** PyAudioMixer may be the key to getting the functionality we need **


Or we could be dumb and try to learn how PYDUB
    uses PyAudio, then try to set up our own mixer by
    editing the chunks of data as theyre sent to the audio_stream
Of course then we'd have to do more multiprocessing to
    create a proper mixer with multiple channels for
    the main audio, the next track, and sound effects

It'd be dumb because there's value in learning how to use
    a project that someone else has already built,
    In that the process would be similar to what one might
    experience at an actual job, learning about the proprietary
    software && frameworks that your company uses

Though the knowledge you may gain while working with multiprocessing
    more, as well as audio processing may be of enough value to
    merit trying it out at some point.

But just learn how to use PyAudioMixer dummy.
    The short term time savings and challenge of learning a new
    API are better suited to your current goals.

Loooove youuu
    -Nicholas



#################################################################'''
####################################################################

##import PyAudioMixer


if __name__ == '__main__':
    
    test = path.join( music_folder, r"60 New Bark Town's Theme.wav")

    song = AudioSegment.from_file(test, 'wav')

    "Make it quieter"
    song = song - 6

    "Get only the first part"
    seconds = 38
    seconds = 5
    song    = song[:seconds*1000]

    '''
    There's no way to fade out a song if you dont know
    when it will end ahead of time...
    newbark loops at 37 ish seconds


    '''
####    help(song)
####    song = song.fade_out(3000)


    play( song )
    pass

####################################################################
'''#################################################################

from pydub import AudioSegment

    song = AudioSegment.from_wav("never_gonna_give_you_up.wav")


Save Song:

    song.export(' /folder/song_name.wav', 'wav')


Slice audio:

    # pydub does things in milliseconds
    ten_seconds = 10 * 1000

    first_10_seconds = song[:ten_seconds]

    last_5_seconds = song[-5000:]

Make the beginning louder and the end quieter

    # boost volume by 6dB
    beginning = first_10_seconds + 6

    # reduce volume by 3dB
    end = last_5_seconds - 3

Concatenate audio (add one file to the end of another)

    without_the_middle = beginning + end

How long is it?

    without_the_middle.duration_seconds == 15.0

AudioSegments are immutable

    # song is not modified
    backwards = song.reverse()

Crossfade (again, beginning and end are not modified)

    # 1.5 second crossfade
    with_style = beginning.append(end, crossfade=1500)

Repeat

    # repeat the clip twice
    do_it_over = with_style * 2

#################################################################'''
####################################################################







####################################################################
####################################################################
