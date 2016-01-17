#!/usr/bin/env python
# 3d to 2d raycaster based on http://lodev.org/cgtutor/raycasting.html
# Dario Clavijo 2016
import curses
import os
import time
import math
#os.system('clear') 

mapWidth = 24
mapHeight = 24
w=90
h=35
buffer = [[0 for x in range(h)] for x in range(w)] 
stdscr = curses.initscr()

KEY_DOWN='s'
KEY_UP='w'
KEY_LEFT='a'
KEY_RIGHT='d'

worldMap=[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def readKeys():
	c = stdscr.getch()
	return chr(c)	

def getTicks():
	return time.time()

def screen_init():
        for y in range(0,h-2):
                for x in range(0,w):
                        buffer[x][y] = '*'

def cls():
	os.system('clear')

def redraw():
	for y in range(0,h-2):
    		str_ = ""
	    	for x in range(0,w):
      			str_ += str(buffer[x][y])
    		print str_ + "\r"

def verLine(x, drawStart, drawEnd, color):
	for y in range(drawStart,drawEnd):
		#print x,y,color,buffer
		color_str = '\033[%dm' % (91+color)
		buffer[x][y] = color_str + "."

def main():
	screen_init()
	posX = 22.0
	posY = 12.0  #x and y start position
  	dirX = -1.0
	dirY = 0.0 #initial direction vector
  	planeX = 0.0
 	planeY = 0.66 #the 2d raycaster version of camera plane
  
  	time = 0.0 #time of current frame
  	oldTime = 0.0 #time of previous frame

	while True:
    		for x in range(0,w): #(int x = 0 x < w x++)
      			#calculate ray position and direction 
      			cameraX = 2.0 * x / float(w) - 1 #x-coordinate in camera space
      			rayPosX = posX
     			rayPosY = posY
      			rayDirX = dirX + planeX * cameraX
      			rayDirY = dirY + planeY * cameraX
		
		  	#which box of the map we're in  
      			mapX = int(rayPosX)
      			mapY = int(rayPosY)
       
      			#length of ray from current position to next x or y-side
      			#float sideDistX
      			#float sideDistY
       
       			#length of ray from one x or y-side to next x or y-side
    
			if(rayDirX != 0):		
  				deltaDistX = math.sqrt(1.0 + (rayDirY * rayDirY) / (rayDirX * rayDirX))
      			else:
				deltaDistX = 999999
			if(rayDirY!=0):
				deltaDistY = math.sqrt(1.0 + (rayDirX * rayDirX) / (rayDirY * rayDirY))
      			else:
				deltaDistY = 999999
			#float perpWallDist
       
      			#what direction to step in x or y-direction (either +1 or -1)
      			#int stepX
      			#int stepY

      			hit = 0 #was there a wall hit?
      			#int side #was a NS or a EW wall hit?

			 #calculate step and initial sideDist
      			if (rayDirX < 0):
        			stepX = -1
        			sideDistX = (rayPosX - mapX) * deltaDistX
      			else:
        			stepX = 1
        			sideDistX = (mapX + 1.0 - rayPosX) * deltaDistX
      			if (rayDirY < 0):
        			stepY = -1
        			sideDistY = (rayPosY - mapY) * deltaDistY
      			else:
        			stepY = 1
        			sideDistY = (mapY + 1.0 - rayPosY) * deltaDistY

      			#perform DDA
      			while (hit == 0):
        			#jump to next map square, OR in x-direction, OR in y-direction
        			if (sideDistX < sideDistY):
          				sideDistX += deltaDistX
          				mapX += stepX
          				side = 0
        			else:
          				sideDistY += deltaDistY
          				mapY += stepY
          				side = 1
        			#Check if ray has hit a wall
        			if (worldMap[mapX][mapY] > 0): 
					hit = 1 

      			#Calculate distance projected on camera direction (oblique distance will give fisheye effect!)
      			if (side == 0):
      				perpWallDist = math.fabs((mapX - rayPosX + (1 - stepX) / 2) / rayDirX)
      			else:
      				perpWallDist = math.fabs((mapY - rayPosY + (1 - stepY) / 2) / rayDirY)
     
		 	#Calculate height of line to draw on screen
      			lineHeight = int(abs(int(h / perpWallDist)))
     			#calculate lowest and highest pixel to fill in current stripe
      			drawStart = int(-lineHeight / 2 + h / 2)
      			if(drawStart < 0):
				drawStart = 0
      			drawEnd = int(lineHeight / 2 + h / 2)
      			if(drawEnd >= h):
				drawEnd = h - 1

      			#choose wall color
      			#ColorRGB color
      			color = worldMap[mapX][mapY]
       
      			#give x and y sides different brightness
      			#if (side == 1):
			#	color = color / 2

     		 	#draw the pixels of the stripe as a vertical line
      			verLine(x, drawStart, drawEnd, color)

    		#timing for input and FPS counter
    		oldTime = time
    		time = getTicks()
    		frameTime = (time - oldTime) / 1000.0 #frameTime is the time this frame has taken, in seconds
    		print(1.0 / frameTime),"\r" #FPS counter
    		cls()
		redraw()

    		#speed modifiers
    		moveSpeed = frameTime * 5.0 #the constant value is in squares/second
    		rotSpeed = frameTime * 3.0 #the constant value is in radians/second
	
    		keypressed = readKeys()
    		#move forward if no wall in front of you
    		if (keypressed == KEY_UP):
      			if(worldMap[int(posX + dirX * moveSpeed)][int(posY)] == False):
				 posX += dirX * moveSpeed
      			if(worldMap[int(posX)][int(posY + dirY * moveSpeed)] == False):
				 posY += dirY * moveSpeed
    
    		#move backwards if no wall behind you
    		if (keypressed == KEY_DOWN):
      			if(worldMap[int(posX - dirX * moveSpeed)][int(posY)] == False):
				 posX -= dirX * moveSpeed
      			if(worldMap[int(posX)][int(posY - dirY * moveSpeed)] == False):
				 posY -= dirY * moveSpeed
    		
    		#rotate to the right   
    		if (keypressed ==  KEY_RIGHT):
     			#both camera direction and camera plane must be rotated
      			oldDirX = dirX
      			dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
      			dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
      			oldPlaneX = planeX
      			planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
      			planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)
   
    		#rotate to the left
    		if (keypressed == KEY_LEFT):
    			#both camera direction and camera plane must be rotated
      			oldDirX = dirX
      			dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
      			dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
      			oldPlaneX = planeX
      			planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
      			planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)


main()
