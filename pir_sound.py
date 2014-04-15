#pir_sound.py

import os
import random
import time 
import RPi.GPIO as io
import pygame 

io.setmode(io.BCM)
io.setwarnings(False)
pir_pin = 18

io.setup( pir_pin, io.IN)

pygame.mixer.init()

try:
	pygame.mixer.music.load("/mnt/usbdrive/tracks/00.mp3")
except: 
	print
	print
	print("File 00.mp3 not found on thumbdrive. Is it in the right folder? Is the thumbdrive plugged in?")
	print
	print

tr_ck = os.popen('ls -A /mnt/usbdrive/tracks/*.mp3 | wc -l')
num_tracks = int(tr_ck.read())
print("Found "+str(num_tracks)+" tracks on USB Drive.")

#this is where you adjust the play time against every time the sensor is triggered:
global buffer 
buffer = 60

def checkTime():
	print("Checking Time")
	print( str( int(time.time()-track_timer)))
def beginPlay(current_track):
	global r
	global track_play_time
	global track_length	
	print("Now Playing: 0"+str(current_track)+".mp3")
	pygame.mixer.music.load("/mnt/usbdrive/tracks/0"+str(current_track)+".mp3")
	tr_m = os.popen('mp3info -p %m /mnt/usbdrive/tracks/0'+str(current_track)+'.mp3')
	tr_s = os.popen('mp3info -p %s /mnt/usbdrive/tracks/0'+str(current_track)+'.mp3') 
	track_length = (int(tr_m.read())*60 )+ int(tr_s.read())
#	print("It is: "+str(track_length)+" seconds long")
	track_play_time = time.time()
	pygame.mixer.music.play()

def endPlay():
	pygame.mixer.music.stop()
	track_timer = time.time()
	track_playing = 0

def inputGiven():
	global track_playing
	global track_timer	
	if  time.time() - track_timer < buffer:
 		track_timer = time.time()
		print("skipping begin play")
	else :
		beginPlay(int(randomGenerator()))
	
	track_timer = time.time()
	
		track_playing = 1
	
def randomGenerator():
	global last_track
	global r 
	
	r = random.randint( 0, num_tracks-1)
	if r == last_track:
		r = 0
		return r
	else: 	
		#beginPlay(r)
		last_track = r
		return r

###
prog_start = time.time()	
last_track = 0
track_playing = 0
track_timer = 0
###
beginPlay(randomGenerator())
track_timer = time.time()
track_playing = 0
while True:

	if io.input( pir_pin):
		inputGiven()		

	if time.time() - track_play_time > track_length:
		beginPlay(int(randomGenerator()))
		print("BEGIN PLAY")
	
	if time.time() - track_timer > buffer:
		endPlay()
	

