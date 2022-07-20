import os
import sys
import time
import subprocess
import random

global playlistlink

#put your youtube playlist link here 
playlistlink = "https://youtube.com/playlist?list=PLuKpO2KmUaHC84gQgcWEaxGau3uV6HVVs"

#initialise static video on layer 1 
backgroundloop = ['omxplayer', 
                  '--no-osd', 
                  '--loop', 
                  '--layer', 
                  '1', 
                  '--aspect-mode', 
                  'fill', 
                  'assets/static.mp4']
playstatic = subprocess.Popen(backgroundloop, stdin=subprocess.PIPE)

while True:
    #get number of videos in playlist
    command = ['yt-dlp', 
               '-i', 
               '--no-warnings', 
               '--yes-playlist', 
               '--playlist-end', 
               '1', 
               '--print', 
               '"%(playlist_count)s"', 
               playlistlink]
 
    print(command)

    p = subprocess.Popen(command,
                         shell=False,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    number = int(((stdout.decode('ascii')).strip()).replace('"', '')) #convert returned value to int
    print(number)

    #generate random order based on number of videos in playlist
    randomlist = random.sample(range(1, number+1), number)
    print(randomlist)

    for x in range(1, (number+1)):
        print('playing ' + str(randomlist[x-1]) + ' of ' + str(number))

        #initialise youtube video on layer 2
        commandyt = 'omxplayer --layer 2 --no-osd --aspect-mode fill `yt-dlp -g -f 18 --no-warnings --playlist-items ' + str(randomlist[x-1]) + " " + playlistlink + '`'
        playyt = subprocess.Popen(commandyt, shell=True)
        playyt.wait()
