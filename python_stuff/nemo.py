#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 18:25:00 2018

@author: inesverissimo


"""

from psychopy import visual, core, event 
import numpy as np
import random 
import pickle

# draw fixation cross function
def draw_fixation(posit,lineSize,linecolor,linewidth): 
    
    t = lineSize/2.0
    vertical_line = visual.Line(win,start = (posit[0],posit[1]-t),end = (posit[0],posit[1]+t),lineColor = linecolor,lineWidth=linewidth)
    horizontal_line = visual.Line(win,start = (posit[0]-t,posit[1]),end = (posit[0]+t,posit[1]),lineColor = linecolor,lineWidth=linewidth)
    
    vertical_line.draw()
    horizontal_line.draw() 
    
    

########## Initial parameters #########
# screen info   
hRes = 1920 #900 #1920
vRes = 1080 #700 #1080  
screenHeight = 30 #height of the screen in cm 
screenDis = 71    #distance between screen and chinrest in cm     
backCol = 'black'
# fixation cross info
fixpos = (0,0) #position
fixlineSize = 15
fixcolor = 'white'
linewidth = 5
# stim info
num_img = np.repeat(range(0,17),2)
# general info
num_blk = 2 #total number of blocks
num_trl = len(num_img) #total number of trials
stim_time = 2.5 #stimulus presentation time (seconds)
iti = 3.4 #inter-trial-interval (seconds)
RT_trl = np.array(np.zeros((num_blk,num_trl)),object) #array for all RTs
img_index = np.zeros((num_blk,num_trl),dtype=int) #array to save all indexes used

# create a window
#win = visual.Window(size= (hRes, vRes), monitor="testMonitor", color = backCol, units="pix")
win = visual.Window(size= (hRes, vRes), color = backCol, units='pix',fullscr  = True, screen = 1,allowStencil=True)   

pp = '0' #raw_input("Participant number: ")
 
#pause
core.wait(2.0)



for j in range(num_blk): #start block
    
    text = 'Block %i' %(j+1)
    BlockText = visual.TextStim(win, text=text, color='white', height=50, pos = (0,140))
    text2 = 'Press spacebar to start'
    PressText = visual.TextStim(win, text=text2, color='white', height=30, pos = (0,-140))
    
    BlockText.draw()
    PressText.draw()
    draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation 
    win.flip()
    event.waitKeys(keyList = 'space') 

    draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation 
    win.flip() # flip the screen
    core.wait(2.0) #pause
    
    np.random.shuffle(num_img) #shuffle indexes to guarantee random trials
            
    for i in range(num_trl): #start trials

        img_dir = "nemo_images/img%d.jpeg" %(num_img[i])
        img = visual.ImageStim(win,image=img_dir,units="pix",pos = (0,0))
        img.draw()
        draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation        
        win.flip()
        
        t0 = core.getTime() #get the time (seconds)
        key = [] # reset key to nothing 
           
        while not key:
            key = event.getKeys(keyList = ['space'])
            if core.getTime()-t0 > stim_time:
                break
        
        RT = core.getTime() - t0
        
        if RT > stim_time:
            RT_trl[j][i] = float('nan') #if response takes longer than stim period, then put nan
        else:
            RT_trl[j][i] = RT #else save actual RT
        
    img_index[j][:] = num_img # image index for all blocks and trials
    win.flip() # flip the screen
    core.wait(iti) #pause    

dict_var = {'RT':RT_trl,'indexes':img_index}

#save data of interest
with open('data_Nemo_pp_' + pp + '.pickle', 'wb') as write_file:
    pickle.dump(dict_var, write_file,protocol=pickle.HIGHEST_PROTOCOL)

#cleanup
win.close() #close display
core.quit()
