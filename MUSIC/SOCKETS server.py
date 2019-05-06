''' Doc_String '''

import audioop
import pyaudio
import wave
from os import chdir, listdir
from time import time, sleep
import socket




####################################################################
####################################################################

CHUNK = 1024

####################################################################
####################################################################

def server_program():
    host            = socket.gethostname()
    port            = 5000
    server_socket   = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(2)
    
    print('Attempting to connect to Client')
    conn, address   = server_socket.accept()
    print('Connected! Recieving data')
    
    paud            = pyaudio.PyAudio()
    stream          = paud.open(format=8, channels=2, rate=44100, output=True)
    
    while True:
        try: data = conn.recv(CHUNK)
        except ConnectionResetError as error: data = False
        if (not data)  or  (data == ''): break
        stream.write(data)
    
    print()
    print('Connection Closed')
    print('Closing Audio stream')
    print('Terminating PyAudio Program')
    conn.close()
    stream.stop_stream()
    stream.close()
    paud.terminate()
    return 0


####################################################################
####################################################################






####################################################################
####################################################################


if __name__ == '__main__':
    server_program()


####################################################################
####################################################################











####################################################################
####################################################################

