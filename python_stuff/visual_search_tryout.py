
# -*- coding: utf-8 -*-
"""
Created 6th June 2018
Author: Ines V.

Descrip: Try out script for simple visual search task
"""

from psychopy import visual, core, event #import some libraries from PsychoPy
import numpy as np
import random 
#import pickle

########## Initial parameters #########
# general info
num_blk = 2 #number of blocks
num_trl = 10 #number of trials
# screen info   
hRes = 1920 #900 #1920
vRes = 1080#700 #1080      
backCol = 'black'
# fixation cross info
fixpos = (0,0)
fixlineSize = 15
fixcolor = 'white'
linewidth = 2
# gabor info
siz_gab = 100
dist1 = 360/6 #distance between stim (degrees)
dist2 = 360/12 #distance between stim (degrees)
init_dgr1 = 0 #initial pos (degree) for 1st row stim
init_dgr2 = 30 #initial pos (degree) for 2nd row stim
hyp1 = 150 
hyp2 = hyp1 + siz_gab + 50

ort_trgt = 330 #orientation of target (degrees)
ort_distr = 30 #orientation of distractors (degrees)
num_empty = 5 #number of empty positions
lbl_trgt = 1 #target label (integer)
lbl_distr = 2 #distractor label (integer)
lbl_emp = 0 #empty position label (integer)


#######################################
### functions ###
# draw fixation cross function
def draw_fixation(posit,lineSize,linecolor): 
    
    t = lineSize/2.0
    vertical_line = visual.Line(win,start = (posit[0],posit[1]-t),end = (posit[0],posit[1]+t),lineColor = linecolor,lineWidth=linewidth)
    horizontal_line = visual.Line(win,start = (posit[0]-t,posit[1]),end = (posit[0]+t,posit[1]),lineColor = linecolor,lineWidth=linewidth)
    
    vertical_line.draw()
    horizontal_line.draw() 
    
# transform polar coordinates to cartesian
    
def pol2cart(hyp, theta):  
    x = hyp * np.cos(np.deg2rad(theta))
    y = hyp * np.sin(np.deg2rad(theta))
    return(x, y)
    
#######################################
    
# x,y position arrays + labels for conditions
posrow1 = np.arange(init_dgr1,init_dgr1+360,dist1)
(xpos1,ypos1) = pol2cart(hyp1, posrow1)
posrow2 = np.arange(init_dgr2,init_dgr2+360,dist2)
(xpos2,ypos2) = pol2cart(hyp2, posrow2)

poslist_x = np.append(xpos1,xpos2)
poslist_y = np.append(ypos1,ypos2)
poslist_lbl = np.append(np.full((1,num_empty),lbl_emp),np.full((1,len(poslist_x)-(num_empty+1)),lbl_distr))
poslist_lbl = np.append(poslist_lbl,[lbl_trgt])

# create a window
#win = visual.Window(size= (hRes, vRes), monitor="testMonitor", color = backCol, units="pix")
win = visual.Window(size= (hRes, vRes), color = backCol, units='pix',fullscr  = True, screen = 1,allowStencil=True)   
   
#pause
core.wait(2.0)

for j in range(num_blk):

    text = 'Block %i' %(j+1)
    BlockText = visual.TextStim(win, text=text, color='white', height=50, pos = (0,140))
    gabor = visual.GratingStim(win=win,tex='sin',mask='gauss',ori=ort_trgt,sf=0.05,size=siz_gab,pos=(0,0))
    text2 = 'Press spacebar to start'
    PressText = visual.TextStim(win, text=text2, color='white', height=30, pos = (0,-140))
    
    BlockText.draw()
    gabor.draw()
    PressText.draw()
    win.flip()
    event.waitKeys(keyList = 'space') 

    draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
    win.flip() # flip the screen
    core.wait(2.0) #pause
    
    for k in range(num_trl):
        
        np.random.shuffle(poslist_lbl) #randomize labels
        #position list for display
        poslist = np.vstack((poslist_x,poslist_y))
        poslist = np.vstack((poslist,poslist_lbl))

        for i in range(len(poslist[0])):
            if poslist[2][i] == 1:
                gabor = visual.GratingStim(win=win,tex='sin',mask='gauss',ori=ort_trgt,sf=0.05,size=siz_gab,pos=(poslist[0][i],poslist[1][i]))
            elif poslist[2][i] == 0:
                gabor = visual.ShapeStim(win=win,lineColor='black',lineColorSpace='rgb',fillColor='black',fillColorSpace='rgb',size=siz_gab,pos=(poslist[0][i],poslist[1][i]))
            else:
                gabor = visual.GratingStim(win=win,tex='sin',mask='gauss',ori=ort_distr,sf=0.05,size=siz_gab,pos=(poslist[0][i],poslist[1][i]))
            gabor.draw()
    
        draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation
        win.flip() # flip the screen
        event.waitKeys(keyList = 'space') 
    
        draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
        text3 = 'Move your eyes back to fixation'
        moveEyesText = visual.TextStim(win, text=text3, color='white', height=30, pos = (0,100))
        moveEyesText.draw()
        win.flip() # flip the screen
        core.wait(2.0) #pause


#cleanup
win.close() #close display
core.quit()



