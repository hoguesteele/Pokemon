''' Doc_String '''



####################################################################
####################################################################

def main_loop( App ):
    
    "Create QUEUE and start progress_bar process"
    queue = Queue()
    
    "Start a process that listens for the next Audio track"
    music_player = Process(target=poll_queue, args=( queue, ))
    music_player.start()
    
    
    "Start the main App"
    run(App, queue)
    
    
    ## Close Processes ##
    "Check if music player is still running"
    if music_player.is_alive():
        queue.put('break')
        music_player.join(timeout=0.1)
        
        "Check if JOIN failed"
        if music_player.is_alive():
            print('music_player still alive...')
            print('Killing music_player','\n')
            music_player.terminate()

####################################################################
####################################################################

if __name__ == '__main__':
    
    from MAIN import *
    
    main_loop( App )
    
####################################################################
####################################################################
